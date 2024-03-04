import csv
import operator
from datetime import datetime, timedelta
from itertools import accumulate
from typing import Iterable

from packages import Packages


class City:
    """
    Represents a city with nodes and an adjacency matrix.

    Attributes:
        nodes (list): A list of node indices.
        adjacency_matrix (list): A 2D list representing the adjacency matrix.

    Methods:
        __init__(self, adj_mat_fp: str) -> None:
            Initializes the graph given an adjacency matrix file path.
        __iter__(self) -> Iterable:
            Returns an iterator for the adjacency matrix.
        __getitem__(self, key) -> list:
            Returns the adjacency matrix for a given node index.
        _load(self, filename: str) -> None:
            Loads the adjacency matrix from a file.
        __str__(self) -> str:
            Returns a string representation of the adjacency matrix.
        address_to_node(self, address: str) -> int:
            Converts an address to its corresponding node index.
        node_to_address(self, node: int) -> str:
            Converts a node number to its corresponding address.
    """

    def __init__(self, adj_mat_fp: str) -> None:
        """
        Initializes the graph given a adjacency matrix file path.

        Args:
            adj_mat_fp (str): The file path of the adjacency matrix.
        """

        self.nodes = []
        self.adjacency_matrix = []
        self._load(adj_mat_fp)

        pass

    def __iter__(self) -> Iterable:
        return iter(self.adjacency_matrix)

    def __getitem__(self, key) -> list:
        if key not in self.nodes:
            raise KeyError(key)
        else:
            return self.adjacency_matrix[key]

    def _load(self, filename: str) -> None:
        """
        Loads the adjacency matrix from a file.

        Args:
            filename (str): The file path of the adjacency matrix.
        """

        with open(file=filename, mode="r", newline="", encoding="utf-8-sig") as file:
            csv_reader = csv.reader(file, delimiter=",")

            for current_row_index, row in enumerate(csv_reader):
                self.nodes.append(current_row_index)
                current_row_index += 1
                self.adjacency_matrix.append(
                    [float(_) if _ != "" else 0.0 for _ in row]
                )

        for i in range(len(self.nodes)):
            for j in range(i, len(self.adjacency_matrix[i])):
                self.adjacency_matrix[i][j] = self.adjacency_matrix[j][i]

    def __str__(self) -> str:
        return "\n".join([str(_) for _ in self.adjacency_matrix])

    def _convert_miles_to_minutes(self, miles: float) -> float:
        # Would require a rework if the MPH of a truck could change.
        MPH = 18.0
        MINUTES = 60.0
        return miles / MPH * MINUTES

    def address_to_node(self, address: str) -> int:
        """
        Converts an address to its corresponding node index.

        Args:
            address (str): The address to convert.

        Returns:
            int: The node index corresponding to the address.

        Raises:
            KeyError: If the address is not found in the locations dictionary.
        """

        locations = {
            "4001 South 700 East": 0,
            "1060 Dalton Ave S": 1,
            "1330 2100 S": 2,
            "1488 4800 S": 3,
            "177 W Price Ave": 4,
            "195 W Oakland Ave": 5,
            "2010 W 500 S": 6,
            "2300 Parkway Blvd": 7,
            "233 Canyon Rd": 8,
            "2530 S 500 E": 9,
            "2600 Taylorsville Blvd": 10,
            "2835 Main St": 11,
            "300 State St": 12,
            "3060 Lester St": 13,
            "3148 S 1100 W": 14,
            "3365 S 900 W": 15,
            "3575 W Valley Central Station bus Loop": 16,
            "3595 Main St": 17,
            "380 W 2880 S": 18,
            "410 S State St": 19,
            "4300 S 1300 E": 20,
            "4580 S 2300 E": 21,
            "5025 State St": 22,
            "5100 South 2700 West": 23,
            "5383 S 900 East #104": 24,
            "600 E 900 South": 25,
            "6351 South 900 East": 26,
        }

        if address not in locations:
            raise KeyError(address)

        return locations[address]

    def node_to_address(self, node: int) -> str:
        """
        Converts a node number to its corresponding address.

        Args:
            node (int): The node number.

        Returns:
            str: The address corresponding to the given node number.

        Raises:
            KeyError: If the address is not found in the locations dictionary.
        """

        locations = {
            0: "4001 South 700 East",
            1: "1060 Dalton Ave S",
            2: "1330 2100 S",
            3: "1488 4800 S",
            4: "177 W Price Ave",
            5: "195 W Oakland Ave",
            6: "2010 W 500 S",
            7: "2300 Parkway Blvd",
            8: "233 Canyon Rd",
            9: "2530 S 500 E",
            10: "2600 Taylorsville Blvd",
            11: "2835 Main St",
            12: "300 State St",
            13: "3060 Lester St",
            14: "3148 S 1100 W",
            15: "3365 S 900 W",
            16: "3575 W Valley Central Station bus Loop",
            17: "3595 Main St",
            18: "380 W 2880 S",
            19: "410 S State St",
            20: "4300 S 1300 E",
            21: "4580 S 2300 E",
            22: "5025 State St",
            23: "5100 South 2700 West",
            24: "5383 S 900 East #104",
            25: "600 E 900 South",
            26: "6351 South 900 East",
        }

        if node not in locations:
            raise KeyError(node)

        return locations[node]

    def distance_between(self, a: int, b: int) -> float:
        return self.adjacency_matrix[a][b]

    def route_length(self, route: list) -> float:
        total_length = 0.0
        for i in range(len(route) - 1):
            a = route[i]
            b = route[i + 1]
            distance = self.distance_between(a, b)
            total_length += distance
        return total_length

    def distances(self, route: list) -> list:
        distances = []
        for i in range(1, len(route)):
            a = route[i - 1]
            b = route[i]
            distance = self.distance_between(a, b)
            distances.append(distance)
        return distances

    def cumulative_distances(self, route: list) -> list:
        return list(accumulate(self.distances(route), operator.add))

    def time_at_each_stop(self, route: list, time_offset: float = 480.0) -> list:
        times = [
            self._convert_miles_to_minutes(_) + time_offset
            for _ in self.cumulative_distances(route)
        ]
        return times

    def cumulative_times(
        self, route: list, start_time: datetime.time, speed: float = 18.0
    ) -> list:
        now = datetime.now()
        start_datetime = datetime.combine(now.date(), start_time)
        distances = self.distances(route)

        time_for_each_leg = [
            timedelta(hours=distance / speed) for distance in distances
        ]

        cumulative_times = [start_datetime]
        for time in time_for_each_leg:
            new_time = cumulative_times[-1] + time
            cumulative_times.append(new_time)

        return [time.time() for time in cumulative_times]

    def route_is_on_time(
        self, route: list, packages: Packages, time_offset: float = 480.0
    ) -> bool:
        times = self.time_at_each_stop(route, time_offset)
        for i in range(len(route) - 1):
            current_stop = route[i]
            for package in packages:
                current_package_address = package["address"]
                current_package_node = self.address_to_node(current_package_address)

                if current_package_node == current_stop:
                    current_package_deadline = package["deadline"]
                    if current_package_deadline < times[i]:
                        return False
        return True
