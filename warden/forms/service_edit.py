from flask_wtf import Form
from sqlalchemy import distinct, exists, select
from wtforms import StringField, SubmitField, BooleanField, SelectField, validators
from wtforms.validators import DataRequired

class ServiceEdit(Form):
    name = StringField('Name', validators=[DataRequired()])
    in_production = BooleanField('Is In Production')
    docs = BooleanField('Where Docs')
    owner = StringField('Owner', validators=[DataRequired()])
    submit = SubmitField('Save')