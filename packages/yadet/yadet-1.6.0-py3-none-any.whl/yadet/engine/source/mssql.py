from yadet.config.table import TableConfig
from yadet.engine.source.base import SourceMssqlEngine, SourceEngine
from yadet.helpers.parser import parse_value
from yadet.helpers.sql import clean_sql

import pyodbc
from typing import Any, Dict


class MsSqlSourceEngine(SourceEngine):

    def __init__(self, connection_str: str, debug: bool = False):
        super().__init__(vendor=SourceMssqlEngine, debug=debug)
        self._connection_str: str = connection_str
        self._conn: pyodbc.Connection = None
        
        self.connect()

    def connect(self):
        self._conn: pyodbc.Connection = pyodbc.connect(self._connection_str)

    def fetch_one(self, sql: str) -> Any:
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    def fetch_all(self, sql: str) -> Any:
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
            
    def where_clause(self, table_config: TableConfig, table_index: Dict) -> str:
        if not table_config.delta:
            return "" if table_config.filter_clause is None else f"WHERE {table_config.filter_clause}"
        
        where_clause = ""
        index_where_clause = ""
        if table_index:
            index_where_clause = " AND ".join([
                f"{field} > '{parse_value(val=table_index['columns'][field]['max'], dtype=dtype)}'" 
                for field, dtype in table_config.order_by_columns.items()
                if table_index.get("columns", {}).get(field, {}).get("max") is not None
            ])
        
        if table_config.filter_clause is not None:
            where_clause = f"WHERE {table_config.filter_clause}"
            if index_where_clause not in (None, ""):
                where_clause += f" AND {index_where_clause}"
        
        elif index_where_clause not in (None, ""):
            where_clause = f"WHERE {index_where_clause}"

        return where_clause

    def order_by_clause(self, table_config: TableConfig) -> str:
        order_by_field_clause = ", ".join([
            f"{field} ASC" for field in table_config.order_by_columns.keys()
        ])
        return f"ORDER BY {order_by_field_clause}"

    def join_clause(self, table_config: TableConfig) -> str:
        return "" if table_config.join_clause is None else table_config.join_clause

    def num_records_query(self, table_config: TableConfig, table_index: Dict) -> str:
        # Get Number of Records, Min, Max Value
        min_max_fields = ", ".join([
            f"{func}({field}) AS '{indx}__{func.lower()}'"
            for indx, field in enumerate(table_config.order_by_columns.keys())
            for func in ("MIN", "MAX")
        ])
        
        # Table Alias
        table_alias = "" if table_config.table_alias is None else f"AS {table_config.table_alias}"
        
        # SQL
        sql = f"""SELECT COUNT(*) AS num_records, {min_max_fields} FROM \
                    {table_config.table_name} {table_alias} {self.join_clause(table_config=table_config)} \
                    {self.where_clause(table_config=table_config, table_index=table_index)}"""
        return clean_sql(sql=sql)

    def extract_query(self, table_config: TableConfig, start_indx: int, table_index: Dict) -> str:
        # Table Alias
        table_alias = "" if table_config.table_alias is None else f"AS {table_config.table_alias}"
        
        base_sql = f"""
        SELECT {table_config.columns} 
        FROM {table_config.table_name} {table_alias} 
        {self.join_clause(table_config=table_config)}
        {self.where_clause(table_config=table_config, table_index=table_index)}
        {self.order_by_clause(table_config=table_config)}
        OFFSET {start_indx} ROWS
        FETCH NEXT {table_config.batch_size} ROWS ONLY
        """
        if table_config.flat:
            base_sql = f"WITH base_cte as ({base_sql}) SELECT * FROM base_cte"

        sql = f"{base_sql} FOR JSON AUTO;"
        return clean_sql(sql=sql)
