from yadet.config.table import TableConfig
from yadet.engine.target.base import TargetEngine
from yadet.objects.base import BaseObject

from typing import Dict, List


class TargetInterface(BaseObject):

    def __init__(self,
                 engine: TargetEngine,
                 table_config: TableConfig,
                 debug: bool = False) -> None:
        self.engine: TargetEngine = engine
        self.table_config: TableConfig = table_config
        self.debug: bool = debug

    def write_batch(self, data: List[Dict], batch_key: str, start_indx: int):
        return self.engine.write_batch(
            table_name=self.table_config.get_output_table_name, data=data, batch_key=batch_key,
            start_indx=start_indx
        )

    def write_meta(self, meta: Dict, batch_key: str):
        return self.engine.write_meta(meta=meta, batch_key=batch_key)

    def __str__(self) -> str:
        return f"{str(self.engine)}"
