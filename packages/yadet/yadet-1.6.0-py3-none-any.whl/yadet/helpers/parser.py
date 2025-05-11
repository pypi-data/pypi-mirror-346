from dateutil.parser import parse as date_parse
from typing import Any


def parse_value(val: str, dtype: str) -> Any:
    if val is None:
        return None
    
    val = str(val)
    if dtype == "str":
        return str(dtype)

    if dtype == "int":
        return int(val)

    if dtype == "date":
        return date_parse(val).strftime("%Y-%d-%m")

    if dtype == "datetime":
        return date_parse(val).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    raise NotImplementedError(f"dtype {dtype} not implemented")
