
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, AnyOf, InputRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User,Post,Location, Customer
from flask import request
from wtforms.fields.html5 import DateField
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
    contact=StringField(_l('Contact'))
    sid=StringField(_l('SID'))
    matchcode=StringField(_l('Matchcode'))
    seller=StringField(_l('Seller'))
    vrf=StringField(_l('VRF'))
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
    submit = SubmitField(_l('Submit'))


class CustomerForm(FlaskForm):
    name= StringField(_l('Name'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def validate_name(self, name):
        customer = Customer.query.filter_by(name=name.data).first()
        if customer is not None:
            raise ValidationError(_('Please use a different Customer.'))
    


class Post_r_Form(FlaskForm):
    post_r = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class Statistic_Work_Form(FlaskForm):
    category=SelectField(u'Category', coerce=int, validators=[InputRequired()])
    technology=StringField(_l('Technology') ,id='stat_technology')
    time=IntegerField(_l('Time') ,id='stat_time')
    customer=StringField(_l('Customer') ,id='stat_customer')
    contract=StringField(_l('Contract'),id='stat_contract')
    hardware=StringField(_l('Hardware') , id='stat_hardware')
    user=StringField(_l('User'), id='stat_user')
    subcategory=SelectField(u'Subcategory', coerce=int, validators=[InputRequired()], id='stat_subcategory')
    
    submit = SubmitField(_l('Submit'))

class DeleteForm(FlaskForm):
    id_del=IntegerField(_l('ID_DEL'), validators=[DataRequired()])
    delete = SubmitField(_l('Delete'))


class InfoForm(FlaskForm):
    infotext=StringField(_l('Info'))
    submit2 = SubmitField(_l('Submit'))


class RemoveForm(FlaskForm):
    id_rem=IntegerField(_l('ID_REM'), validators=[DataRequired()])
    remove = SubmitField(_l('Remove'))


class ScriptForm(FlaskForm):
    description=StringField(_l('Description'))
    script=SelectField(u'Script', coerce=int, validators=[InputRequired()], id='sel_script')
    connector=StringField(_l('Connector'))
    send = SubmitField(_l('Send'))


class StatbyTimeForm(FlaskForm):

    daterange = StringField(_l('Daterange'))
    submit = SubmitField(_l('Submit'))
    create = SubmitField(_l('Create'))


class TemplateForm(FlaskForm):
    name=SelectField(u'Template', coerce=int, validators=[InputRequired()], id='sel_template')
    submit = SubmitField(_l('Submit'))

class JournalForm(FlaskForm):
    description=StringField(_l('Description'))
    body=TextAreaField(_l('Body'))
    submit_journal = SubmitField(_l('Submit'))



    
    
