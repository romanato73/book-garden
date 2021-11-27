from api.masterclass import MasterResource
from flask import jsonify,request,session
from shared_db import db
from sqlalchemy.exc import IntegrityError

from models.models import BookTitle,Library,Stock

# SET response_error a response_ok
# osetrene

class BookTitleResource(MasterResource):
    def get(self,id = None):
        if id is None:
            booktitle = BookTitle.query.all()

            array = []
            for row in booktitle:
                row = row.__dict__
                del row["_sa_instance_state"]
                array.append(row)

            return self.response_ok(array)

        else:
            booktitle = BookTitle.query.filter_by(id = id).all()

            if booktitle:
                booktitle = booktitle[0].__dict__
                del booktitle["_sa_instance_state"]

            return self.response_ok(booktitle)

    # Add book to DB
    # Can be done by Admin and Distributor
    def post(self,id = None):
        if not (self.is_logged() and (self.is_admin() or self.is_distributor())):
            return self.response_error("Unauthorised action!")

        name        = request.form.get("name")
        author      = request.form.get("author")
        publisher   = request.form.get("publisher")
        isbn        = request.form.get("isbn")
        genre       = request.form.get("genre")
        description = request.form.get("description")
        rating      = request.form.get("rating")
        photo       = request.form.get("rating")
        date_publication = request.form.get("date_publication")

        try:
            booktitle = BookTitle(name        = name,
                                  author      = author,
                                  publisher   = publisher,
                                  isbn        = isbn,
                                  genre       = genre,
                                  description = description,
                                  rating      = rating,
                                  photo       = photo,
                                  date_publication = date_publication)

            db.session.add(booktitle)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            return self.response_error("Database refused push (check if ISBN is unique)!" + '\n' + e.orig.diag.message_detail)  # TODO

        # autostock
        libraries = Library.query.all()
        if not libraries:
            return

        for row in libraries:
            row = row.__dict__
            stock = Stock(library_id=row["id"], booktitle_id=booktitle.id, amount=0)
            db.session.add(stock)

        db.session.commit()

        return self.response_ok("Committed to db")

    # Delete a book from DB
    # Can be done by Admin
    def delete(self, id):

        if not (self.is_logged() and self.is_admin()):
            return self.response_error("Unauthorised action!")

        BookTitle.query.filter_by(id=id).delete()
        db.session.commit()

        return self.response_ok("Committed to db")

    # Update any book
    # Can be done by Admin and Distributor
    def put(self,id):

        if not (self.is_logged() and (self.is_admin() or self.is_distributor())):
            return self.response_error("Unauthorised action!")

        booktitle = BookTitle.query.filter_by(id=id).first()

        if not booktitle:
            return self.response_error("Booktitle doesnt exist")

        name        = request.form.get("name")
        author      = request.form.get("author")
        publisher   = request.form.get("publisher")
        isbn        = request.form.get("isbn")
        genre       = request.form.get("genre")
        description = request.form.get("description")
        rating      = request.form.get("rating")
        photo       = request.form.get("rating")
        date_publication = request.form.get("date_publication")

        try:
            booktitle.name        = name
            booktitle.author      = author
            booktitle.publisher   = publisher
            booktitle.isbn        = isbn
            booktitle.genre       = genre
            booktitle.description = description
            booktitle.rating      = rating
            booktitle.photo       = photo
            booktitle.date_publication = date_publication

            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            return self.response_error(e.orig.diag.message_detail)

        return self.response_ok("Committed to db")

