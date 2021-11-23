from db.database import db
from models.models import Performance, User,Card,Deck,Result
from sqlalchemy import *
import hashlib
import random




def sha3512(password):
    m = hashlib.sha3_512()
    m.update(password.encode("utf-8"))
    return str(m.hexdigest())


def add_user(username,password):
    password_hash = sha3512(password)
    #print(password_hash)
    new_user = User(username = username,password_hash = password_hash)
    db.session.add(new_user)
    db.session.commit()
    user_id = db.session.query(User.user_id).filter(User.username==username).first()[0]
    db.session.close()
    return user_id


def user_exists(username):
    user = db.session.query(User).filter(User.username==username).first()
    if user == None:
        return False
    else:
        return True

def authenticate_user(username,password):
    password_hash = sha3512(password)
    #print("password hash = {}".format(password_hash))
    user = db.session.query(User).filter(User.username==username,User.password_hash==password_hash).first()
    if user == None:
        return False
    else:
        return True
def get_user_id(username):
    user_id = db.session.query(User.user_id).filter(User.username==username).first()[0]
    db.session.close()
    return user_id


def add_card(question,answer,deck_id):
    new_card = Card(question = question,answer = answer,deck_id=deck_id)
    db.session.add(new_card)
    db.session.commit()

def delete_card(card_id):
    db.session.query(Card).filter(Card.card_id==card_id).delete()
    db.session.commit()
    db.session.close()

def get_card(card_id):
    card = db.session.query(Card).filter(Card.card_id==card_id).first()
    db.session.close()
    return card.card_id,card.question,card.answer

def get_cards(deck_id):
    cards = [(card.card_id,card.question,card.answer) for card in db.session.query(Card).filter(Card.deck_id==deck_id).all()]
    print(cards)
    return cards

def add_deck(name,description):
    new_deck = Deck(name = name,description=description)
    db.session.add(new_deck)
    db.session.commit()

def update_deck(deck_id,name,description):
    db.session.query(Deck).filter(Deck.deck_id==deck_id).update({"name":name,"description":description})
    db.session.commit()

def delete_deck(deck_id):
    db.session.query(Deck).filter(Deck.deck_id==deck_id).delete()
    db.session.commit()
    db.session.close()


def get_decks():
    decks = [(deck.deck_id,deck.name,deck.description) for deck in db.session.query(Deck).all()]
    print(decks[0])
    return decks



def get_deck(deck_id):
    deck = [(deck.deck_id,deck.name,deck.description) for deck in db.session.query(Deck).filter(Deck.deck_id==deck_id).all()][0]
    return deck

def option_gen(cards):
    data = []
    with open('data/wordlist.txt') as f:
        W = f.readlines()
        n = len(W)
    for card in cards:
        options = [card[2]]
        while len(options) < 4:
            idx = random.randint(0,n-1)
            print(idx)
            if W[idx] not in options and W[idx]:
                options.append(W[idx])
        random.shuffle(options)
        data.append((card,options))
    return data

def get_result(user_id):
    score = sum([x[5] for x in db.session.query(Result).filter(Result.user_id==user_id,Result.score==1).all()])
    n = len(db.session.query(Result).filter(Result.user_id==user_id).all())
    points = (score/n)*100
    wrong_cards = db.session.query(Result).filter(Result.user_id==user_id,Result.score==0).all()
    db.session.close()
    return points

def update_performance(user_id,card_id,deck_id,score):
    new_performance = Performance(user_id=user_id,card_id=card_id,deck_id=deck_id,score=score)
    db.session.add(new_performance)
    db.session.commit()
    db.session.close()

def update_result(user_id,card_id,answer,submission,score):
    new_result = Result(user_id=user_id,card_id=card_id,answer=answer,submission=submission,score=score)
    db.session.add(new_result)
    db.session.commit()
    db.session.close()

def reset_result():
    db.session.query(Result).delete()
    db.session.commit()
    db.session.close()