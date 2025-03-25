import sqlalchemy
from data.db_session import SqlAlchemyBase


class DataBase(SqlAlchemyBase):
    __tablename__ = 'works'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name_work = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hours = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)

