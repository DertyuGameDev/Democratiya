from data import db_session
from data.user import User
from data.job import Jobs
from data.departments import Department
from data.category import Category, association_table
from flask import Flask, render_template, redirect, abort, request, make_response, jsonify
from data.forms import *
from data import users_resource, jobs_resource
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from data import jobs_api, users_api
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app, catch_all_404s=True)
login_manager = LoginManager()


def main():
    login_manager.init_app(app)
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    db_session.global_init('db/test.db')
    api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:jobs_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)


@app.route('/', methods=["GET", "POST"])
def main_route():
    db_sess = db_session.create_session()
    jobs_data = db_sess.query(Jobs).all()
    print_data = []

    data_info = db_sess.query(association_table).all()
    for elem in data_info:
        job = db_sess.query(Jobs).filter(Jobs.id == elem[0]).first()
        category = db_sess.query(Category).filter(Category.id == elem[1]).first()
        print_data.append((job, category))
    return render_template('base_with_btn.html', jobs_data=jobs_data, print_data=print_data, title="Jobs page")


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


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
    return render_template('login.html', title='Authorization', form=form)


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
            return render_template('content.html', title='Registration',
                                   form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('content.html', title='Registration',
                                   form=form, message="Такой пользователь уже есть")

        make_registration(db_sess=db_sess, form=form)
        return redirect('/')
    return render_template('content.html', title='Registration', form=form)


@app.route("/addjob", methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.team_leader.data).first():
            return render_template(template_name_or_list="job.html", form=form, title="Adding a job")

        id_category = int(form.id_category.data)
        if not db_sess.query(Category).filter(id_category == Category.id).first():
            return render_template(template_name_or_list="job.html", form=form, title="Adding a job",
                                   text="Adding a Job", message="Категории с указанном id не существует")

        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data

        category = db_sess.query(Category).filter(Category.id == form.id_category.data).first()
        job.categories_relationship.append(category)
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
        user = db_sess.query(User).filter(form.team_leader.data == User.id).first()
        if user:
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
        else:
            return render_template('job_edit.html',
                                   title='Editing a job', form=form, text='Editing a job',
                                   message="нет такого тимлида")
    return render_template('job_edit.html',
                           title='Editing a job', form=form, text='Editing a job')


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


@app.route('/departaments', methods=['GET', 'POST'])
def departments():
    db_sess = db_session.create_session()
    department_data = db_sess.query(Department).all()
    return render_template('departments.html', title='Departments', department_data=department_data)


@app.route("/adddepartments", methods=["GET", "POST"])
@login_required
def adddepartments():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            department = Department()
            department.title = form.title.data
            department.chief = form.chief.data
            department.email = form.email.data
            department.members = form.members.data

            department.user_id = user.id
            db_sess.add(department)
            db_sess.commit()
            return redirect("/")
    return render_template('work_with_departments.html', title='Departments', form=form)


@app.route('/editdepartments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep_check = db_sess.query(Department).filter(Department.id == id).filter(
            ((Department.user_id == current_user.id) | (current_user.id == 1))).first()

        if dep_check:
            form.title.data = dep_check.title
            form.chief.data = dep_check.chief
            form.members.data = dep_check.members
            form.email.data = dep_check.email
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep_obj = db_sess.query(Department).filter(Department.id == id).filter(
            ((Department.user_id == current_user.id) | (current_user.id == 1))).first()

        if dep_obj:
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user:
                dep_obj.title = form.title.data
                dep_obj.chief = form.chief.data
                dep_obj.members = form.members.data
                dep_obj.email = form.email.data
                dep_obj.user_id = user.id
                db_sess.merge(dep_obj)
                db_sess.commit()
                return redirect('/')
            return render_template('work_with_departments.html', title='Departments', form=form,
                                   message="Ошибка с почтой")
        else:
            abort(404)
    return render_template('work_with_departments.html', title='Departments', form=form)


@app.route('/deletedepartments/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id).filter(
        ((Department.user_id == current_user.id) | (current_user.id == 1))).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1', debug=True)
