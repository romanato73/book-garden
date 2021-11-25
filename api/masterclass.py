from flask import jsonify,session
from flask_restful import Resource
from shared_db import db

from models.models import Stock


class MasterResource(Resource):  # subclass

    def response_error(self, message):
        return jsonify({'status': 'error', 'message': message})

    def response_ok(self, data):
        return jsonify({'status': 'success', 'data': data})

    def add_to_stock(self, stock_id, amount):  # TODO zaporny amount je possible?
        stock = Stock.query.filter_by(id=stock_id).first()
        # TODO mam kontrolovat ci existuje stock ci fck it?
        stock.amount = stock.amount + amount
        db.session.commit()
        #return True

    def take_from_stock(self, stock_id):
        stock = Stock.query.filter_by(id=stock_id).first()
        if stock.amount > 0:  # there are books on stock
            stock.amount = stock.amount - 1
            db.session.commit()
            return True
        else:
            return False  # Not possible to subtract

    def make_stock_availiable(self, stock):
        stock.availability = True
        # TODO Remove votes here
        db.session.commit()

    def stock_in_which_lib(self, stock_id):
        stock = Stock.query.filter_by(id=stock_id).first()
        if stock:  # in some cases it is "guaranteed" the stock exists (if admin didnt break something)
            return stock.library_id
        else:
            return None


    # Session control #
    def is_admin(self):
        if session['user_type'] == 5:
            return True
        else:
            return False

    def is_librarian(self):
        if session['user_type'] == 4:
            return True
        else:
            return False

    def is_distributor(self):
        if session['user_type'] == 3:
            return True
        else:
            return False

    def is_user(self, user_id):  # Regular user can ask for his info only
        if session['user_id'] == user_id:
            return True
        else:
            return False

    def is_logged(self):
        if 'user_id' in session:
            return True
        else:
            return False
