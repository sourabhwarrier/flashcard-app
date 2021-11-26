from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Column, ForeignKey
from db.database import db

class User(db.Model):
    __tablename__ = "users"
    user_id = Column(db.Integer,primary_key=True,autoincrement=True)
    username = Column(db.String,unique=True,nullable=False)
    password_hash = Column(db.String,nullable=False)

class Card(db.Model):
    __tablename__ = "cards"
    card_id = Column(db.Integer,primary_key=True,autoincrement=True)
    question = Column(db.String,nullable=False)
    answer = Column(db.String,nullable=False)
    deck_id = Column(db.Integer, db.ForeignKey("decks.deck_id"),nullable=False)

class Deck(db.Model):
    __tablename__ = "decks"
    deck_id = Column(db.Integer,primary_key=True,autoincrement=True)
    name = Column(db.String,nullable=False)
    description = Column(db.String,nullable=False)

class Rating(db.Model):
    __tablename__ = "ratings"
    rating_id = Column(db.Integer,primary_key=True,autoincrement=True)
    deck_id = Column(db.String,db.ForeignKey("decks.deck_id"),nullable=False)
    rating = Column(db.String,nullable=False)

class Performance(db.Model):
    __tablename__ = "performances"
    performance_id = Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = Column(db.Integer, db.ForeignKey("users.user_id"),nullable=False)
    card_id = Column(db.Integer, db.ForeignKey("cards.card_id"),nullable=False)
    deck_id = Column(db.Integer, db.ForeignKey("decks.deck_id"),nullable=False)
    score = Column(db.Integer,nullable=False)
class Result(db.Model):
    __tablename__ = "results"
    result_id = Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = Column(db.Integer, db.ForeignKey("users.user_id"),nullable=False)
    card_id = Column(db.Integer, db.ForeignKey("cards.card_id"),nullable=False)
    answer = Column(db.String,nullable=False)
    submission = Column(db.String,nullable=False)
    score = Column(db.Integer,nullable=False)

class Misc(db.Model):
    __tablename__ = "misc"
    misc_id = Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = Column(db.Integer, db.ForeignKey("users.user_id"),nullable=False)
    deck_id = Column(db.Integer, db.ForeignKey("decks.deck_id"),nullable=False)
    last_time = Column(db.String,nullable=False)

