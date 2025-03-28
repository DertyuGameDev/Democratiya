import datetime

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Login / Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat Password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    age = StringField("Age", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city_from = StringField("City", validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobsForm(FlaskForm):
    team_leader = IntegerField("Team Leader id", validators=[DataRequired()])
    job = StringField("Job Title", validators=[DataRequired()])
    work_size = IntegerField("Work Size", validators=[DataRequired()])
    collaborators = StringField("Collaborators")
    start_date = DateField("Start Date", default=datetime.datetime.now)
    end_date = DateField("End Date", default=datetime.datetime.now)
    is_finished = BooleanField("Is job finished?", default=False)
    submit = SubmitField("Отправить")
