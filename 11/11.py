from flask import Flask, render_template, request, url_for
import os

app = Flask(__name__)


@app.route('/')
def main_route():
    return ''


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    params = {
        'title': 'Галерея с загрузкой',
    }
    for current_dir, dirs, files in os.walk(os.path.join('static', 'img')):
        for i in range(len(files)):
            files[i] = url_for('static', filename=f'img/{files[i]}')
        params['files'] = files
    if request.method == 'GET':
        return render_template(template_name_or_list='content.html', **params)
    elif request.method == 'POST':
        get_file = request.files['file']
        new_file = get_file.filename
        try:
            with open(f'static/img/{new_file}', 'wb') as file:
                file.write(get_file.read())
        except Exception:
            return render_template(template_name_or_list='content.html', **params)

        for current_dir, dirs, files in os.walk(os.path.join('static', 'img')):
            for i in range(len(files)):
                files[i] = url_for('static', filename=f'img/{files[i]}')
            params['files'] = files
        return render_template(template_name_or_list='content.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
