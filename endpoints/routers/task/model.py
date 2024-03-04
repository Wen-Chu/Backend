from endpoints import DB

class Task(DB.Model):
    __tablename__ = 'task'
    id = DB.Column(DB.Integer, primary_key=True)
    admin_name = DB.Column(DB.Integer, DB.ForeignKey('admin.admin_name'))
    task_name = DB.Column(DB.String(100))
    status = DB.Column(DB.Integer, default=0)
    created_at = DB.Column(DB.DateTime)
    last_updated = DB.Column(DB.DateTime)