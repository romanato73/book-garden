# Confirm reservation - Librarian/Admin
# from flask_restful import Resource
from api.masterclass import MasterResource
from flask import jsonify,request,session
from shared_db import db

from models.models import Reservation,Borrowing


class ReservationConfirmRes(MasterResource):

    # Confirm the reservation
    # Can be done by Admin and Librarian
    def get(self, id):  # TODO mozno GET/nieco ine?

        # if not ('user_id' in session and (session['user_type'] == 5 or session['user_type'] == 4)):
        #     return self.response_error("Action not allowed for current session!")

        if not (self.is_logged() and (self.is_admin() or self.is_librarian())):
            return self.response_error("Action not allowed for current session!")

        reservation = Reservation.query.filter_by(id=id).first()
        if reservation:
            # Librarian can confirm only reservations in his/her library
            if self.is_librarian():
                lib = self.stock_in_which_lib(reservation.stock_id)
                # TODO toto sa Romana opytat ci mi posle lib_id alebo ne
                # if lib != lib_id:
                #     return self.response_error("Missing permissions!")

            person_id = reservation.person_id
            stock_id = reservation.stock_id
            # Change stock count
            if not self.take_from_stock(stock_id):
                return self.response_error("Stock empty!")
            # Create borrowing
            db.session.add(Borrowing(stock_id=stock_id, person_id=person_id))
            # Delete reservation
            Reservation.query.filter_by(id=id).delete()
            db.session.commit()
            # Change stock count
            return self.response_ok({})  # TODO idk ako a ci vobec
        else:
            return self.response_error("Not in DB!")
