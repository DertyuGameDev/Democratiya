from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main_route():
    return ''


@app.route('/table/<string:sex>/<int:age>')
def table(sex, age):
    params = {
        'title': 'Цвет каюты',
        'sex': sex,
        'age': age
    }

    return render_template(template_name_or_list='content.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
