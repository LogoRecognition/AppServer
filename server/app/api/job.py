# coding=utf-8
"""Deal with job-related APIs."""
from flask import request
from flask_restplus import Namespace, Resource
from flask_login import login_required, current_user
from ..model import jobs
from .utils import get_message_json, handle_internal_error, HTTPStatus, ConstantCodes

api = Namespace('jobs')


@api.route('/<int:job_id>')
class JobResource(Resource):
    """Deal with single job."""

    @login_required
    def get(self, job_id):
        """Retrieve a single job by id."""
        try:
            result = jobs.find_job_by_id(job_id)
        except Exception as err:
            return handle_internal_error(str(err))

        if len(result) == 1:
            result = result[0]
        else:
            return get_message_json('任务不存在'), HTTPStatus.NOT_FOUND

        # Admin can retrieve any job,
        # while others can only retrieve his own job
        if not current_user.is_admin() and result.account_id != current_user.account_id:
            return get_message_json('用户无法访问他人任务'), HTTPStatus.FORBIDDEN

        json_res = result.to_json()
        json_res['message'] = '成功查看任务'
        return json_res, HTTPStatus.OK

    @login_required
    @api.doc(parser=api.parser()
             .add_argument('body', type=str, required=True, help='json', location='json')
            )
    def put(self, job_id):
        """Edit a single job by id."""
        form = request.form
        if form['account_id'] != current_user.account_id:
            return get_message_json('用户无法修改他人任务'), HTTPStatus.FORBIDDEN
        try:
            previous_job = jobs.find_job_by_id(job_id)
            if len(previous_job) == 1:
                previous_job = previous_job[0]
            else:
                return get_message_json('任务不存在'), HTTPStatus.NOT_FOUND

            if previous_job.job_state == ConstantCodes.Finished:
                return get_message_json('用户无法修改已完成的任务'), HTTPStatus.FORBIDDEN

            result = jobs.update_job_by_id(
                job_id,
                form['image_id'],
                form['account_id'],
                form['label_id'],
                form['job_state'],
                form['finished_date']
            )
            if result == 1:
                json_res = form.copy()
                json_res['message'] = '成功编辑任务'
                return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))

    @login_required
    def delete(self, job_id):
        """Delete a single job by id."""
        # Only admin can delete any job
        if not current_user.is_admin():
            return get_message_json('删除任务需要管理员权限'), HTTPStatus.FORBIDDEN

        try:
            result = jobs.delete_job_by_id(job_id)
            if result == 1:
                return get_message_json('已删除该任务'), HTTPStatus.OK
            else:
                return get_message_json('任务不存在'), HTTPStatus.NOT_FOUND
        except Exception as err:
            return handle_internal_error(str(err))


@api.route('/')
class JobsCollectionResource(Resource):
    """Deal with collection of jobs."""

    @login_required
    @api.doc(params={'account_id': 'account id'})
    def get(self):
        """List all jobs."""
        # account_id is an optional argument
        account_id = int(request.args.get('account_id'))
        if not current_user.is_admin()\
                and (account_id is None or account_id != current_user.account_id):
            return get_message_json('用户无法访问其他用户的任务列表')

        try:
            result = jobs.find_all_jobs(account_id)

            data = []
            for job in result:
                data.append(job.to_json())
            json_res = {
                'message': '成功获取所有任务',
                'data': data
            }
            return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))

    @login_required
    @api.doc(parser=api.parser()
             .add_argument('body', type=str, required=True, help='json', location='json')
            )
    def post(self):
        """Create a job."""
        form = request.form
        # Only admin can create jobs
        if not current_user.is_admin():
            return get_message_json('创建任务需要管理员权限'), HTTPStatus.FORBIDDEN
        
        try:
            result = jobs.add_job(
                form['image_id'],
                form['account_id']
            )
            json_res = result.to_json()
            json_res['message'] = '任务创建成功'

            return json_res, HTTPStatus.CREATED
        except Exception as err:
            return handle_internal_error(str(err))
