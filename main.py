# Student ID: 011651581

from city import City
from datetime import datetime
from packages import Packages
from truck import Truck

# These are the base data structures that are used to drive the projects behavior.
city = City(adj_mat_fp="distances.csv")
packages = Packages(fname="packages.csv")


# Manually loading the packages onto the trucks.
manifest1 = [1, 13, 15, 30, 29, 31, 34, 37, 40, 19, 14, 16, 20]
manifest2 = [3, 18, 36, 38, 6, 25, 28, 32, 35, 39, 26, 27, 24]
manifest3 = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 33]


def get_packages(manifest):
    """
    Converts a manifest (list of integers) to a list of package objects.
    """
    selected_packages = []
    for id in manifest:
        selected_packages.append(packages[id])
    return selected_packages


# The individual trucks are initialized.
truck1 = Truck(1, get_packages(manifest1), city, 480.0)  # starts at 8am
truck2 = Truck(2, get_packages(manifest2), city, 545.0)  # starts at 9:05am
truck3 = Truck(3, get_packages(manifest3), city, 620.0)  # starts at 10:20am

# The find_route method sets the value of the internal route variable for each truck.
t1r = truck1.find_route()
t2r = truck2.find_route()
t3r = truck3.find_route()


def time_str_to_float(time_str):
    """
    Converts a string containing a time formatted like HH:MM am/pm and converts it to a float that represents the number of minutes since the start of the day.
    """
    time = datetime.strptime(time_str, "%I:%M %p").time()
    return time.hour * 60.0 + time.minute


def parse_schedule_command(command):
    """
    Takes a schedule command and returns the arguments.
    """
    command_parts = command.split()
    if len(command_parts) == 4 and command_parts[0] == "schedule":
        start_time = datetime.strptime(
            command_parts[1] + " " + command_parts[2], "%I:%M %p"
        )
        end_time = datetime.strptime(
            command_parts[3] + " " + command_parts[4], "%I:%M %p"
        )
        return start_time, end_time
    else:
        return None, None


def parse(input_str):
    """
    Takes input from the command line interface and returns the appropriate response.

    If the command is quit, then the function returns None, which causes the while loop driving the command line to break, quitting the program.

    If the command is schedule, and there are arguments, then the arguments are converted to floats to be used to drive the status_at_time method from the truck objects.

    If the command is schedule and there are no arguments, then a default time of 1439 (11:59 pm) is used.

    If the command is miles, then the function returns the sum of the total length of todays truck routes in miles.
    """

    parts = input_str.split()
    if not parts:
        return f"{input_str} not recognized. Please check your spelling and try again."

    cmd = parts[0]

    if cmd == "quit":
        return None
    if cmd == "schedule" and 1 < len(parts):
        arg = time_str_to_float(" ".join(parts[1:]))
        return "\n".join(
            truck1.status_at_time(arg)
            + truck2.status_at_time(arg)
            + truck3.status_at_time(arg)
        )
    if cmd == "schedule":
        return "\n".join(
            truck1.status_at_time(1439)
            + truck2.status_at_time(1439)
            + truck3.status_at_time(1439)
        )
    if cmd == "miles":
        return f"Today's route is {round(sum([truck.route_length for truck in [truck1, truck2, truck3]]), 2)} miles long."


# There's some kind "it doesn't work on my machine" bug that requires a variable be set, instead of just using "while True:"
b = True
print(
    "Commands:\n[miles] to view the total miles of the current scheduled routes.\n[schedule] to view the schedule.\n[schedule HH:MM am/pm] (ex: schedule 10:00 am) to view the schedule up to a given time.\n[quit] to quit."
)
while b:
    """
    The main loop of the program and its interface.
    
    The reset method is called after every command, otherwise previous commands would effect the current command. 
    """
    i = input("\nType the command and press enter.\n")

    o = parse(i)
    if o:
        print(o)
        truck1.reset()
        truck2.reset()
        truck3.reset()
    else:
        break
