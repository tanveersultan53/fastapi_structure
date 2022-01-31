import os

from invoke import task

# from app.widget.model import Widget
from app.fizz.model import Fizz

from app.db import get_db, Base, engine
from wsgi import app


@task
def init_db(ctx):
    print("Creating all resources.")

    Base.metadata.create_all()
    engine.execute("insert into widget values (1, 'hey', 'there');")
    print(engine.execute("select * from widget;"))


@task
def drop_all(ctx):
    if input("Are you sure you want to drop all tables? (y/N)\n").lower() == "y":
        print("Dropping tables...")
        Base.metadata.drop_all()


def seed_things():
    # classes = [Widget, Fizz]
    classes = [ Fizz]
    for klass in classes:
        seed_thing(klass)


def seed_thing(cls):
    session = next(get_db())
    things = [
        {"name": "Pizza Slicer", "purpose": "Cut delicious pizza"},
        {"name": "Rolling Pin", "purpose": "Roll delicious pizza"},
        {"name": "Pizza Oven", "purpose": "Bake delicious pizza"},
    ]
    session.bulk_insert_mappings(cls, things)
    session.commit()


@task
def seed_db(ctx):
    if (
        input("Are you sure you want to drop all tables and recreate? (y/N)\n").lower()
        == "y"
    ):
        print("Dropping tables...")
        Base.metadata.drop_all()
        Base.metadata.create_all()
        seed_things()
        print("DB successfully seeded.")