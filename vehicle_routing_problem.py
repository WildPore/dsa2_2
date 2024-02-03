from city import City
from genetic_algorithm import Chromosome
from packages import Packages


def extract_destinations(packages: Packages, city: City) -> set:
    destinations = set()
    for package_id in packages.keys():
        package = packages[package_id]
        address = package["address"]
        destinations.add(city.address_to_node(address))

    return destinations


packages = Packages("packages.csv")
city = City("distances.csv")

destinations = list(extract_destinations)

alloc_chm = Chromosome(alphabet=destinations)
alloc_chm.generate_individual(10)

print(extract_destinations(packages, city))
