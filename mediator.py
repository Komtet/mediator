from collections import OrderedDict


class Mediator(object):
    def __init__(self):
        self._listeners = {}

    def dispatch(self, event):
        if not isinstance(event, Event):
            event_name = event
            event = Event()
            event.set_name(event_name)
        else:
            event_name = event.get_name()
        if event_name in self._listeners:
            for listener in self._listeners[event_name].values():
                listener(event)
        return event

    def add_listener(self, event, listener, priority=None):
        event_name = _get_event_name(event)
        if event_name not in self._listeners:
            self._listeners[event_name] = {}
        if priority is not None:
            if priority in self._listeners[event_name]:
                raise IndexError(
                    'The event "{0}" already have a listener '
                    'with priority {1}'.format(
                        event_name,
                        priority
                    )
                )
        else:
            if len(self._listeners[event_name]):
                priority = list(self._listeners[event_name].keys())[-1] + 1
            else:
                priority = 0
        self._listeners[event_name][priority] = listener
        self._listeners[event_name] = OrderedDict(sorted(
            self._listeners[event_name].items(),
            key=lambda item: item[0]
        ))

    def remove_listener(self, event, listener=None):
        event_name = _get_event_name(event)
        if event_name in self._listeners:
            if not listener:
                del self._listeners[event_name]
            else:
                for p, l in self._listeners[event_name].items():
                    if l is listener:
                        self._listeners[event_name].pop(p)
                        return

    def add_subscriber(self, subscriber):
        if not isinstance(subscriber, SubscriberInterface):
            raise TypeError('Unexpected subscriber type given')
        for event_name, params in subscriber.get_subscribed_events().items():
            if isinstance(params, str):
                self.add_listener(event_name, getattr(subscriber, params))
            elif isinstance(params, list):
                if not params:
                    raise ValueError('Invalid params "%r" for event "%s"' % (params, event_name))
                if len(params) <= 2 and isinstance(params[0], str):
                    priority = params[1] if len(params) > 1 else None
                    self.add_listener(event_name, getattr(subscriber, params[0]), priority)
                else:
                    for listener in params:
                        priority = listener[1] if len(listener) > 1 else None
                        self.add_listener(event_name, getattr(subscriber, listener[0]), priority)
            else:
                raise ValueError('Invalid params for event "%s"' % event_name)


class Event(object):
    def __init__(self, name=None):
        self.__name = name

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class SubscriberInterface(object):
    def get_subscribed_events(self):
        raise NotImplementedError()


def _get_event_name(event):
    if isinstance(event, Event):
        return event.get_name()
    else:
        return event
