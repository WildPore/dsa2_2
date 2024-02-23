import copy
from city import City
from math import inf


class Truck:
    def __init__(self, id: int, packages: list, city: City, start_time: float) -> None:
        self.id = id

        self.packages = packages
        self.delivered_packages: list = []
        self.undelivered_packages = copy.deepcopy(self.packages)
        for pkg in self.undelivered_packages:
            pkg["delivery_status"] = "En route"

        self.city = city
        self.start_time = start_time
        self.time = start_time

        self.speed: float = 18.0
        self.location: int = 0
        self.index: int = 1
        self.route: list = self.find_route()
        self.route_length: float = self.get_route_length()
        self.destinations: set = self.get_delivery_nodes()
        self.distance_travelled: float = 0.0

    def reset(self):
        """
        Resets the truck back to its initial starting position, time, and status.
        """

        self.location = 0
        self.distance_travelled = 0.0
        self.delivered_packages = []
        self.undelivered_packages = copy.deepcopy(self.packages)
        for pkg in self.undelivered_packages:
            pkg["delivery_status"] = "En route"
        self.time = self.start_time
        self.index = 1

    def _finished_route(self) -> bool:
        """
        Determines if the route has been completed. If the index is equal to the length of the route, then all nodes have been visited.
        """

        return len(self.route) == self.index

    def get_packages(self) -> list:
        """
        Returns all the packages currently loaded on the truck.
        """

        return self.delivered_packages + self.undelivered_packages

    def get_route_length(self) -> float:
        route = self.find_route()
        return self.city.route_length(route)

    def move_to(self, node: int) -> None:
        """
        Moves to a specific node and appropriately increases miles travelled and other stats.
        """

        self.distance_travelled += self.city.distance_between(self.location, node)
        self.time = (
            self.city._convert_miles_to_minutes(self.distance_travelled)
            + self.start_time
        )
        self.location = node

    def move_to_address(self, address: str) -> None:
        node = self.city.address_to_node(address)
        self.move_to(node)

    def packages_at_location(self) -> list | None:
        """
        Returns a list of packages for undelivered packages at the current location.

        If there are no packages at the current location, returns None.
        """

        pkgs = []

        for pkg in self.undelivered_packages:
            if self.city.address_to_node(pkg["address"]) == self.location:
                pkgs.append(pkg)

        if pkgs == []:
            return None

        return pkgs

    def deliver(self) -> None:
        """
        Delivers packages at the current location.

        This method updates the delivery status of each package at the current location to "Delivered at {current_time}".
        It then moves the delivered packages from the undelivered_packages list to the delivered_packages list.

        Returns:
            None
        """

        pkgs_to_deliver = self.packages_at_location()

        if pkgs_to_deliver:
            for pkg in pkgs_to_deliver:
                pkg["delivery_status"] = f"Delivered at {formattime(self.time)}"
                self.delivered_packages.append(pkg)
                self.undelivered_packages.remove(pkg)

    def get_delivery_nodes(self) -> set:
        """
        Returns a set of all of the nodes that the truck must visit in order to deliver all of its packages.
        """

        nodes = set()
        for package in self.packages:
            nodes.add(self.city.address_to_node(package["address"]))
        return nodes

    def get_delivered_package_ids(self) -> list:
        """
        Returns a list of the delivered packages' IDs.
        """

        return [pkg["id"] for pkg in self.delivered_packages]

    def _nearest_neighbor(self, destinations: list) -> int:
        """
        Returns the int representing the nearest node to the truck's current location.

        Takes a list representing possible destinations that route requires.
        """

        nearest = None
        min_distance = inf

        for destination in destinations:
            distance = self.city[self.location][destination]
            if distance < min_distance:
                min_distance = distance
                nearest = destination

        return nearest

    def find_route(self) -> list:
        """
        Given the packages, find a route that delivers all of the packages while respecting constriants.
        """

        route = [0]
        destinations = self.get_delivery_nodes()
        while destinations:
            nearest = self._nearest_neighbor(destinations)
            destinations.remove(nearest)
            route.append(nearest)
            self.location = nearest
        route.append(0)  # return to hub after deliveries are completed

        return route

    def next(self) -> None:
        """
        This function calls other functions to simulate the truck driving to the next location, delivering the appropriate package, and then updating the route to account for the visited node.
        """

        if self.route == []:
            self.find_route()

        if self._finished_route():
            return

        self.move_to(self.route[self.index])
        self.index += 1
        self.deliver()

    def status_at_time(self, time: float) -> str:
        """
        Returns a formatted string that displays the projected status of a truck at the specified time.
        """

        output = ["\n", ""]

        if time <= 620.0:
            for pkg in self.undelivered_packages:
                if pkg["id"] == 9:
                    pkg["address"] = "300 State St"

        if time < self.start_time:
            output[1] = f"Truck {self.id} has not left the depot."
            for pkg in self.undelivered_packages:
                output.append(f"\t{formatpkg(pkg)}")
            return output

        while self.time < time:
            self.next()
            if self._finished_route():
                output.append(f"{formattime(self.time)}, returned to depot.")
                break
        for pkg in self.undelivered_packages + self.delivered_packages:
            output.append(f"\t{formatpkg(pkg)}")

        output[1] = f"Truck {self.id}: {round(self.distance_travelled, 2)} miles"
        return output


def formattime(minutes: float) -> str:
    minutes = int(minutes)  # Convert minutes to an integer
    hours, minutes = divmod(minutes, 60)

    am_pm = "am" if hours < 12 else "pm"

    while 12 <= hours:
        hours -= 12

    if hours == 0:
        hours = 12

    formatted_time = f"{hours}:{minutes:02d} {am_pm}"
    return formatted_time


def formatpkg(pkg) -> str:
    return f"Package #{pkg["id"]}, deadline: {formattime(pkg["deadline"])}, status: [{pkg["delivery_status"]}], destination: [{pkg["address"]}, {pkg["city"]} {pkg["state"]} {pkg["zipcode"]}], weight: {pkg["weight"]}kg, notes: \"{pkg["notes"]}\""
