from data import db_session
from flask import Flask, render_template, redirect, abort, request
from data.forms import LoginForm, RegisterForm, JobsForm
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from data.user import User
from data.job import Jobs

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init('db/test.db')


@app.route('/', methods=["GET", "POST"])
def main_route():
    db_sess = db_session.create_session()
    jobs_data = db_sess.query(Jobs).all()
    return render_template('base_with_btn.html', jobs_data=jobs_data)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


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
        if form.password.data != form.password_again.data:
            return render_template('content.html', title='Регистрация',
                                   form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('content.html', title='Регистрация',
                                   form=form, message="Такой пользователь уже есть")

        make_registration(db_sess=db_sess, form=form)
        return redirect('/')
    return render_template('content.html', title='Регистрация', form=form)


@app.route("/addjob", methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.team_leader.data).first():
            return render_template(template_name_or_list="job.html", form=form, title="Adding a job")
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data

        db_sess.add(job)
        db_sess.commit()

        return redirect("/")
    return render_template(template_name_or_list="job.html", form=form, title="Adding a job", text="Adding a Job")


@app.route('/jobs_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_edit(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job_check = db_sess.query(Jobs).filter(Jobs.id == id).filter(
            ((Jobs.team_leader == current_user.id) | (current_user.id == 1))).first()

        if job_check:
            form.job.data = job_check.job
            form.team_leader.data = job_check.team_leader
            form.work_size.data = job_check.work_size
            form.collaborators.data = job_check.collaborators
            form.is_finished.data = job_check.is_finished
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job_obj = db_sess.query(Jobs).filter(Jobs.id == id).filter(
            ((Jobs.team_leader == current_user.id) | (current_user.id == 1))).first()

        if job_obj:
            job_obj.job = form.job.data
            job_obj.team_leader = form.team_leader.data
            job_obj.work_size = form.work_size.data
            job_obj.collaborators = form.collaborators.data
            job_obj.is_finished = form.is_finished.data
            db_sess.merge(job_obj)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html',
                           title='Редактирование работы', form=form, text='Edit jobs')


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).filter(
        ((Jobs.team_leader == current_user.id) | (current_user.id == 1))).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
