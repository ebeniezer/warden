from flask_wtf import Form
from wtforms import SubmitField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired


class ServiceNew(Form):
    service_name = StringField('Service Name', validators=[DataRequired()])

    docs = BooleanField('docs')
    in_production = BooleanField('In production')
    owner = StringField('Owner')
    git_source = StringField('Git Source')
    submit = SubmitField('Add Service')