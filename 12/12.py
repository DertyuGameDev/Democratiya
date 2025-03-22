from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def main_route():
    return ''


@app.route('/member')
def member():
    with open('templates/js.json', mode='r', encoding='utf8') as f:
        data = json.load(f)
    params = {
        'title': 'Личная карточка',
        'data': data
    }
    return render_template(template_name_or_list='content.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
