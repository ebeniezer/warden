from flask import Blueprint
application_blueprint = Blueprint('application', __name__, template_folder='templates')

__all__ = [
    'views'
]

from . import views