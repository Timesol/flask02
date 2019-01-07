from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, AnyOf, InputRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User,Post,Location, Customer
from flask import request



class PypScriptsForm(FlaskForm):
    name=StringField(_l('Scriptname'))
    body=TextAreaField(_l('Script'))
    submit = SubmitField(_l('Submit'))


class CreateTemplateForm(FlaskForm):
    name=StringField(_l('Templatename'))
    create = SubmitField(_l('Create'))