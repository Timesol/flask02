from flask import Blueprint

bp = Blueprint('pyps', __name__)

from app.pyps import routes