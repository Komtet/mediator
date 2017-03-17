from setuptools import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='mediator',
    version='0.4.0',
    keywords=['event', 'events', 'mediator', 'dispatcher', 'event dispatcher'],
    description='A library implements the Mediator pattern to make your code extensible',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    long_description=long_description,
    author='Kilte Leichnam',
    author_email='nwotnbm@gmail.com',
    url='https://github.com/Kilte/mediator',
    py_modules=['mediator'],
    install_requires=['venusian'],
    test_suite='tests',
    tests_require=['coverage']
)
