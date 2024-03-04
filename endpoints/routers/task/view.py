from flask_restful import Resource, reqparse
from endpoints.routers.task.model import Task
from flask_jwt_extended import jwt_required, get_jwt_identity
from endpoints import DB
from datetime import datetime

class task(Resource):
    @jwt_required()
    def get(self, task_id=None):
        try:
            if not task_id:
                tasks = Task.query.all()
                if len(tasks) == 0:
                    return {"error": "No task"}, 404
                task_data = []
                for task in tasks:
                    task_data.append({"id": task.id, "admin_name": task.admin_name, "task_name": task.task_name,
                                      "status": task.status, "created_at": task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                      "last_updated": task.last_updated.strftime('%Y-%m-%d %H:%M:%S')})
            else:
                task = Task.query.filter_by(id=task_id).first()
                if not task:
                    return {"error": "Task not found"}, 404
                task_data = {"id": task.id, "admin_name": task.admin_name, "task_name": task.task_name,
                             "status": task.status, "created_at": task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                             "last_updated": task.last_updated.strftime('%Y-%m-%d %H:%M:%S')}
            return task_data, 200
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500

    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('task_name', required=True, type=str, help="task_name cannot be blank.")
            parser.add_argument('status', type=int, nullable=True, default=0)
            args = parser.parse_args()
            new_task = Task(admin_name=get_jwt_identity(), task_name=args['task_name'], status=args['status'],
                            created_at=datetime.now(), last_updated=datetime.now())
            DB.session.add(new_task)
            DB.session.commit()
            return {"message": "Task created successfully"}, 200
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500

    @jwt_required()
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('task_id', required=True, type=int, help="task_id cannot be blank.")
            parser.add_argument('task_name', required=True, type=str, help="task_name cannot be blank.")
            parser.add_argument('status', required=True, type=int, help="status cannot be blank.")
            args = parser.parse_args()
            task = Task.query.filter_by(id=args['task_id']).first()
            if not task:
                return {"error": "Task not found"}, 404
            task.task_name = args['task_name']
            task.status = args['status']
            task.last_updated = datetime.now()
            DB.session.commit()
            return {"message": "Task updated successfully"}, 200
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500

    @jwt_required()
    def delete(self, task_id):
        try:
            task = Task.query.filter_by(id=task_id).first()
            if not task:
                return {"error": "Task not found"}, 404
            DB.session.delete(task)
            DB.session.commit()
            return {"message": "Task deleted successfully"}, 200
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500