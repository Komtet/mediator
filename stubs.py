from mediator import Event


class VenusianEvent(Event):
    def __init__(self):
        super(VenusianEvent, self).__init__()
        self.success = False


class VenusianEventWithCategory(Event):
    def __init__(self):
        super(VenusianEventWithCategory, self).__init__()
        self.success = False


@VenusianEvent.listen()
def venusian_event_listener(event):
    event.success = True


@VenusianEventWithCategory.listen(instance='obj', category='custom-category')
def venusian_event_with_category_listener(event):
    event.success = True
