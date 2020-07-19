from flask import Blueprint, request, url_for
from pony.orm import flush, desc

from ..api import ApiError, ApiResult, PonyResult, get_valid_document
from ..models import Event
from ..validation_rules import event_schema


bp = Blueprint('events', __name__, url_prefix='/events')


@bp.route('/')
def index():
    return PonyResult(
        Event.select().order_by(desc(Event.start_date))
    )


@bp.route('/', methods=['POST'])
def create():
    document = get_valid_document(event_schema, request.json)
    event = Event(**document)
    flush()
    return PonyResult(event, 201, {
        'Location': url_for('events.get', id=event.id)
    })


@bp.route('/<int:id>')
def get(id):
    return PonyResult(Event[id])


@bp.route('/<int:id>', methods=['PUT'])
def update(id):
    event = Event[id]
    document = get_valid_document(event_schema, request.json)
    event.set(**document)
    return PonyResult(event)


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    event = Event[id]
    event.delete()
    return ApiResult(status=204)


@bp.route('/<int:id>/members')
def members(id):
    event = Event[id]
    return PonyResult(event.event_members, exclude=['event'])
