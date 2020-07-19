import traceback

from cerberus import Validator
from flask import Flask, jsonify
from pony.orm import ObjectNotFound
from pony.orm.core import Entity, Query, SetInstance
from pony.orm.serialization import to_dict
from werkzeug.exceptions import HTTPException


def get_valid_document(schema, document, message=None):
    v = Validator(schema)

    if not v.validate(document):
        raise ValidationError(v.errors, message)

    return v.document


class FlaskApi(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register_error_handler(
            ApiError, lambda err: err.to_result()
        )
        self.register_error_handler(
            HTTPException, self.__handle_http_exception
        )
        self.register_error_handler(
            ObjectNotFound, self.__handle_entity_not_found
        )
        self.register_error_handler(
            Exception, self.__handle_exception
        )

    def __handle_exception(self, err):
        args = err.__class__, err, err.__traceback__
        description = None

        if self.debug:
            description = traceback.format_exception(*args)

        traceback.print_exception(*args)

        return ApiError(str(err), 500, description).to_result()

    def __handle_http_exception(self, err):
        err = ApiError(err.name, err.code, err.description)
        return err.to_result()

    def __handle_entity_not_found(self, err):
        message = f'Entity "{err.entity.__name__}" with id "{err.pkval}" not found.'
        return ApiError(message, 404).to_result()

    def make_response(self, rv):
        if isinstance(rv, ApiResult):
            rv = rv.to_response()
        return super().make_response(rv)


class ApiResult(object):
    def __init__(self, body=None, status=200, headers=None):
        self._body = None
        self._status = status
        self._headers = headers

        if body is not None:
            self.set_body(body)

    def set_body(self, body):
        self._body = body

    def to_response(self):
        return jsonify(self._body), self._status, self._headers


class PonyResult(ApiResult):
    def __init__(self, body=None, status=200, headers=None, **to_dict_kwargs):
        self.to_dict_kwargs = to_dict_kwargs
        super().__init__(body, status, headers)

    def set_body(self, body):
        if isinstance(body, SetInstance):
            body = body.select()

        if isinstance(body, Query):
            self._body = [
                i.to_dict(with_lazy=True, **self.to_dict_kwargs)
                for i in body
            ]
        elif isinstance(body, Entity):
            self._body = body.to_dict(
                with_lazy=True, **self.to_dict_kwargs
            )
        else:
            assert False, 'Invalid PonyORM type for body.'


class ApiError(Exception):
    def __init__(self, message, status=400, description=None):
        self.message = message
        self.status = status
        self.description = description

    def to_result(self):
        return ApiResult({
            'message': self.message,
            'status': self.status,
            'description': self.description,
        }, self.status)


class ValidationError(ApiError):
    def __init__(self, errors, message=None):
        super().__init__(
            message or 'The request contains errors and cannot be processed.',
            status=422,
            description=errors
        )
