from typing import Any, Iterator, List, Tuple

from custom_types import Bucket, HashTableStructure, KeyValuePair


class HashTable:
    """
    A hash table implementation in Python.

    Attributes:
        size (int): The size of the hash table.
        _table (HashTableStructure): The underlying data structure for the hash table.

    Methods:
        __init__(self, size: int = 10) -> None: Initializes a new instance of the HashTable class.
        __iter__(self) -> Iterator[Bucket]: Returns an iterator over the hash table.
        __contains__(self, key: Any) -> bool: Checks if a key is present in the hash table.
        __len__(self) -> int: Returns the number of elements in the hash table.
        __getitem__(self, key: Any) -> Any: Retrieves the value associated with a key.
        __setitem__(self, key: Any, value: Any) -> None: Sets the value associated with a key.
        __delitem__(self, key: Any) -> None: Deletes the key-value pair from the hash table.
        __str__(self) -> str: Returns a string representation of the hash table.
        _hash(self, key: Any) -> int: Computes the hash value for a key.
        _resize(self) -> None: Resizes the hash table when it reaches its load factor.
        _get(self, key: Any, default: Any = None) -> Any: Retrieves the value associated with a key, with an optional default value.
        _set(self, key: Any, value: Any) -> None: Sets the value associated with a key.
        _del(self, key: Any) -> None: Deletes the key-value pair from the hash table.
        keys(self) -> List[Any]: Returns a list of all keys in the hash table.
        values(self) -> List[Any]: Returns a list of all values in the hash table.
        zip(self) -> Iterator[Tuple[Any, Any]]: Returns an iterator over key-value pairs in the hash table.
    """

    def __init__(self, size: int = 10) -> None:
        """
        Initializes a new instance of the HashTable class.

        Args:
            size (int): The size of the hash table.

        Returns:
            None
        """
        self.size: int = size
        self._table: HashTableStructure = [[] for _ in range(self.size)]

    def __iter__(self) -> Iterator[Bucket]:
        """
        Returns an iterator over the hash table.

        Yields:
            Bucket: The next bucket in the hash table.
        """
        for entry in self._table:
            yield entry

    def __contains__(self, key: Any) -> bool:
        """
        Checks if the hash table contains a specific key.

        Args:
            key (Any): The key to search for in the hash table.

        Returns:
            bool: True if the key is found, False otherwise.
        """
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
        result = "\n".join(
            f"{pair.key}: {{{self._format_value(pair.value)}}}"
            for bucket in self._table
            for pair in bucket
        )
        return result

    def _format_value(self, value: Any, indent: int = 0) -> str:
        """
        Formats the given value as a string representation with optional indentation.

        Args:
            value (Any): The value to be formatted.
            indent (int, optional): The number of spaces for indentation. Defaults to 0.

        Returns:
            str: The formatted string representation of the value.
        """
        if isinstance(value, HashTable):
            nested_indent = indent + 4
            nested_result = "\n".join(
                f"{' ' * nested_indent}{nested_key}: {{{self._format_value(nested_value, nested_indent)}}}"
                for nested_key, nested_value in value.zip()
            )
            return f"\n{' ' * indent}{{\n{nested_result}\n{' ' * indent}}}"
        else:
            return str(value)

    def _hash(self, key: Any) -> int:
        """
        Hashes the given key using the built-in hash function and returns the hash value modulo the size of the hash table.

        Args:
            key (Any): The key to be hashed.

        Returns:
            int: The hash value of the key modulo the size of the hash table.
        """
        return hash(key) % self.size

    def _resize(self) -> None:
        """
        Resizes the hash table by doubling its size and rehashing all the elements.
        This method is called when the load factor exceeds a certain threshold.

        Returns:
            None
        """
        self.size *= 2
        new_table: List[List[Tuple[Any, Any]]] = [None] * self.size
        for i in range(len(self._table)):
            new_table[i] = self._table[i]
        self._table = new_table

    def _get(self, key: Any, default: Any = None) -> Any:
        """
        Retrieves the value associated with the given key from the hash table.

        Args:
            key (Any): The key to search for in the hash table.
            default (Any, optional): The value to return if the key is not found. Defaults to None.

        Returns:
            Any: The value associated with the key if found, otherwise the default value.
        """
        index = self._hash(key)
        bucket = self._table[index]
        for pair in bucket:
            if pair.key == key:
                return pair.value
        return default

    def _set(self, key: Any, value: Any) -> None:
        """
        Sets the value associated with the given key in the hash table.

        Args:
            key (Any): The key to set the value for.
            value (Any): The value to be associated with the key.

        Returns:
            None
        """
        index = self._hash(key)
        bucket = self._table[index]
        for i, pair in enumerate(bucket):
            if pair.key == key:
                bucket[i] = KeyValuePair(key, value)
                return
        bucket.append(KeyValuePair(key, value))

    def _del(self, key: Any) -> None:
        """
        Deletes the key-value pair with the given key from the hash table.

        Args:
            key (Any): The key of the key-value pair to be deleted.

        Raises:
            KeyError: If the key is not found in the hash table.

        Returns:
            None
        """
        index = self._hash(key)
        bucket = self._table[index]
        for i, pair in enumerate(bucket):
            if pair.key == key:
                del bucket[i]
                return
        raise KeyError("Key not found.")

    def keys(self) -> List[Any]:
        """
        Returns a list of all keys in the hash table.

        Returns:
            List[Any]: A list containing all the keys in the hash table.
        """
        key_list = []
        for bucket in self._table:
            for item in bucket:
                key_list.append(item[0])
        return key_list

    def values(self) -> List[Any]:
        """
        Returns a list of all values stored in the hash table.

        This method iterates over each bucket in the hash table and retrieves
        the value of each entry. The values are then collected into a list and
        returned.

        Returns:
            A list of all values stored in the hash table.
        """
        return [entry.value for bucket in self._table for entry in bucket]

    def zip(self) -> Iterator[Tuple[Any, Any]]:
        """
        Returns an iterator that combines the keys and values of the hash table.

        Returns:
            An iterator that yields tuples of (key, value) pairs from the hash table.
        """
        return zip(self.keys(), self.values())
