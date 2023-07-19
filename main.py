# Sean Kenney
# Student ID: 001041212
# C950 - Data Structures and Algorithms II
# NHP2 Task 1: WGUPS ROUTING PROGRAM

import csv
import datetime
import Trucks
from Packages import Package
from CreateHashTable import CreateHashMap


# distance_between function
# Time Complexity: O(1)
# Input(s): delivery_address1 (address string), delivery_address2 (address string)
# This function determines the distance between two addresses by calling the distance_data table matrix.
# Output(s): distances (float int)
def distance_between(delivery_address1, delivery_address2):
    address1 = convert_address_to_address_id(delivery_address1)
    address2 = convert_address_to_address_id(delivery_address2)
    distances = distance_data[address1][address2]
    # If matrix value is blank, the values will be inverted.
    if distances == "":
        distances = distance_data[address2][address1]
    return float(distances)


# convert_address_to_address_id function
# Time Complexity: O(n) where n is the # of rows within the delivery_address_data list.
# Input(s): address (address string)
# This function determines the address_id by searching the delivery_address_data table with an address string.
# Output(s): address_id (int)
def convert_address_to_address_id(address):
    for field in delivery_address_data:
        if address in field[2]:
            address_id = int(field[0])
            return address_id


# min_distance_address function - Nearest Neighbor Search Algorithm
# Time Complexity: O(n), n is the # of packages in the truck_packages list.
# Input(s): from_address (address string), truck_packages (delivery_truck.truck_packages table)
# This function compares the addresses of the packages within the truck_packages table with the current address
# by calling the distance_between function to determine which package has the shortest distance.
# Output(s): next_address (address string), next_package_id (int), shortest_distance(int)
def min_distance_from_address(from_address, truck_packages):
    shortest_distance = 1000
    next_address = ''
    next_package_id = 0
    for pack in truck_packages:
        package = package_hash_table.look_up(pack)
        add2 = package.package_address
        distance1 = distance_between(from_address, add2)
        if distance1 < shortest_distance:
            shortest_distance = distance1
            next_address = add2
            next_package_id = pack
    return next_address, next_package_id, shortest_distance


# deliver_packages function
# Time Complexity: 0(n^2) where n is the # of undelivered packages in delivery_truck
# Input(s): delivery_truck (int), designated start_time (00:00:00).
# Each package assigned to the delivery_truck.packages table will loop through the min_distance_from_address function
# and calculate the total miles traveled for each package to be delivered. As packages are delivered, they are removed
# from the delivery_truck.packages table until all packages are removed.
# Output(s): miles (total miles traveled for all deliveries)
def deliver_packages(delivery_truck, start_time):
    h, m, s = start_time.split(":")
    package_start_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    current_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    from_address = '4001 South 700 East'
    miles = 0
    for _ in delivery_truck.truck_packages[:]:
        address_visited, id_delivered, distance_traveled = min_distance_from_address(from_address,
                                                                                     delivery_truck.truck_packages)
        miles = miles + distance_traveled
        speed = delivery_truck.truck_speed
        delivery_time = datetime.timedelta(seconds=(distance_traveled / speed * 60 * 60))
        current_time = current_time + delivery_time

        package_delivered = package_hash_table.look_up(id_delivered)
        package_delivered.package_delivery_time = current_time
        package_delivered.package_start_time = package_start_time
        package_delivered.package_delivery_status = 'Delivered'
        from_address = address_visited
        delivery_truck.truck_packages.remove(id_delivered)
    return miles    


# load_package_data function
# Time Complexity: O(n), where n is the # of items in packages_list.
# Input(s): packages (package data), hash_table (package_hash_table object)
# This function loads package data and separates it into individual fields. It then inputs the data
# into the package_hash_table.
def load_package_data(packages_list, hash_table):
    for package in packages_list:
        p_package_id = int(package[0])
        p_package_address = package[1]
        p_package_city = package[2]
        p_package_state = package[3]
        p_package_zip = package[4]
        p_package_deadline = package[5]
        p_package_weight = package[6]
        p_package_notes = package[7]
        p_package_start_time = ""
        p_package_delivery_time = ""
        p_package_delivery_status = "At the Hub"

        # Creates the Package object
        p = Package(p_package_id, p_package_address, p_package_city, p_package_state, p_package_zip,
                    p_package_deadline, p_package_weight, p_package_notes, p_package_start_time,
                    p_package_delivery_time, p_package_delivery_status)

        # Inserts the package object into the Package Hash table
        hash_table.insert(p_package_id, p)


# pre_load_delivery_trucks function
# Time Complexity: O(1)
# this function loads the package_id's into each delivery_truck's truck_packages table.
def preload_delivery_trucks():
    delivery_truck1.truck_packages = [1, 7, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 39, 40]
    delivery_truck2.truck_packages = [3, 4, 5, 6, 17, 18, 23, 24, 25, 26, 36, 38]
    delivery_truck3.truck_packages = [2, 8, 9, 10, 11, 12, 22, 27, 28, 32, 33, 35]


# correct_package_address
# Time Complexity: O(1)
# Input(s): incorrect_package_id (int), corrected_address (string)
# This function is used to update a packages address within the package_hash_table.
# Output(s): None
def update_package_address(incorrect_package_id, corrected_address):
    incorrect_package = package_hash_table.look_up(incorrect_package_id)
    new_address, new_city, new_state, new_zip = corrected_address.split(",")
    incorrect_package.package_address = new_address
    incorrect_package.package_city = new_city
    incorrect_package.package_state = new_state
    incorrect_package.package_zip = new_zip
    incorrect_package.package_notes = "Address Corrected"


# package_status_check function
# Time Complexity: 0(n), where n is the # of packages in the package_hash_table
# Input(s): time (00:00:00), package_input (either package id or "all")
# This function takes an input of time and package_input
# and checks the package_delivery_time and package_start_time of an individual package or all packages
# and assigns a package_delivery_status and prints the package(s) details.
def package_status_check(time, package_input):
    h, m, s = time.split(":")
    converted_input_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    if package_input == 'all':
        for i in range(len(package_data)):
            package = package_hash_table.look_up(int(i+1))
            if package.package_delivery_time < converted_input_time:
                package.package_delivery_status = "Delivered"
            elif package.package_start_time < converted_input_time:
                package.package_delivery_status = "En Route"
            else:
                package.package_delivery_status = "At the Hub"
            print(str(package))
    else:
        package = package_hash_table.look_up(int(package_input))
        # if package_input is not found within the package_hash_table
        if str(package) == "None":
            print("The entered package id was not found.")
        else:
            if package.package_delivery_time < converted_input_time:
                package.package_delivery_status = "Delivered"
            elif package.package_start_time < converted_input_time:
                package.package_delivery_status = "En Route"
            else:
                package.package_delivery_status = "At the Hub"
            print(str(package))


# Read PackageFile.csv for all packages data.
# Time Complexity: O(n), where n is the number of rows in the CSV file.
with open('files/PackageFile.csv') as packages:
    package_data = list(csv.reader(packages, delimiter=','))

# Read DeliveryAddresses.csv for all delivery locations.
# Time Complexity: O(n), where n is the number of rows in the CSV file.
with open('files/DeliveryAddresses.csv') as delivery_addresses:
    delivery_address_data = list(csv.reader(delivery_addresses, delimiter=','))

# Read DistanceTable.csv for distances between delivery locations.
# Time Complexity: O(n), where n is the number of rows in the CSV file.
with open('files/DistanceTable.csv') as distance:
    distance_data = list(csv.reader(distance, delimiter=','))

# This creates the package_hash_table object by calling the CreateHashMap class.
package_hash_table = CreateHashMap()

# This calls the load_package_data function to load the package date into the package_hash_table.
load_package_data(package_data, package_hash_table)

# Create 3 delivery_truck objects with the following inputs:
# truck_capacity, truck_speed, truck_packages
delivery_truck1 = Trucks.DeliveryTruck(16, 18, [])
delivery_truck2 = Trucks.DeliveryTruck(16, 18, [])
delivery_truck3 = Trucks.DeliveryTruck(16, 18, [])

# This calls the preload_delivery_trucks function to load packages for each delivery_truck.
preload_delivery_trucks()

# This calls the update_package_address function to correct the address for package #9.
# Correction is reported at 10:20 AM prior to delivery_truck3's departure at 11:00 AM.
update_package_address(9, "410 S State St,Salt Lake City,UT,84111")

# This calls the deliver_packages function for each delivery_truck.
# milage values are rounded.
truck1_milage = round(deliver_packages(delivery_truck1, '08:00:00'), 2)
truck2_milage = round(deliver_packages(delivery_truck2, '09:10:00'), 2)
truck3_milage = round(deliver_packages(delivery_truck3, '11:00:00'), 2)

# This calculates the total_miles_traveled for all three delivery_trucks.
total_miles_traveled = round(truck1_milage + truck2_milage + truck3_milage, 2)

# This displays the welcome message and route delivery details (including total mileage)
# Time Complexity: O(1)
print("--------------------------------------------------------------")
print("Welcome to Western Governors University Parcel Service (WGUPS)")
print("--------------------------------------------------------------")
print("Route Delivery Details:")
print("Delivery Truck 1 traveled", truck1_milage, "miles.")
print("Delivery Truck 2 traveled", truck2_milage, "miles.")
print("Delivery Truck 3 traveled", truck3_milage, "miles.")
print("Total mileage traveled by all delivery trucks:", total_miles_traveled, "miles")
print("--------------------------------------------------------------")
# Program will continue to run
finished = False
while not finished:
    print("Enter a package id to view the status and details for a specific package")
    user_input_1 = input("or enter 'All' to view the status and details of all packages: ").lower()
    user_input_time = input("Enter an specific time (hh:mm:ss): ")
    print("--------------------------------------------------------------")
    try:
        package_status_check(user_input_time, user_input_1)
        print("--------------------------------------------------------------")
    except ValueError:
        print("Invalid Entry.")

    user_input = input("Would you like view the status and details for another package"
                       " or another specified time? (Y/N)").lower()
    print("--------------------------------------------------------------")
    if user_input == "n":
        print("Thanks for using WGUPS!")
        finished = True
