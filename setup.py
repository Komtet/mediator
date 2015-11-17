from setuptools import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='mediator',
    version='0.1.0',
    description='A library implements the Mediator pattern to make your code extensible',
    long_description=long_description,
    author='Kilte Leichnam',
    author_email='nwotnbm@gmail.com',
    url='https://github.com/Kilte/mediator',
    py_modules=['mediator'],
    license='MIT',
    keywords=['event', 'events', 'mediator', 'dispatcher', 'event dispatcher'],
    test_suite='tests'
)
