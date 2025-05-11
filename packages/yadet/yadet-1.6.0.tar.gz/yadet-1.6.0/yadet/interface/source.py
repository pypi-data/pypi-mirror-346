from yadet.config.table import TableConfig
from yadet.engine.source.base import SourceEngine
from yadet.helpers.base import chunks
from yadet.helpers.parser import parse_value
from yadet.objects.base import BaseObject

import json
from typing import Dict, List, Optional


class SourceInterface(BaseObject):

    def __init__(self,
                 engine: SourceEngine,
                 table_config: TableConfig,
                 table_index: Dict,
                 debug: bool = False) -> None:
        self.engine: SourceEngine = engine
        self.table_config: TableConfig = table_config
        self.table_index: Dict = table_index
        self.debug: bool = debug

    def info(self, msg: str):
        print(f"[{self.table_config.get_table_alias}] {msg}")

    def num_records_query(self) -> str:
        query = self.engine.num_records_query(
            table_config=self.table_config, table_index=self.table_index
        )
        if self.engine.debug or self.debug:
            self.info(query)
        return query

    def extract_query(self, start_indx: int) -> str:
        query = self.engine.extract_query(
            table_config=self.table_config, start_indx=start_indx, table_index=self.table_index
        )
        if self.engine.debug or self.debug:
            self.info(query)
        return query

    def fetch_num_records(self) -> Dict:
        records, *order_range = self.engine.fetch_one(self.num_records_query())
        return {
            "records": records,
            "columns": {
                col: {
                    "min": parse_value(val=min_max[0], dtype=dtype),
                    "max": parse_value(val=min_max[1], dtype=dtype)
                }
                for (col, dtype), min_max
                in zip(self.table_config.order_by_columns.items(), list(chunks(order_range)))
            }}

    def fetch_extract_batch(self, start_indx: int) -> List[Dict]:
        rows = self.engine.fetch_all(self.extract_query(start_indx=start_indx))
        if len(rows) > 0:
            return json.loads(''.join([row[0] for row in rows]))
        return []

    def __str__(self) -> str:
        return f"{str(self.engine)}"
