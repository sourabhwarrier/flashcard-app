from sqlalchemy.sql.schema import Column
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

