from typing import Any, NamedTuple, List


class KeyValuePair(NamedTuple):
    key: Any
    value: Any


Bucket = List[KeyValuePair]
HashTableStructure = List[Bucket]
