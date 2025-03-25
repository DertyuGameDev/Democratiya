from data.db_session import global_init, create_session
from data.db_file import DataBase
from flask import Flask, render_template

global_init('db/test.db')
app = Flask(__name__)


@app.route('/')
def main_route():
    db_sess = create_session()
    get_data = db_sess.query(DataBase).all()
    return render_template(template_name_or_list='content.html', get_data=get_data, title="15")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
