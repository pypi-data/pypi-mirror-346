from typing import Dict


__all__ = [
    "assemble_url",
]


def assemble_url(base_url: str, params: Dict) -> str:
    """"""
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    request_url = f"{base_url}?{query_string}"
    return request_url
