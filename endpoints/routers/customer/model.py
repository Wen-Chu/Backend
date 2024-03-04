from endpoints import DB

class Customer(DB.Model):
    __tablename__ = 'customer'
    id = DB.Column(DB.Integer, primary_key=True)
    customer_name = DB.Column(DB.String(20), unique=True, nullable=False)
    balance = DB.Column(DB.Integer, default=0)