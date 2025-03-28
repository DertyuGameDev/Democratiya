from requests import get, post, put, delete

#сначала запустить сервак, потом тесты
print('1:', get('http://127.0.0.1:8080/api/get_all_users').json())  # получение всех юзеров
print('2:', get('http://127.0.0.1:8080/api/get_one_users/1').json())  # получение одного юзера

print('3:', post('http://127.0.0.1:8080/api/add_user',
                 json={"email": "6@6", "password": "6", "name": "lox3", "surname": "lox3",
                       "age": 17, "address": "дебри", "position": "position",
                       "speciality": "speciality", "city": "Кострома"}))  # добавление пользователя
#
print('4:', put('http://127.0.0.1:8080/api/edit_user/6',
                json={"name": "лох7", "surname": "лох7",
                      "age": 18, "address": "дебри", "position": "position",
                      "speciality": "speciality"}).text)  # редактирование пользователя

print('5:', delete("http://127.0.0.1:8080/api/user_delete/6").text)
