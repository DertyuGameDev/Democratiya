from data import db_session
from data.user import User


def add_mans(surname, name, age, position, speciality, address, email, db_sess):
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email
    db_sess.add(user)


db_session.global_init('db/info.sqlite')
db_sess = db_session.create_session()
add_mans(surname='Scott', name='Ridley', age=21, position='captain', speciality='research engineer',
         address='module_1', email='scott_chief@mars.org', db_sess=db_sess)
add_mans(surname='Adrianova', name='Alla', age=25, position='colonist',
         speciality='research engineer', address='module_2', email='alla@mars.org', db_sess=db_sess)
add_mans(surname='Larionov', name='Valera', age=17, position='colonist',
         speciality='research engineer', address='module_3', email='valera@mars.org', db_sess=db_sess)
add_mans(surname='Motovilov', name='Gregory', age=16, position='colonist',
         speciality='research engineer', address='module_4', email='gregory@mars.org', db_sess=db_sess)
add_mans(surname='Saharov', name='Ilya', age=15, position='colonist',
         speciality='research engineer', address='module_5', email='ilya@mars.org', db_sess=db_sess)
db_sess.commit()
