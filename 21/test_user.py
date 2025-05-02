from requests import get, post, delete

# сначала запустить сервак, потом тесты
print('1:', get('http://127.0.0.1:8080/api/v2/users').text)  # корректный запрос на получение всех ержанов

print('2:', get('http://127.0.0.1:8080/api/v2/users/1').text)  # корректный запрос на получение одного ержана

print('3:', post('http://127.0.0.1:8080/api/v2/users',
                 json={"email": "Alla_Mikhailovna@Alla.com", "password": "A", "name": "Alla", "surname": "Адрианова",
                       "age": 25, "address": "Делоне", "position": "хз, что писать сюда",
                       "speciality": "преподаватель", "city": "Ярославль"}).text)  # корректный запрос

print('4:', post('http://127.0.0.1:8080/api/v2/users',
                 json={"email": "Valera@Valera.com", "password": "V", "name": "Valera", "surname": "Larionov",
                       "age": 17, "address": "Дома", "position": "хз, что писать сюда",
                       "speciality": "яндекс-лицеист", "city": "Ярославль"}).text)  # корректный запрос

print('5:', post('http://127.0.0.1:8080/api/v2/users',
                 json={"email": "Motota@Motota.com", "password": "M", "name": "Гриша", "surname": "Мотовилов",
                       "age": 16, "address": "подвал", "position": "хз, что писать сюда",
                       "speciality": "лентяй", "city": "Ярославль"}).text)  # корректный запрос

print('6:', post('http://127.0.0.1:8080/api/v2/users',
                 json={"email": "Artem@Artem.com", "password": "A", "name": "Артем", "surname": "Артем",
                       "age": 16, "address": "подвал", "position": "хз, что писать сюда",
                       "speciality": "лентяй", "city": "Ярославль"}).text)  # корректный запрос

print('7:', post('http://127.0.0.1:8080/api/v2/users',
                 json={"email": "Motota@Motota.com", "password": "M", "name": "Гриша", "surname": "Мотовилов",
                       "age": 16, "address": "подвал", "position": "хз, что писать сюда",
                       "speciality": "лентяй", "city": "Ярославль"}).text)  # некорректный запрос, почта уже есть

print('8:', delete('http://127.0.0.1:8080/api/v2/users/666').text)  # такого нет

print('9:', delete('http://127.0.0.1:8080/api/v2/users/10').text)  # корректное удаление

print('10:', get('http://127.0.0.1:8080/api/v3/users').text)  # адрес неверный
