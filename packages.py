import csv
import re
from datetime import datetime
from hash_table import HashTable


class Packages(HashTable):
    def __init__(self, fname: str) -> None:
        packages_size = 40  # Since there are 40 packages, just hardcode it.
        super().__init__(packages_size)

        # Does this execute after super init?
        self._load(fname)

    def _load(self, fname: str):
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

                package["earliest_availability"] = self._available(row[7])
                package["required_truck"] = self._truck(row[7])
                package["dependencies"] = self._dependencies(row[7])
                # print(int(row[0]), package)

                self[int(row[0])] = package

    def _convert_deadline(self, deadline: str) -> float:
        """_summary_

        Args:
            deadline_str (str): _description_

        Returns:
            float: _description_
        """
        if "EOD" in deadline:
            return 1439.0
        else:
            time = datetime.strptime(deadline, "%I:%M %p").time()
            return time.hour * 60.0 + time.minute

    def _available(self, notes: str) -> float:
        if "Available " in notes:
            time = notes.split("Available ")[1]
            time = datetime.strptime(time, "%I:%M %p").time()
            return time.hour * 60 + time.minute
        else:
            return 0.0

    def _truck(self, notes: str) -> int:
        if "Truck 2" in notes:
            return 2
        else:
            return 0

    def _dependencies(self, notes: str) -> list:
        if "Must be delivered with " in notes:
            ints = re.findall(r"\d+", notes)
            return [int(i) for i in ints]
        else:
            return None

    def select_all(self, key) -> list:
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


# packages = Packages(fname="packages.csv")
# for package in packages:
#     print(package[1]["address"])
