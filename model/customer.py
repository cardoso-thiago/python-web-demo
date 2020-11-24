from datetime import datetime
from config.init import db, marsh


class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    document = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CustomerSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
