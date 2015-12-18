import sys

from time import time
from unittest import TestCase

from venusian import Scanner

import stubs

from mediator import Mediator, Event, SubscriberInterface


class Listener(object):
    def __init__(self):
        self.events = []

    def __call__(self, event):
        self.events.append(event)


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
            'test_event': [
                ['middle'],
                ['first', -255],
                ['last', 255],
            ],
            'test_another_event': 'another_event_handler',
            'test_even_more_event': ['even_more_event_handler']
        }


class BadSubscriberOne(SubscriberInterface):
    def get_subscribed_events(self):
        return {
            'test_event': None
        }


class BadSubscriberTwo(SubscriberInterface):
    def get_subscribed_events(self):
        return {
            'test_event': []
        }


class TestMediator(TestCase):
    def test_dispatch_with_event(self):
        mediator = Mediator()
        event = Event()
        event.set_name('test_event')
        listener = Listener()
        mediator.add_listener(event, listener)
        mediator.dispatch(event)
        self.assertEqual(len(listener.events), 1)
        self.assertIs(listener.events[0], event)

    def test_dispatch_with_str(self):
        mediator = Mediator()
        listener = Listener()
        mediator.add_listener('test_event', listener)
        event = mediator.dispatch('test_event')
        self.assertEqual(len(listener.events), 1)
        self.assertIs(listener.events[0], event)

    def test_remove_listener(self):
        mediator = Mediator()
        listener1 = Listener()
        listener2 = Listener()
        mediator.add_listener('test_event', listener1)
        mediator.add_listener('test_event', listener2)
        mediator.dispatch('test_event')
        mediator.remove_listener('test_event', listener1)
        mediator.dispatch('test_event')
        self.assertEqual(len(listener1.events), 1)
        self.assertEqual(len(listener2.events), 2)
        mediator.remove_listener('test_event')
        mediator.dispatch('test_event')
        self.assertEqual(len(listener1.events), 1)
        self.assertEqual(len(listener2.events), 2)

    def test_add_listener_with_same_priority_failed(self):
        mediator = Mediator()
        mediator.add_listener('test_event', lambda event: None, 0)
        with self.assertRaises(IndexError):
            mediator.add_listener('test_event', lambda event: None, 0)

    def test_add_subscriber(self):
        mediator = Mediator()
        subscriber = Subscriber()
        with self.assertRaises(TypeError):
            mediator.add_subscriber(object())
        mediator.add_subscriber(subscriber)
        mediator.dispatch('test_event')
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

        event = mediator.dispatch('test_another_event')
        self.assertIs(subscriber.results['another'], event)

        event = mediator.dispatch('test_even_more_event')
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
    def test_event(self):
        event = Event()
        self.assertEqual(event.get_name(), 'Event')
        event.set_name('new-event')
        self.assertEqual(event.get_name(), 'new-event')
        event = Event('new-event')
        self.assertEqual(event.get_name(), 'new-event')


class TestEventDecorator(TestCase):
    def test_event_decorator(self):
        mediator = Mediator()
        event = stubs.VenusianEvent()
        mediator.dispatch(event)
        self.assertFalse(event.success)
        mediator.scan(stubs)
        mediator.dispatch(event)
        self.assertTrue(event.success)

        mediator = Mediator()
        mediator.set_scanner(Scanner(mediator=mediator))
        event = stubs.VenusianEvent()
        mediator.dispatch(event)
        self.assertFalse(event.success)
        mediator.scan(stubs)
        mediator.dispatch(event)
        self.assertTrue(event.success)
