from requests import get, post, delete, put

# сначала запустить сервак, потом тесты

print("1:", get('http://127.0.0.1:8080/api/get_all_jobs').json())  # все работы
print("2:", get('http://127.0.0.1:8080/api/get_one_jobs/2').json())  # одна работа
print("3:", post("http://127.0.0.1:8080/api/create_jobs",
                 json={"team_leader": 1, "job": "test_post", "work_size": 1, "collaborators": "2",
                       "is_finished": True}))  # создание работы
print("4:", put("http://127.0.0.1:8080/api/edit_jobs/11",
                json={"team_leader": 1, "job": "test_post", "work_size": 10,
                      "collaborators": "2",
                      "is_finished": True}))  # редактирование работы
print("5:", delete(('http://127.0.0.1:8080/api/job_delete/11')))  # удаление работы
