from flask_restful import abort, Resource
from flask import jsonify
from . import db_session
from .user import User
from .user_parser import parser


def abort_if_users_not_found(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == user_id).first()
    if not users:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == user_id).first()
        return jsonify({'users': users.to_dict(
            only=("id", "surname", "name", "age", "position", "speciality", "address", "email", "modified_date"))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()

        for elem in user.job_relationship:
            db_sess.delete(elem)

        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        for i in range(len(users)):
            users[i] = users[i].to_dict(
                only=("id", "surname", "name", "age", "position", "speciality",
                      "address", "email", "city_from", "modified_date"))
        return jsonify(users)

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == args["email"]).first():
            return jsonify({'Fail: The mail already exists': 'Error'})

        user = User(
            surname=args["surname"],
            name=args["name"],
            age=args["age"],
            position=args["position"],
            speciality=args["speciality"],
            address=args["address"],
            email=args["email"],
            city_from=args["city"],
            hashed_password=args["password"]
        )

        user.set_password(user.hashed_password)
        db_sess.add(user)
        db_sess.commit()
        return jsonify(
            {"id": user.id, "surname": user.surname, "name": user.name, "age": user.age, "position": user.position,
             "speciality": user.speciality, "address": user.address, "email": user.email})
