from flask import Blueprint, request, url_for, abort
from pony.orm import flush

from ..api import ApiError, ApiResult, PonyResult, get_valid_document
from ..models import Event, Person, EventMembers
from .. import validation_rules


bp = Blueprint('members', __name__, url_prefix='/members')


@bp.route('/<int:id>')
def get(id):
    return PonyResult(Person[id])


@bp.route('/<email>')
def get_by_email(email):
    person = Person.get(email=email)

    if person is None:
        abort(404)

    return PonyResult(person)


@bp.route('/', methods=['POST'])
def create():
    document = get_valid_document(validation_rules.person_schema, request.json)
    # fixme: проверка на дублирующий E-Mail в БД
    person = Person(**document)
    flush()
    return PonyResult(person, 201, {
        'Location': url_for('members.get', id=person.id)
    })


@bp.route('/<int:id>/events/<int:event_id>', methods=['POST'])
def registration(id, event_id):
    member = Person[id]
    event = Event[event_id]

    if EventMembers.exists(person=member, event=event):
        raise ApiError(
            f'You have already successfully registered to "{event.title}".', 409)

    return PonyResult(EventMembers(event=event, person=member), 201, {
        # 'Location': url_for('events.get', id=event.id)
    })


@bp.route('/<int:id>/events')
def events(id):
    member = Person[id]
    return PonyResult(member.event_members, exclude=['person'])
