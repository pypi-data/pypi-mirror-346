import re


def clean_sql(sql: str) -> str:
    return re.sub("\s+", " ", sql).strip()
