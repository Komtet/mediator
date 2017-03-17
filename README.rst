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

Defining events
----------------------

.. code:: python

    from mediator import Event


    class EventOne(Event):
        pass


    class EventTwo(Event):
        event_name = 'event_two'

Adding a listener
-----------------

.. code:: python

    def event_listener(event):
        print('Got event: %r' % event)

    m.add_listener(EventOne, event_listener)
    # or m.add_listener('EventOne', event_listener)
    m.add_listener('event_two', event_listener)
    # or m.add_listener(EventTwo, event_listener)

Triggering events
-----------------

.. code:: python

    event1 = EventOne()
    event2 = EventTwo()

    m.dispatch(event1)
    # Got event: <EventOne object at 0x7f954bc2b250>

    m.dispatch(event2)
    # Got event: <EventTwo object at 0x7f954bbbd510>

Removing a listener
-------------------

.. code:: python

    def another_listener(event):
        print('Got another event: %r' % event)

    m.add_listener(EventOne, another_listener)
    m.remove_listener('EventOne', event_listener)
    m.dispatch(event1)
    # Got another event: <EventOne object at 0x7f954bc2b250>


Removing all listeners
----------------------

.. code:: python

    m.remove_listener('EventOne')
    m.dispatch(event1)
    # Nothing was happened


Using priorities
----------------

.. code:: python

    m.add_listener('EventOne', another_listener, -255)
    m.add_listener('EventOne', event_listener, 255)
    m.dispatch(event1)
    # Got another event: <EventOne object at 0x7f954bc2b250>
    # Got event: <EventOne object at 0x7f954bc2b250>


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
        event_name = 'event1'

        def __init__(self):
             self.first = False
             self.middle = False
             self.last = False

    class Event2(Event):
        event_name = 'event2'

         def __init__(self):
             self.success = True

    class Event3(Event2):
        event_name = 'event3'

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


Adding listeners using decorator
--------------------------------

.. code:: python

    import sys
    import venusian

    from mediator import VENUSIAN_CATEGORY


    @SomeEvent.listen(priority=255, instance='mediator', category=VENUSIAN_CATEGORY)  # All args are optional
    def some_event_listener(event):
        event.attr = 'value'

    scanner = venusian.Scanner(mediator=mediator)
    scanner.scan(package=sys.modules[__name__], categories=[VENUSIAN_CATEGORY])
    m.dispatch(SomeEvent())

See source code and tests for more information.

Changelog
=========


0.4.0 (17.03.2017)
------------------

- Fixed multiple inheritance support
- Improved venusian support

0.3.0 (25.02.2016)
------------------

- ``Mediator.__init__`` and ``Mediator.scan`` now takes keyword arguments only.
- Removed ``Mediator.set_scanner`` method.
- ``Mediator.dispatch()`` now takes event instances only.
- ``Mediator.add_listener`` and ``Mediator.remove_listener`` takes subclass of ``Event`` or ``str``.
- ``Event.get_name()`` and ``Event.set_name()`` were removed in favor of ``Event.get_event_name()`` and ``Event.event_name`` class attribute.
- And now there is no requirement to call ``super().__init__()`` in your own events.

0.2.1 (18.12.2015)
------------------

- Added ``Mediator.set_scanner`` method in order to allow use custom scanner instance.

0.2.0 (17.12.2015)
------------------

- Automatic event name detection based on a class name.
- Added ``%Event%.listen`` decorator.

0.1.0 (19.11.2015)
------------------

- First release.

Contributing
============

- Fork and clone it
- Create your feature branch (git checkout -b awesome-feature)
- Make your changes
- Write/update tests, if it's necessary (make buildout && make tests)
- Update README.md, if it's necessary
- Push your branch (git push origin awesome-feature)
- Send a pull request

LICENSE
=======

The MIT License (MIT)
