import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer)
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user_relationship = orm.relationship("User", back_populates="departament_relationship")
