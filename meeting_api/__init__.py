from .api import ApiResult, ApiError
from pony.flask import Pony

from .api import FlaskApi
from .models import db
from .routes import events, members


def create_app():
    app = FlaskApi(__name__, instance_relative_config=True)
    app.config.from_pyfile('development.py')

    app.register_blueprint(events.bp)
    app.register_blueprint(members.bp)

    return app


app = create_app()

Pony(app)


@app.route('/')
def index():
    raise ApiError('Error in Api')
    # return ApiResult([1, 2, 3])


db.bind(**app.config.get('PONY'))
db.generate_mapping(create_tables=True)
