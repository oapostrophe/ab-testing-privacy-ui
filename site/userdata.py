class Event:
    """Class to store data for each event during a visit."""
    def __init__(self, user_id, url, timestamp, event_type, element_id, banner_style, user_agent, mobile):
        self.user_id = user_id
        self.url = url
        self.timestamp = timestamp
        self.event_type = event_type
        self.element_id=element_id
        self.banner_style=banner_style
        self.user_agent=user_agent
        self.mobile=mobile

    def __str__(self):
        return self.user_id + self.event_type