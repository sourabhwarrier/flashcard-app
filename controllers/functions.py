from db.database import db
from models.models import Misc, Performance, Rating, User,Card,Deck,Result
from sqlalchemy import *
import hashlib
import random
import matplotlib.pyplot as plt
import base64
from io import BytesIO


# USER FUNCTIONS BEGIN
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
# USER FUNCTIONS END


# CARD FUNCTIONS BEGIN
def add_card(question,answer,deck_id):
    new_card = Card(question = question,answer = answer,deck_id=deck_id)
    db.session.add(new_card)
    db.session.commit()

def delete_card(card_id):
    delete_performance_by_card(card_id)
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
# CARD FUNCTIONS END



# DECK FUNCTIONS BEGIN
def get_decks():
    decks = [(deck.deck_id,deck.name,deck.description) for deck in db.session.query(Deck).all()]
    print(decks[0])
    return decks

def add_deck(name,description):
    new_deck = Deck(name = name,description=description)
    db.session.add(new_deck)
    db.session.commit()

def update_deck(deck_id,name,description):
    db.session.query(Deck).filter(Deck.deck_id==deck_id).update({"name":name,"description":description})
    db.session.commit()

def delete_deck(deck_id):
    delete_rating(deck_id)
    delete_misc_by_deck(deck_id)
    delete_performance_by_deck(deck_id)
    db.session.query(Deck).filter(Deck.deck_id==deck_id).delete()
    db.session.commit()
    db.session.close()

def get_deck(deck_id):
    deck = [(deck.deck_id,deck.name,deck.description) for deck in db.session.query(Deck).filter(Deck.deck_id==deck_id).all()][0]
    return deck
# DECK FUNCTIONS END



# RESULT FUNCTIONS BEGIN
def get_result(user_id):
    try:
        score = sum([int(x.score) for x in db.session.query(Result).filter(Result.user_id==user_id,Result.score==1).all()])
        n = len(db.session.query(Result).filter(Result.user_id==user_id).all())
        print(n)
        points = (score/n)*100
        wrong_cards = [x.card_id for x in db.session.query(Result).filter(Result.user_id==user_id,Result.score==0).all()]
        db.session.close()
        return points,wrong_cards
    except:
        return None,None


def update_result(user_id,card_id,answer,submission,score):
    new_result = Result(user_id=user_id,card_id=card_id,answer=answer,submission=submission,score=score)
    db.session.add(new_result)
    db.session.commit()
    db.session.close()

def reset_result():
    db.session.query(Result).delete()
    db.session.commit()
    db.session.close()
# RESULT FUNCTIONS END


# PERFORMANCE FUNCTIONS BEGIN
def get_performance(user_id):
    deck_ids = list(set([(x.deck_id) for x in db.session.query(Performance).filter(Performance.user_id==user_id).all()]))
    print(deck_ids)
    decks_studied = [[(x.deck_id,x.name,x.description) for x in db.session.query(Deck).filter(Deck.deck_id==t)] for t in deck_ids]
    print(decks_studied)
    if decks_studied != []:
        decks_studied = [x[0] for x in decks_studied]
    averages = []
    points = []
    times = []
    for deck in decks_studied:
        point = sum([int(x.score) for x in db.session.query(Performance).filter(Performance.user_id==user_id,Performance.deck_id==deck[0]).all()])
        attempts = len([x for x in db.session.query(Performance).filter(Performance.user_id==user_id,Performance.deck_id==deck[0]).all()])
        averages.append(round((point/attempts)*100,2))
        points.append(point)
        times.append(get_misc(user_id,deck[0]))
    #return [],[],[],[]
    return decks_studied,averages,points,times
def update_performance(user_id,card_id,deck_id,score):
    new_performance = Performance(user_id=user_id,card_id=card_id,deck_id=deck_id,score=score)
    db.session.add(new_performance)
    db.session.commit()
    db.session.close()
def delete_performance_by_card(card_id):
    db.session.query(Performance).filter(Performance.card_id==card_id).delete()
    db.session.commit()
    db.session.close()
def delete_performance_by_deck(deck_id):
    db.session.query(Performance).filter(Performance.deck_id==deck_id).delete()
    db.session.commit()
    db.session.close()
# PERFORMANCE FUNCTIONS END

# MISC FUNCTIONS BEGIN
def add_misc(user_id,deck_id,time):
    new_misc = Misc(user_id=user_id,deck_id=deck_id,last_time=time)
    db.session.add(new_misc)
    db.session.commit()

def update_misc(user_id,deck_id,time):
    db.session.query(Misc).filter(Misc.deck_id==deck_id,Misc.user_id==user_id).update({"user_id":user_id,"deck_id":deck_id,"last_time":time})
    db.session.commit()

def delete_misc_by_deck(deck_id):
    db.session.query(Misc).filter(Misc.deck_id==deck_id).delete()
    db.session.commit()
    db.session.close()

def get_misc(user_id,deck_id):
    time = [x.last_time for x in db.session.query(Misc).filter(Misc.deck_id==deck_id,Misc.user_id==user_id).all()]
    return time
# MISC FUNCTIONS END






# RATING FUNCTIONS BEGIN
def update_rating(deck_id,rating):
    print("Reached here inside rating")
    new_rating = Rating(deck_id=deck_id,rating=rating)
    db.session.add(new_rating)
    db.session.commit()
    db.session.close()
    
def delete_rating(deck_id):
    db.session.query(Rating).filter(Rating.deck_id==deck_id).delete()
    db.session.commit()
    db.session.close()

def get_rating(deck_id):
    L = db.session.query(Rating).filter(Rating.deck_id==deck_id).all()
    if L != []:
        r = sum([int(x.rating) for x in L])/len(L)
        if r <0.5:
            return "Easy"
        elif r<1.5:
            return "Medium"
        else:
            return "Hard"
    else:
        return "No rating"
# RATING FUNCTIONS END

# OTHER FUNCTIONS BEGIN
def gen_hist_img(L):
    L = [L[0]]+L
    plt.plot(L)
    plt.ylabel("Points")
    plt.xlabel("Question")
    plt.xticks([i for i in range(len(L))])
    #print("length of x ; ",len(L),L)
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.clf()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def get_score_breakdown(user_id,deck_id):

    card_ids = [x[0] for x in get_cards(deck_id)]
    scores = []
    for x in card_ids:
        s =sum([int(y.score) for y in db.session.query(Performance).filter(Performance.user_id==user_id,Performance.card_id==x).all()])
        scores.append(s)
    return scores

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
                options.append(W[idx].capitalize())
        random.shuffle(options)
        data.append((card,options))
        print("options generated : ",options)
    return data
# OTHER FUCNTIONS END