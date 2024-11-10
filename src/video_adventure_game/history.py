import datetime

class Event:
    def __init__(self, choice):
        self.date = datetime.datetime.now()
        self.choice = choice

class History:
    """Define history of choice"""

    def __init__(self):
        self.event_choices = []

    def add_event(self, choice):
        self.event_choices.append(Event(choice))

    def __str__(self):
        return ",".join([event.choice.id for event in self.event_choices])
    
    def last(self, nb):
        return ",".join([event.choice.id for event in self.event_choices][-nb:])