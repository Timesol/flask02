
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, AnyOf, InputRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User,Post,Location, Customer
from flask import request

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class LocationForm(FlaskForm):
    residence = StringField(_l('Residence'))
    technology = StringField(_l('Technology'))
    customer = SelectField(u'Customer', coerce=int, validators=[InputRequired()])
    hardware= StringField(_l('Hardware'))
    project= StringField(_l('Project'))
    projectmanager= StringField(_l('Projectmanager'))
    contract=StringField(_l('Contract ID'))
    submit = SubmitField(_l('Submit'))


class NetworkForm(FlaskForm):
    locid=StringField(_l('ID'))
    name=StringField(_l('Name'))
    network=StringField(_l('Network'))
    fromip=StringField(_l('From'))
    toip=StringField(_l('To'))
    gateway=StringField(_l('Gateway'))
    subnet=StringField(_l('Subnet'))
    cdir=StringField(_l('Cdir'))
    vip =StringField(_l('Vip'))
    adinfo1 =StringField(_l('Additional Info'))
    adinfo2 =StringField(_l('Additional Info 2'))
    submit = SubmitField(_l('Submit'))


class CustomerForm(FlaskForm):
    name= StringField(_l('Name'))
    submit = SubmitField(_l('Submit'))
    


class Post_r_Form(FlaskForm):
    post_r = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class Statistic_Work_Form(FlaskForm):
    category=SelectField('Category',
        choices=[('installation', 'Installation'), ('commissioning', 'Commissioning'), ('dismantling', 'Dismantling'),('mpls', 'MPLS'),('cia', 'CIA'),('hardware', 'Hardware'),('unlock', 'Unlock'),('disruption', 'Disruption')])
    technology=StringField(_l('Technology'))
    time=StringField(_l('Time'))
    customer=StringField(_l('Customer'))
    contract=StringField(_l('Contract'))
    hardware=StringField(_l('Hardware'))
    user=StringField(_l('User'))
    subcategory=SelectField(u'Subcategory',  validators=[InputRequired()])
    adinfo=SelectField(u'adinfo', validators=[InputRequired()])
    submit = SubmitField(_l('Submit'))  
    
    
