import flask
from flask import jsonify, make_response, request
from data.job import Jobs
from data import db_session

"""
'api_jobs' – имя Blueprint
__name__ – имя исполняемого модуля, относительно которого будут искаться все необходимые каталоги
template_folder – подкаталог для шаблонов данного Blueprint 
(необязательный параметр, при его отсутствии берется подкаталог шаблонов приложения)
"""

blueprint = flask.Blueprint('api_jobs', __name__, template_folder='templates')


@blueprint.route('/api/get_all_jobs', methods=['GET'])
def get_jobs():
    """если в only нужно токо один аргумент, то запятую после него поставить"""
    db_sess = db_session.create_session()
    jobs_data = db_sess.query(Jobs).all()

    for i in range(len(jobs_data)):
        jobs_data[i] = jobs_data[i].to_dict(
            only=("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))

    return jsonify(jobs_data)


@blueprint.route('/api/get_one_jobs/<int:job_id>')
def api_one_jobs(job_id):
    db_sess = db_session.create_session()
    jobs_data = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not jobs_data:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    return jsonify({'jobs': jobs_data.to_dict(
        only=("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))})


@blueprint.route('/api/create_jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        is_finished=request.json['is_finished'],
        collaborators=request.json['collaborators']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id, 'team_leader': jobs.team_leader, 'job': jobs.job, 'work_size': jobs.work_size,
                    'collaborators': jobs.collaborators, 'start_date': jobs.start_date, 'end_date': jobs.end_date,
                    'is_finished': jobs.is_finished})


@blueprint.route('/api/edit_jobs/<int:job_id>', methods=['PUT'])
def edit_jobs(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    obj_job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not obj_job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    obj_job.team_leader = request.json['team_leader']
    obj_job.job = request.json['job']
    obj_job.work_size = request.json['work_size']
    obj_job.collaborators = request.json['collaborators']
    obj_job.is_finished = request.json['is_finished']

    db_sess.commit()

    return jsonify(
        {'id': obj_job.id, 'team_leader': obj_job.team_leader, 'job': obj_job.job, 'work_size': obj_job.work_size,
         'collaborators': obj_job.collaborators, 'start_date': obj_job.start_date, 'end_date': obj_job.end_date,
         'is_finished': obj_job.is_finished})


@blueprint.route('/api/job_delete/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(job_id)
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})
