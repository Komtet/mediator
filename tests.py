from time import time
from unittest import TestCase

import stubs

from mediator import Mediator, Event, SubscriberInterface


class Listener(object):
    def __init__(self):
        self.events = []

    def __call__(self, event):
        self.events.append(event)


class EventOne(Event):
    event_name = 'event_one'


class EventTwo(Event):
    event_name = 'event_two'


class EventThree(Event):
    event_name = 'event_three'


class Subscriber(SubscriberInterface):
    def __init__(self):
        self.results = {}

    def first(self, event):
        self.results['first'] = (event, time())

    def middle(self, event):
        self.results['middle'] = (event, time())

    def last(self, event):
        self.results['last'] = (event, time())

    def another_event_handler(self, event):
        self.results['another'] = event

    def even_more_event_handler(self, event):
        self.results['even_more'] = event

    def get_subscribed_events(self):
        return {
            'event_one': [
                ['middle'],
                ['first', -255],
                ['last', 255],
            ],
            'event_two': 'another_event_handler',
            'event_three': ['even_more_event_handler']
        }


class BadSubscriberOne(SubscriberInterface):
    def get_subscribed_events(self):
        return {'test_event': None}


class BadSubscriberTwo(SubscriberInterface):
    def get_subscribed_events(self):
        return {'test_event': []}


class TestMediator(TestCase):
    def test_dispatch_failed(self):
        meditator = Mediator()
        with self.assertRaises(TypeError) as context:
            meditator.dispatch('unexpected_event')
        self.assertEqual(str(context.exception), 'Expects instance of Event')

    def test_add_listener_with_object(self):
        mediator = Mediator()
        listener = Listener()
        mediator.add_listener(Event, listener)
        event = Event()
        mediator.dispatch(event)
        self.assertEqual(len(listener.events), 1)
        self.assertIs(listener.events[0], event)

    def test_add_listener_with_string(self):
        mediator = Mediator()
        listener = Listener()
        mediator.add_listener('Event', listener)
        event = Event()
        event = mediator.dispatch(event)
        self.assertEqual(len(listener.events), 1)
        self.assertIs(listener.events[0], event)

    def test_add_listener_with_same_priority_failed(self):
        mediator = Mediator()
        mediator.add_listener(Event, lambda event: None, 0)
        with self.assertRaises(IndexError):
            mediator.add_listener(Event, lambda event: None, 0)

    def test_add_listener_with_invalid_event_failed(self):
        mediator = Mediator()
        listener = Listener()
        with self.assertRaises(TypeError) as context:
            mediator.add_listener(1, listener)
        self.assertEqual(str(context.exception), 'Expects subclass of Event or str')

    def test_remove_listener(self):
        mediator = Mediator()
        listener1 = Listener()
        listener2 = Listener()
        mediator.add_listener(Event, listener1)
        mediator.add_listener(Event, listener2)
        event = Event()
        mediator.dispatch(event)
        mediator.remove_listener(Event, listener1)
        mediator.dispatch(event)
        self.assertEqual(len(listener1.events), 1)
        self.assertEqual(len(listener2.events), 2)
        mediator.remove_listener(Event)
        mediator.dispatch(event)
        self.assertEqual(len(listener1.events), 1)
        self.assertEqual(len(listener2.events), 2)

    def test_remove_listener_with_invalid_event_failed(self):
        mediator = Mediator()
        listener = Listener()
        with self.assertRaises(TypeError) as context:
            mediator.remove_listener(1, listener)
        self.assertEqual(str(context.exception), 'Expects subclass of Event or str')

    def test_add_subscriber(self):
        mediator = Mediator()

        with self.assertRaises(TypeError) as context:
            mediator.add_subscriber(object())
        self.assertEqual(str(context.exception), 'Expects instance of SubscriberInterface')

        subscriber = Subscriber()
        mediator.add_subscriber(subscriber)

        event = EventOne()
        mediator.dispatch(event)
        self.assertEqual(len(subscriber.results), 3)
        events = [result[0] for result in subscriber.results.values()]
        self.assertIs(events[0], events[1])
        self.assertIs(events[1], events[2])
        first, middle, last = (
            subscriber.results['first'][1],
            subscriber.results['middle'][1],
            subscriber.results['last'][1]
        )
        self.assertTrue(first < middle < last, '%r %r %r' % (first, middle, last))

        event = EventTwo()
        mediator.dispatch(event)
        self.assertIs(subscriber.results['another'], event)

        event = EventThree()
        mediator.dispatch(event)
        self.assertIs(subscriber.results['even_more'], event)

        with self.assertRaises(ValueError):
            mediator.add_subscriber(BadSubscriberOne())

        with self.assertRaises(ValueError):
            mediator.add_subscriber(BadSubscriberTwo())


class TestSubscriberInterface(TestCase):
    def test_get_subscribed_events(self):
        subscriber = SubscriberInterface()
        with self.assertRaises(NotImplementedError):
            subscriber.get_subscribed_events()


class TestEvent(TestCase):
    def test_get_event_name(self):
        self.assertEqual(Event.get_event_name(), 'Event')
        self.assertEqual(EventOne.get_event_name(), 'event_one')
        self.assertEqual(EventTwo.get_event_name(), 'event_two')
        self.assertEqual(EventThree.get_event_name(), 'event_three')


class TestEventDecorator(TestCase):
    def test_event_decorator(self):
        mediator = Mediator()
        event = stubs.VenusianEvent()
        mediator.dispatch(event)
        self.assertFalse(event.success)
        mediator.scan(package=stubs)
        mediator.dispatch(event)
        self.assertTrue(event.success)
