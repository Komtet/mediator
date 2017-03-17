import collections
import inspect

import venusian

__all__ = ['Mediator', 'Event', 'SubscriberInterface']

VENUSIAN_CATEGORY = 'mediator'


class Mediator(object):
    def __init__(self):
        self._listeners = {}
        super(Mediator, self).__init__()

    def dispatch(self, event):
        if not isinstance(event, Event):
            raise TypeError('Expects instance of Event')
        event_name = event.get_event_name()
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
        self._listeners[event_name] = collections.OrderedDict(sorted(
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
            raise TypeError('Expects instance of SubscriberInterface')
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
    event_name = None

    @classmethod
    def get_event_name(cls):
        return cls.__name__ if cls.event_name is None else cls.event_name

    @classmethod
    def listen(cls, priority=None, instance='mediator', category=VENUSIAN_CATEGORY):
        event_name = cls.get_event_name()

        def decorator(listener):
            def callback(scanner, name, ob):
                getattr(scanner, instance).add_listener(event_name, listener, priority)
            venusian.attach(listener, callback, category=category)
            return listener

        return decorator


class SubscriberInterface(object):
    def get_subscribed_events(self):
        raise NotImplementedError()


def _get_event_name(event):
    if isinstance(event, str):
        return event
    if inspect.isclass(event) and issubclass(event, Event):
        return event.get_event_name()
    raise TypeError('Expects subclass of Event or str')
