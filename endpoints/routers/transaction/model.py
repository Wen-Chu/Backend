from endpoints import DB

class Transaction(DB.Model):
    __tablename__ = 'transaction'
    id = DB.Column(DB.Integer, primary_key=True)
    customer_id = DB.Column(DB.Integer, DB.ForeignKey('customer.id'), nullable=False)
    trans_type = DB.Column(DB.String(10), nullable=False)
    amount = DB.Column(DB.Integer, nullable=False)
    balance = DB.Column(DB.Integer, nullable=False)
    timestamp = DB.Column(DB.DateTime, server_default=DB.func.now())