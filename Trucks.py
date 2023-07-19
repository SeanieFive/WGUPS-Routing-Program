class DeliveryTruck:
    def __init__(self, truck_capacity, truck_speed, truck_packages):
        self.truck_capacity = truck_capacity
        self.truck_speed = truck_speed
        self.truck_packages = truck_packages

    def __str__(self):
        return "%s, %s, %s" % (self.truck_capacity, self.truck_speed, self.truck_packages)
