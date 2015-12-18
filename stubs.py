from mediator import Event


class VenusianEvent(Event):
    def __init__(self):
        super(VenusianEvent, self).__init__()
        self.success = False


@VenusianEvent.listen()
def venusian_event_listener(event):
    event.success = True
