from yadet.config.project import ProjectConfig
from yadet.interface.extract_transfer import ExtractTransferInterface
from yadet.interface.source import SourceInterface
from yadet.interface.target import TargetInterface
from yadet.objects.base import BaseObject

from datetime import datetime, timedelta
from dateutil.parser import parse as date_parse
from typing import Any, Dict, Optional


class ProjectBatchRun(BaseObject):

    def __init__(self,
                 project: ProjectConfig,
                 batch_id: Optional[Any] = None,
                 debug: bool = False):
        self.project: ProjectConfig = project
        self.batch_id: Optional[Any] = batch_id
        self.batch_key: str = datetime.today().strftime("%y%m%d-%H%M")
        self.debug: bool = debug
        self._meta: Dict = {}

    def start(self):
        self._meta["batch_id"] = self.batch_id
        self._meta["batch_key"] = self.batch_key
        self._meta["start_datetime"] = datetime.now()
        self._meta["table_meta"] = []

    def end(self):
        self._meta["end_datetime"] = datetime.now()
        self._meta["duration_seconds"] = (
            self._meta["end_datetime"] - self._meta["start_datetime"]
        ).total_seconds()

        # Write Meta for Batch
        self.target_engine.write_meta(meta=self.meta, batch_key=self.batch_key)

        # Update Table Index for Project
        for table_meta in self.meta["table_meta"]:
            if table_meta["records"] > 0:
                self.project.project_table_index.update({
                    table_meta["table"]: {
                        "last_runtime": self._meta["start_datetime"],
                        "columns": table_meta["columns"]
                    }
                })

        self.project.save()

    def add_table_meta(self, table_meta: Dict):
        self._meta["table_meta"].append(table_meta)

    def run_batch(self):
        self.start()
        self.source_engine = self.project.get_source_engine()
        self.target_engine = self.project.get_target_engine()

        for table_config in self.project.tables_config:
            # Skip if Table Config not Active
            if not table_config.active:
                # TODO: Add Meta for Skipped Table
                print(
                    f'[{table_config.get_table_alias}] Skipping inactive table'
                )
                continue

            # Source Table Index
            table_index = self.project.project_table_index.get(
                table_config.get_table_alias, {}
            )

            # Skip if Min Wait is Active
            if table_config.min_wait is not None:
                last_runtime = table_index.get("last_runtime")
                if last_runtime is not None:
                    last_runtime = date_parse(last_runtime)
                    next_runtime = last_runtime + timedelta(seconds=table_config.min_wait * 60)
                    if next_runtime > datetime.now():
                        print(f'[{table_config.get_table_alias}] Skipping table with min wait: {str(next_runtime)}')
                        continue

            source = SourceInterface(
                engine=self.source_engine, table_config=table_config,
                table_index=table_index, debug=self.debug
            )
            target = TargetInterface(
                engine=self.target_engine, table_config=table_config,
                debug=self.debug
            )
            extact_transfer = ExtractTransferInterface(
                source=source, target=target, table_config=table_config,
                debug=self.debug
            )

            # Run Transfer
            table_meta = extact_transfer.extract_transfer(
                batch_key=self.batch_key
            )
            self.add_table_meta(table_meta=table_meta)

        self.end()

    @property
    def meta(self) -> Dict:
        return self._meta
