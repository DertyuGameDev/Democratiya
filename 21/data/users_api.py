import flask
from flask import jsonify, make_response, request, render_template, url_for
from .user import User
from . import db_session
from .images import check_get_image

blueprint = flask.Blueprint('api_user', __name__, template_folder='templates')


@blueprint.route('/api/users_show/<int:user_id>', methods=['GET'])
def user_show(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if check_get_image(user.city_from):
        image = "image_city"
    else:
        image = "problem_city"
    params = {
        "name": user.name,
        "surname": user.surname,
        "city": user.city_from,
        'image': f"{url_for('static', filename=f'img/{image}.png')}"
    }
    return render_template(template_name_or_list='users_show.html', **params)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users_data = db_sess.query(User).all()
    if not users_data:
        return make_response(jsonify({'error': 'Not found'}), 404)

    for i in range(len(users_data)):
        users_data[i] = users_data[i].to_dict(
            only=("id", "surname", "name", "age", "position", "speciality", "address", "email", "modified_date"))
    return jsonify(users_data)


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)

    user = user.to_dict(
        only=("id", "surname", "name", "age", "position", "speciality", "address", "email", "modified_date"))

    return jsonify(user)


@blueprint.route('/api/add_user', methods=['POST'])
def add_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "position", "speciality", "address", "email", "password", "city"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User(
        surname=request.json["surname"],
        name=request.json["name"],
        age=request.json["age"],
        position=request.json["position"],
        speciality=request.json["speciality"],
        address=request.json["address"],
        email=request.json["email"],
        city_from=request.json["city"],
        hashed_password=request.json["password"]
    )
    user.set_password(user.hashed_password)
    db_sess.add(user)
    db_sess.commit()
    return jsonify(
        {"id": user.id, "surname": user.surname, "name": user.name, "age": user.age, "position": user.position,
         "speciality": user.speciality, "address": user.address, "email": user.email})


@blueprint.route('/api/edit_user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "position", "speciality", "address"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)

    user.address = request.json["address"]
    user.name = request.json["name"]
    user.speciality = request.json["speciality"]
    user.age = request.json["age"]
    user.position = request.json['position']

    user.surname = request.json["surname"]
    db_sess.commit()
    return jsonify(
        {"id": user.id, "surname": user.surname, "name": user.name, "age": user.age, "position": user.position,
         "speciality": user.speciality, "address": user.address, "email": user.email})


@blueprint.route('/api/user_delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if user_id == 1:
        return jsonify({"You can't delete the captain": "Error"})

    for elem in user.job_relationship:
        db_sess.delete(elem)

    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
