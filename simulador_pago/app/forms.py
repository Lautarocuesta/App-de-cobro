from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    price = FloatField('Precio', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    submit = SubmitField('Guardar')
