from datetime import datetime

from pony.orm import (
    Database,
    Required, Optional, PrimaryKey, Set,
    LongStr
)


db = Database()


class UpdateableMixin(object):
    def before_update(self):
        self.updated = datetime.now()


class Person(db.Entity, UpdateableMixin):
    firstname = Required(str, 255)
    lastname = Required(str, 255)
    email = Required(str, 64, unique=True)
    phone = Optional(str, 32)
    created = Optional(datetime, default=datetime.now)
    updated = Optional(datetime, default=datetime.now)
    event_members = Set('EventMembers')

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Event(db.Entity, UpdateableMixin):
    title = Required(str, 512)
    description = Required(LongStr)
    text = Required(LongStr)
    start_date = Required(datetime)
    end_date = Required(datetime)
    address = Optional(LongStr)
    created = Optional(datetime, default=datetime.now)
    updated = Optional(datetime, default=datetime.now)
    event_members = Set('EventMembers')


class EventMembers(db.Entity, UpdateableMixin):
    person = Required('Person')
    event = Required('Event')
    approved = Optional(bool, default=False)
    created = Optional(datetime, default=datetime.now)
    updated = Optional(datetime, default=datetime.now)
    PrimaryKey(person, event)
