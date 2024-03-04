from endpoints import DB

class Admin(DB.Model):
    __tablename__ = 'admin'
    id = DB.Column(DB.Integer, primary_key=True)
    admin_name = DB.Column(DB.String(64), unique=True, nullable=False)
    password = DB.Column(DB.String(128), nullable=False)