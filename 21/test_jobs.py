from requests import get, post, put, delete

print("1:", get('http://127.0.0.1:8080/api/v2/jobs').text)  # корректный запрос на получение всех работ

print("2:", get('http://127.0.0.1:8080/api/v2/lox').text)  # некорректный запрос на получение всех работ (из-за путя)

print("3:", get('http://127.0.0.1:8080/api/v2/jobs/2').text)  # корректный запрос на получение одной работы

print("4:", get('http://127.0.0.1:8080/api/v2/jobs/235235235').text)  # некорректный запрос на получение одной работы

print("5:", post('http://127.0.0.1:8080/api/v2/jobs',
                 json={"team_leader": 1, "work_size": 15, "finish": True, "collaborators": "2",
                       "title": "бесполезная работа"}).text)  # корректный запрос

print("6:", post('http://127.0.0.1:8080/api/v2/jobs',
                 json={"team_leader": 1, "work_size": 15}).text)  # некорректный запрос, не указаны все данные

print("7:", delete("http://127.0.0.1:8080/api/v2/jobs/6").text)  # корректное удаление

print("8:", delete("http://127.0.0.1:8080/api/v2/jobs/6").text)  # некорректное удаление, нет уже работы больше

print("9:", put("http://127.0.0.1:8080/api/v2/jobs/5",
                json={"team_leader": 1, "title": "хрен хреныч", "work_size": 10,
                      "collaborators": "2", "finish": True}).text)  # корректное редактирование работы

print("10:", put("http://127.0.0.1:8080/api/v2/jobs/5", json={}).text)  # некорректное редактирование работы
