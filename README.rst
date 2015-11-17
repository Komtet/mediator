========
Mediator
========

A library implements the Mediator pattern to make your code extensible.

Inspired by `symfony/event-dispatcher <https://github.com/symfony/event-dispatcher>`_ component.

.. image:: https://img.shields.io/travis/Kilte/mediator.svg?style=flat-square
    :target: https://travis-ci.org/Kilte/mediator

Installation
============

Using pip:

.. code:: sh

    # pip install mediator

Manually:

.. code:: sh

    $ git clone https://github.com/Kilte/mediator
    $ cd mediator
    # python setup.py install

Usage
=====

.. code:: python

    from mediator import Mediator

    m = Mediator()


Adding a listener
-----------------

.. code:: python

    def event_listener(event):
        print('Got event: %r' % event)

    m.add_listener('event_name', event_listener)

Triggering events
-----------------

.. code:: python

    event = m.dispatch('event_name')
    # Got event: <mediator.Event object at 0x7f954bc2b250>
    print(event)
    # <mediator.Event object at 0x7f954bc2b250>

Removing a listener
-------------------

.. code:: python

    def another_listener(event):
        print('Got another event: %r' % event)

    m.add_listener('event_name', another_listener)
    m.remove_listener('event_name', event_listener)
    m.dispatch('event_name')
    # Got another event: <mediator.Event object at 0x7f954bbbd510>


Removing all listeners
----------------------

.. code:: python

    m.remove_listener('event_name')
    m.dispatch('event_name')
    # Nothing was happened


Using priorities
----------------

.. code:: python

    m.add_listener('test_event', another_listener, -255)
    m.add_listener('test_event', event_listener, 255)
    m.dispatch('test_event')
    # Got another event: <mediator.Event object at 0x7f954bbbd510>
    # Got event: <mediator.Event object at 0x7f954bbbd510>


Defining custom events
----------------------

.. code:: python

    from mediator import Event

    def my_event_listener(event):
        event.params = 'params'


    class MyEvent(Event):
        def __init__(self):
            super(MyEvent, self).__init__('my_event')
            self.params = None

    event = MyEvent()
    m.add_listener('my_event', my_event_listener)
    m.dispatch(event)
    print(event.params)
    # params


Using Subscribers
-----------------

.. code:: python

    from mediator import SubscriberInterface


    class Subscriber(SubscriberInterface):
        def first(self, event):
            event.first = True

        def middle(self, event):
            event.middle = True

        def last(self, event):
            event.last = True

        def event2_handler(self, event):
            event.success = True

        def event3_handler(self, event):
            event.success = True

        def get_subscribed_events(self):
            return {
                'event1': [
                    ['middle'],
                    ['first', -100],
                    ['last', 100]
                ],
                'event2': 'event2_handler',
                'event3': ['event3_handler']
            }

    class Event1(Event):
         def __init__(self):
             super(Event1, self).__init__('event1')
             self.first = False
             self.middle = False
             self.last = False

    class Event2(Event):
         def __init__(self):
             super(Event2, self).__init__('event2')
             self.success = True

    class Event3(Event2):
        pass

    subscriber = Subscriber()
    event1 = Event1()
    event2 = Event2()
    event3 = Event3()

    m.add_subscriber(subscriber)

    m.dispatch(event1)
    print('%s;%s;%s' % (event1.first, event1.middle, event1.last))
    # True;True;True

    m.dispatch(event2)
    print(event2.success)
    # True

    m.dispatch(event3)
    print(event3.success)
    # True

See source code and tests for more information.

Changelog
=========

0.1.0 (19.11.2015)
------------------

- First release.

Contributing
============

- Fork and clone it
- Create your feature branch (git checkout -b awesome-feature)
- Make your changes
- Write/update tests, if it's necessary
- Update README.md, if it's necessary
- Push your branch (git push origin awesome-feature)
- Send a pull request

LICENSE
=======

The MIT License (MIT)
