import flask
from flask import jsonify
from .job import Jobs
from . import db_session

blueprint = flask.Blueprint('api_handlers', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def api_jobs():
    db_sess = db_session.create_session()
    jobs_data = db_sess.query(Jobs).all()

    for i in range(len(jobs_data)):
        jobs_data[i] = jobs_data[i].to_dict(
            only=("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))

    return jsonify(jobs_data)
