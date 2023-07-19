# This creates the Package class
class Package:
    def __init__(self, package_id, package_address, package_city, package_state,
                 package_zip, package_deadline, package_weight, package_notes, package_start_time,
                 package_delivery_time, package_delivery_status):
        self.package_id = package_id
        self.package_address = package_address
        self.package_city = package_city
        self.package_state = package_state
        self.package_zip = package_zip
        self.package_deadline = package_deadline
        self.package_weight = package_weight
        self.package_notes = package_notes
        self.package_start_time = package_start_time
        self.package_delivery_time = package_delivery_time
        self.package_delivery_status = package_delivery_status

    def __str__(self):
        # If the package has been delivered, Delivery Time is displayed.
        if self.package_delivery_status == "Delivered":
            return "Package ID: %s, Delivery Address: %s, Delivery Deadline: %s, Delivery City: %s, " \
                   "Delivery Zip: %s, Package Weight: %s, Delivery Status: %s, Delivery Time: %s"\
                % (self.package_id, self.package_address, self.package_deadline, self.package_city,
                   self.package_zip, self.package_weight, self.package_delivery_status, self.package_delivery_time)
        else:
            # If the package has NOT been delivered, Estimated Delivery Time is displayed.
            return "Package ID: %s, Delivery Address: %s, Delivery Deadline: %s, Delivery City: %s, " \
                   "Delivery Zip: %s, Package Weight: %s, Delivery Status: %s, Estimated Delivery Time: %s"\
                % (self.package_id, self.package_address, self.package_deadline, self.package_city,
                   self.package_zip, self.package_weight, self.package_delivery_status, self.package_delivery_time)
