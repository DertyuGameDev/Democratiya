from flask_restful import abort, Resource
from . import db_session
from .job import Jobs
from flask import jsonify
from .jobs_parser import parser


def abort_if_jobs_not_found(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not jobs:
        abort(404, message=f"Job {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
        return jsonify({'jobs': job.to_dict(
            only=("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
        db_sess.delete(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)

        db_sess = db_session.create_session()
        obj_job = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()

        args = parser.parse_args()
        obj_job.job = args['title']
        obj_job.team_leader = args['team_leader']
        obj_job.work_size = args["work_size"]
        obj_job.collaborators = args['collaborators']
        obj_job.is_finished = args['finish']

        db_sess.commit()

        return jsonify(
            {'id': obj_job.id, 'team_leader': obj_job.team_leader, 'job': obj_job.job, 'work_size': obj_job.work_size,
             'collaborators': obj_job.collaborators, 'start_date': obj_job.start_date, 'end_date': obj_job.end_date,
             'is_finished': obj_job.is_finished})


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        jobs_data = db_sess.query(Jobs).all()

        for i in range(len(jobs_data)):
            jobs_data[i] = jobs_data[i].to_dict(
                only=(
                    "id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))
        return jsonify(jobs_data)

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        obj_job = Jobs(
            job=args['title'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['finish']
        )
        db_sess.add(obj_job)
        db_sess.commit()

        return jsonify(
            {'id': obj_job.id, 'team_leader': obj_job.team_leader, 'job': obj_job.job, 'work_size': obj_job.work_size,
             'collaborators': obj_job.collaborators, 'start_date': obj_job.start_date, 'end_date': obj_job.end_date,
             'is_finished': obj_job.is_finished})
