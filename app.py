import os
from api.customer_api import CustomerApi, CustomersApi
from config.init import api, app, db

if os.path.exists("config/customer.db"):
    os.remove("config/customer.db")

db.create_all()
db.session.commit()

api.add_resource(CustomerApi, '/api/v1/customer/<int:customer_id>', '/api/v1/customer')
api.add_resource(CustomersApi, '/api/v1/customers')

if __name__ == "__main__":
    app.run(host="localhost", port=9091)
