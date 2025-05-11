from yadet.objects.base import BaseObject

from typing import Dict


class TableConfig(BaseObject):
    
    def __init__(self, 
                 ordinal: int, 
                 table_name: str,
                 delta: bool,
                 order_by_columns: Dict[str, str],
                 table_alias: str = None,
                 output_table_name: str = None,
                 columns: str = "*",
                 filter_clause: str = None,
                 join_clause: str = None,
                 flat: bool = True,
                 batch_size: int = 5000,
                 min_wait: int = None,
                 active: bool = True,
                 desc: str = None):
        self.ordinal: int = ordinal
        self.table_name: str = table_name
        self.delta: bool = delta
        self.order_by_columns: Dict[str, str] = order_by_columns
        self.table_alias: str = table_alias
        self.output_table_name: str = output_table_name
        self.columns: str = columns
        self.filter_clause: str = filter_clause
        self.join_clause: str = join_clause
        self.flat: bool = flat
        self.batch_size: int = batch_size
        self.min_wait: int = min_wait
        self.active: bool = active
        self.desc: str = desc

        self.validate()

    def validate(self):
        # TODO: Validate structure of elements
        # TODO: Validate Order by Columns
        ...

    @property
    def get_table_alias(self) -> str:
        return self.table_alias or self.table_name

    @property
    def get_output_table_name(self) -> str:
        return self.output_table_name or self.get_table_alias

    @property
    def data(self) -> Dict:
        return {
            "ordinal": self.ordinal,
            "table_name": self.table_name,
            "delta": self.delta,
            "order_by_columns": self.order_by_columns,
            "table_alias": self.table_alias,
            "output_table_name": self.output_table_name,
            "columns": self.columns,
            "filter_clause": self.filter_clause,
            "join_clause": self.join_clause,
            "flat": self.flat,
            "batch_size": self.batch_size,
            "min_wait": self.min_wait,
            "active": self.active,
            "desc": self.desc,
        }
        
    def __str__(self) -> str:
        return f"{str(self.table_alias)}: {self.ordinal}"