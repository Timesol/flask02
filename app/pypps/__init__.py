from flask import Blueprint

bp = Blueprint('pypps', __name__)

from app.pypps import routes