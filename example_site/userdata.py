import csv

class Event:
    """Class to store data for each event during a visit."""
    def __init__(self, user_id, timestamp, event_type, element_id=None):
        self.user_id = user_id
        self.timestamp = timestamp
        self.event_type = event_type
        self.element_id=element_id

    def __str__(self):
        return self.user_id + self.event_type