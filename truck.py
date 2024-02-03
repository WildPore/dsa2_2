# from typing import TYPE_CHECKING
from city import City
# from packages import Packages

# if TYPE_CHECKING:
#     from city import Graph
#     from packages import Packages


class Truck:
    location: int = 0
    distance_travelled: float = 0.0
    delivered_packages: list = []

    def __init__(self, id: int, packages: list, city: City, start_time: float) -> None:
        self.id = id
        self.packages = packages
        self.city = city
        self.start_time = start_time

    def move_to(self, node: int) -> None:
        """
        Moves to a specific node and appropriately increases miles travelled and other stats.
        """

        self.distance_travelled += self.city.distance_between(self.location, node)
        self.location = node

    def move_to_address(self, address: str) -> None:
        node = self.city.address_to_node(address)
        self.move_to(node)

    def deliver(self, package_id: int) -> None:
        """
        Attempts to deliver a package to the current location if possible.

        Fails silently if there is no package in the vehicle's inventory matching the package_id.
        """

        if self.location == 0:
            return

        for package in self.packages:
            if package["id"] == package_id and package["destination"] == self.location:
                self.delivered_packages.append(package)
                self.packages.remove(package)

    def get_delivery_nodes(self) -> list:
        nodes = set()
        for package in self.packages:
            nodes.add(self.city.address_to_node(package["address"]))
        return list(nodes)

    def deliver_nearest_neighbor(self):
        undelivered_packages = {package["id"]: package for package in self.packages}
        current_location = self.location

        while undelivered_packages:
            print(undelivered_packages)
            nearest_package_id, nearest_node = self.find_nearest_package(
                current_location, undelivered_packages
            )

            if nearest_package_id is None:
                break

            self.move_to(nearest_node)
            self.deliver(nearest_package_id)

            del undelivered_packages[nearest_package_id]

            current_location = nearest_node

    def find_nearest_package(
        self, current_location: int, undelivered_packages: dict
    ) -> (int, int):
        nearest_package_id = None
        nearest_node = None
        shortest_distance = float("inf")

        for package_id, package in undelivered_packages.items():
            destination_node = self.city.address_to_node(package["address"])
            distance = self.city.distance_between(current_location, destination_node)

            if distance < shortest_distance:
                shortest_distance = distance
                nearest_package_id = package_id
                nearest_node = destination_node

        return nearest_package_id, nearest_node
