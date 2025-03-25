from data import db_session
from data.user import User
from flask import Flask, render_template, redirect
from data.form_file import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init('db/register.db')


@app.route('/', methods=["GET", "POST"])
def main_route():
    return ""


@app.route('/login')
def login():
    return render_template('login.html')


def make_registration(db_sess, form):
    user = User(
        email=form.email.data,
        hashed_password=form.password.data,
        surname=form.surname.data,
        name=form.name.data,
        age=form.age.data,
        position=form.position.data,
        speciality=form.speciality.data,
        address=form.address.data
    )
    user.set_password(form.password.data)
    db_sess.add(user)
    db_sess.commit()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            age = int(form.age.data)
        except ValueError:
            return render_template('content.html', title='Регистрация',
                                   form=form, message="Возраст не число")
        if not (3 <= age <= 120):
            return render_template('content.html', title='Регистрация',
                                   form=form, message="Че с возрастом??")
        if form.password.data != form.password_again.data:
            return render_template('content.html', title='Регистрация',
                                   form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('content.html', title='Регистрация',
                                   form=form, message="Такой пользователь уже есть")

        make_registration(db_sess=db_sess, form=form)
        return redirect('/login')
    return render_template('content.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
