from yadet.config.table import TableConfig
from yadet.interface.source import SourceInterface
from yadet.interface.target import TargetInterface
from yadet.objects.base import BaseObject

from datetime import datetime
from typing import Dict


class ExtractTransferInterface(BaseObject):

    def __init__(self,
                 source: SourceInterface,
                 target: TargetInterface,
                 table_config: TableConfig,
                 debug: bool = False) -> None:
        self.source: SourceInterface = source
        self.target: TargetInterface = target
        self.table_config: TableConfig = table_config
        self.meta: Dict = {}
        self.debug: bool = debug

    def info(self, msg: str):
        print(f"[{self.table_config.get_table_alias}] {msg}")

    def start(self):
        self.meta["table"] = self.table_config.get_table_alias
        self.meta["start_datetime"] = datetime.now()

    def end(self):
        self.meta["end_datetime"] = datetime.now()
        self.meta["duration_seconds"] = (
            self.meta["end_datetime"] - self.meta["start_datetime"]
        ).total_seconds()

    def extract_transfer(self, batch_key: str) -> Dict:
        self.meta = self.source.fetch_num_records()

        # Start Tracking
        self.start()

        self.info(f"Collecting {self.meta['records']:,.0f} records")

        start_indx = 0
        while start_indx < self.meta["records"]:

            # Extract Data
            data = self.source.fetch_extract_batch(start_indx=start_indx)

            # Write Batch Out
            self.target.write_batch(
                data=data, batch_key=batch_key, start_indx=start_indx
            )

            # Increment Index
            start_indx += self.table_config.batch_size
            self.info(f"Competed batch start_indx={start_indx:,.0f}")

        # End Tracking
        self.end()

        return self.meta

    def __str__(self) -> str:
        return f"{str(self.source)} -> {str(self.target)}"
