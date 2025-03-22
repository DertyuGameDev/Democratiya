import os

from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/')
def main():
    return ''


@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    if request.method == 'GET':
        # Путь к изображению
        img_path = 'static/img/absd.png'  # Путь к изображению
        # Если файл существует, используем его, иначе используем изображение по умолчанию
        if os.path.exists(img_path):
            nam = 'absd.png'
        else:
            nam = 'man.png'

        # Формируем HTML страницу
        return f'''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                         <link rel="stylesheet"
                         href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                         integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                         crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" 
                        href="{url_for('static', filename='css/style.css')}" />
                        <title>Отбор астронавтов</title>
                      </head>
                    <body>
                        <h2 class="h">Загрузка фотографии</h2>
                        <h3 class="h">для участия в миссиях</h3>
                        <div>
                            <form class="form-login" method="post" enctype="multipart/form-data">
                                <div class="form-group">
                                    <div>
                                        <label for="photo">Выберите файл</label>
                                        <input accept=".png,.jpg" type="file" class="form-control-file" 
                                        id="photo" name="file">
                                    </div>
                                    <img src="{url_for('static', filename=f'img/{nam}')}" />
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                        </div>
                    </body>
                      </html>'''

    elif request.method == 'POST':
        new_file = 'absd.png'  # Имя загружаемого файла
        f = request.files['file']
        # Сохраняем изображение на сервер
        with open(f'static/img/{new_file}', 'wb') as file:
            file.write(f.read())

        # Отправляем HTML с отображением загруженной фотографии
        return f'''<!doctype html>
                <html lang="en">
                 <head>
                    <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, 
                           shrink-to-fit=no">
                             <link rel="stylesheet"
                               href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                  crossorigin="anonymous">
                                   <link rel="stylesheet" type="text/css" 
                                    href="{url_for('static', filename='css/style.css')}" />
                                    <title>Отбор астронавтов</title>
                                  </head>
                                <body>
                                    <h2 class="h">Вот ваше фото!</h2>
                                    <div class="center_image">
                                        <img src="{url_for("static", filename=f"img/{new_file}")}" />
                                    </div>
                                </body>
                                  </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
