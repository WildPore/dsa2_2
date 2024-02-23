import csv
import re
from datetime import datetime
from hash_table import HashTable


class Packages(HashTable):
    """
    Extends the HashTable class with the package specific information.
    """

    def __init__(self, fname: str) -> None:
        packages_size = 40  # Since there are 40 packages, just hardcode it.
        super().__init__(packages_size)

        self._load(fname)

    def _load(self, fname: str) -> None:
        """
        Loads the file from fname.

        This function assumes a very specific formatting for the CSV.
        """
        with open(file=fname, mode="r", newline="", encoding="utf-8-sig") as file:
            csv_reader = csv.reader(file, delimiter=",")
            for row in csv_reader:
                package = HashTable()
                package["id"] = int(row[0])
                package["address"] = row[1]
                package["city"] = row[2]
                package["state"] = row[3]
                package["zipcode"] = row[4]
                package["deadline"] = self._convert_deadline(row[5])
                package["weight"] = float(row[6])
                package["notes"] = row[7]
                package["delivery_status"] = "At the hub"

                package["earliest_availability"] = self._available(row[7])
                package["required_truck"] = self._truck(row[7])
                package["dependencies"] = self._dependencies(row[7])

                self[int(row[0])] = package

    def _convert_deadline(self, deadline: str) -> float:
        """
        Extracts the deadline from the field, converting it to a float representing the minutes passed since the start of the day.
        """
        if "EOD" in deadline:
            return 1439.0
        else:
            time = datetime.strptime(deadline, "%I:%M %p").time()
            return time.hour * 60.0 + time.minute

    def _available(self, notes: str) -> float:
        """
        Extracts the earliest time available from the notes field and returns a float representing the minutes passed since the start of the day.
        """
        if "Available " in notes:
            time = notes.split("Available ")[1]
            time = datetime.strptime(time, "%I:%M %p").time()
            return time.hour * 60 + time.minute
        else:
            return 0.0

    def _truck(self, notes: str) -> int:
        """
        Extracts the truck constraint from the notes field and returns the truck ID as an integer.

        Since there is only a constraint for Truck 2 in the dataset, this function has been hardcoded to check
        for Truck 2.
        """
        if "Truck 2" in notes:
            return 2
        else:
            return 0

    def _dependencies(self, notes: str) -> list:
        """
        Extracts dependent packages (packages that must ride with other packages) from the notes section.

        Returns a list of integers containing the package IDs.
        """
        if "Must be delivered with " in notes:
            ints = re.findall(r"\d+", notes)
            return [int(i) for i in ints]
        else:
            return None

    def select_all(self, key: int | str) -> list:
        """
        Returns all the values associated with that key, does not return values that are none or empty.
        """
        return sorted(
            [
                package
                for package in self.values()
                if package[key] is not None and package[key] != ""
            ],
            key=lambda package: package[key],
        )

    def format(self, pkg_id: int) -> str:
        pkg = self.packages[pkg_id]
        return f"Package #{pkg_id}, status: [{pkg["delivery_status"]}], destination: [{pkg["address"]}, {pkg["city"]} {pkg["state"]} {pkg["zipcode"]}], weight: {pkg["weight"]}kg, notes: \"{pkg["notes"]}\""
