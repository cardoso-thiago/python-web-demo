from flask_restful import Resource
from flask import make_response, abort, request, jsonify
from config.init import db
from model.customer import Customer, CustomerSchema
from marshmallow import ValidationError


class CustomerApi(Resource):

    @staticmethod
    def get(customer_id):
        customer = Customer.query.filter(Customer.customer_id == customer_id).one_or_none()
        if customer is not None:
            customer_schema = CustomerSchema()
            data = customer_schema.dump(customer)
            return data
        else:
            abort(404, "Cliente não encontrado para o id: {customer_id}".format(customer_id=customer_id))

    @staticmethod
    def post():
        schema = CustomerSchema()
        try:
            new_customer = schema.load(request.json, session=db.session)
            existing_customer = (Customer.query.filter(Customer.document == new_customer.document)
                                 .one_or_none())
            if existing_customer is None:
                db.session.add(new_customer)
                db.session.commit()
                data = schema.dump(new_customer)
                return data, 201
            else:
                abort(409, "O cliente com o documento {document} já existe".format(document=existing_customer.document))
        except ValidationError as err:
            abort(400, err.messages)

    @staticmethod
    def patch(customer_id):
        schema = CustomerSchema()
        update_customer = schema.load(request.json, session=db.session, partial=True)
        existing_customer = (Customer.query.filter(Customer.customer_id == customer_id).one_or_none())
        existing_doc_customer = (Customer.query.filter(Customer.document == update_customer.document).one_or_none())

        if existing_customer is None:
            abort(404, "O cliente com o id {customer_id} não existe".format(customer_id=customer_id))
        elif existing_doc_customer is not None:
            abort(409, "O cliente com o documento {document} já existe".format(document=update_customer.document))
        else:
            update_customer.customer_id = customer_id
            db.session.merge(update_customer)
            db.session.commit()
            existing_customer = (Customer.query.filter(Customer.customer_id == customer_id).one_or_none())
            data = schema.dump(existing_customer)
            return data, 200

    @staticmethod
    def delete(customer_id):
        customer = Customer.query.filter(Customer.customer_id == customer_id).one_or_none()

        if customer is None:
            abort(404, "O cliente com o id {customer_id} não existe".format(customer_id=customer_id))
        else:
            db.session.delete(customer)
            db.session.commit()
            customer_schema = CustomerSchema()
            data = customer_schema.dump(customer)
            return make_response(jsonify("Cliente deletado".format(customer_id=customer_id), data), 200)


class CustomersApi(Resource):

    @staticmethod
    def get():
        customers = Customer.query.order_by(Customer.first_name).all()
        customers_schema = CustomerSchema(many=True)
        data = customers_schema.dump(customers)
        if len(data) == 0:
            return data, 204
        return data
