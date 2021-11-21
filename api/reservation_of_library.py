from flask_restful import Resource
from flask import jsonify,request,session
from shared_db import db

from models.models import Reservation,Stock


# gets list of users reservation
# todo session
class ReservationOfLibraryRes(Resource):

    def get(self, library_id):
        #todo - moze to iba librarian - mozno aj admin?????
        # if not session['user_id']:  # no session - no one is logged
        #     return "nenenene"

        # ziskanie pola stock id ktore su napojene na library
        # potom query na reservations ktore su napojene na tieto stocks
        # todo otestovat

        #get id of stock of library - array of ids
        stock_id = Stock.query.with_entities(Stock.id).filter_by(library_id = library_id).all()
        print(stock_id)
        stock_id_array = []
        for id in stock_id:
            stock_id_array.append(id[0])



        #big brain time query
        reservations = Reservation.query.filter(Reservation.stock_id.in_(stock_id_array)).all()

        array = []
        for row in reservations:
            row = row.__dict__
            del row["_sa_instance_state"]
            array.append(row)

        return jsonify(array)


