from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField, TextField, MultipleFileField, TextAreaField
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired, Length


class FormNewServices(FlaskForm):
    name = TextField('name')
    description = TextAreaField('description')
    price = FloatField('price')
    images = MultipleFileField('images')

    # TODO: Validate duplicated name
    @staticmethod
    def validate_name(form, field):
        if len(field.data) == 0:
            raise ValidationError("Name is required")
        if len(field.data) < 3:
            raise ValidationError("Must be greater than 3 letters")

    @staticmethod
    def validate_description(form, field):
        if len(field.data) == 0:
            raise ValidationError("Description is required")

    @staticmethod
    def validate_price(form, field):
        if len(str(field.data)) == 0:
            raise ValidationError("Price is required")
