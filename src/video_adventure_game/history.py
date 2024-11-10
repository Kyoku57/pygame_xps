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

    def events_by_id(self, choice_id):
        return [event for event in self.event_choices if event.choice.id == choice_id]
    
    def event_has_choice_id(self, choice_id):
        return len(self.events_by_id(choice_id))>0

    def __str__(self):
        return ",".join([event.choice.id for event in self.event_choices])
    
    def last(self, nb):
        return ",".join([event.choice.id for event in self.event_choices][-nb:])