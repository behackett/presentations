from setuptools import setup

setup(
    name='FlywayTutorial',
    packages=['flyway_tutorial'],
    entry_points='''
    [flyway.migrations]
    a = flyway_tutorial.migrations_a
    b = flyway_tutorial.migrations_b''',
    paster_plugins=['Ming']
    )
