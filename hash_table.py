from typing import Any, Iterator, List, Tuple

from custom_types import Bucket, HashTableStructure, KeyValuePair


class HashTable:
    def __init__(self, size: int = 10) -> None:
        self.size: int = size
        self._table: HashTableStructure = [[] for _ in range(self.size)]

    def __iter__(self) -> Iterator[Bucket]:
        for entry in self._table:
            yield entry

    def __contains__(self, key: Any) -> bool:
        index = self._hash(key)
        bucket = self._table[index]
        return any(pair.key == key for pair in bucket)

    def __len__(self) -> int:
        return len(self._table)

    def __getitem__(self, key: Any) -> Any:
        return self._get(key, default=None)

    def __setitem__(self, key: Any, value: Any) -> None:
        self._set(key, value)

    def __delitem__(self, key: Any) -> None:
        self._del(key)

    def __str__(self) -> str:
        def format_value(value: Any, indent: int = 0) -> str:
            if isinstance(value, HashTable):
                nested_indent = indent + 4
                nested_result = ""
                for i, (nested_key, nested_value) in enumerate(value.zip()):
                    if i == 0:
                        nested_result += f"\n{' ' * nested_indent}{nested_key}: {{{format_value(nested_value, nested_indent)}}}\n"
                    else:
                        nested_result += f"{' ' * nested_indent}{nested_key}: {{{format_value(nested_value, nested_indent)}}}\n"
                return nested_result
            else:
                return str(value)

        result = ""
        for bucket in self._table:
            for pair in bucket:
                result += f"{pair.key}: {{{format_value(pair.value)}}}\n"
        return result

    def _hash(self, key: Any) -> int:
        return hash(key) % self.size

    def _resize(self) -> None:
        self.size *= 2
        new_table: List[List[Tuple[Any, Any]]] = [None] * self.size
        for i in range(len(self._table)):
            new_table[i] = self._table[i]
        self._table = new_table

    def _get(self, key: Any, default: Any = None) -> Any:
        index = self._hash(key)
        bucket = self._table[index]
        for pair in bucket:
            if pair.key == key:
                return pair.value
        return default

    def _set(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        bucket = self._table[index]
        for i, pair in enumerate(bucket):
            if pair.key == key:
                bucket[i] = KeyValuePair(key, value)
                return
        bucket.append(KeyValuePair(key, value))

    def _del(self, key: Any) -> None:
        index = self._hash(key)
        bucket = self._table[index]
        for i, pair in enumerate(bucket):
            if pair.key == key:
                del bucket[i]
                return
        raise KeyError("Key not found.")

    def keys(self) -> List[Any]:
        key_list = []
        for bucket in self._table:
            for item in bucket:
                key_list.append(item[0])
        return key_list

    def values(self) -> List[Any]:
        return [entry.value for bucket in self._table for entry in bucket]

    def zip(self) -> Iterator[Tuple[Any, Any]]:
        return zip(self.keys(), self.values())
