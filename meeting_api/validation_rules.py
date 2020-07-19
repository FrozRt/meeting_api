from dateutil import parser

event_schema = {
    'title': {
        'required': True,
        'type': 'string',
        'minlength': 1,
        'maxlength': 512,
    },
    'description': {
        'required': True,
        'type': 'string',
        'minlength': 1,
    },
    'text': {
        'required': True,
        'type': 'string',
        'minlength': 1,
    },
    'start_date': {
        'required': True,
        'type': 'datetime',
        'coerce': parser.parse,
    },
    'end_date': {
        'required': True,
        'type': 'datetime',
        'coerce': parser.parse,
    },
    'address': {
        'type': 'string',
    },
}


person_schema = {
    'firstname': {
        'required': True,
        'type': 'string',
        'minlength': 1,
        'maxlength': 255,
    },
    'lastname': {
        'required': True,
        'type': 'string',
        'minlength': 1,
        'maxlength': 255,
    },
    'email': {
        'required': True,
        'type': 'string',
        'minlength': 3,
        'maxlength': 64,
        'regex': r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    },
    'phone': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 32,
        'regex': r'^\+\d+$',
    },
}