
from flask import Flask, session,render_template,request,redirect,g,url_for
from flask_restful import Api
import os

from sqlalchemy import databases
from api.api import CardAddAPI, CardDelAPI,DeckAddAPI,DeckUpdateAPI,DeckDelAPI, QuizApi
from application.configuration import appConfig
from controllers.functions import add_user, get_decks, get_user_id, option_gen, user_exists,authenticate_user,get_cards,get_deck
from db.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(appConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    app.secret_key = os.urandom(24)
    return app, api
    
app,api = create_app()

@app.route('/')
def login():
    print(g.user)
    if request.method == 'GET':
        if g.user:
            return redirect(url_for('dashboard'))
    session.clear()
    return render_template("login.html")




@app.route('/signin',methods=['GET','POST'])
def signin():
    print(g.user)
    status = "" 
    if g.user:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        session.pop('user',None)
        if authenticate_user(request.form['username'],request.form['password']):
            session['user'] = request.form['username']
            return redirect(url_for('dashboard'))
        else:
            status = "Incorrect username or login"
    return render_template("signin.html",message=status)



@app.route('/signup',methods = ['GET','POST'])
def signup():
    status = ""
    if g.user:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        session.pop('user',None)
        username = request.form['username']
        password = request.form['password']
        if not user_exists(username):
            add_user(username,password)
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            status = "username {} is unavailable".format(username)
    return render_template("signup.html",message=status)


@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
    if g.user:
        return render_template("dashboard.html",user=session['user'])
    return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    session.pop('user',None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/decks',methods = ['GET','POST'])
def decks():
    if g.user:
        if get_decks() == None:
            return render_template("decks.html")
        return render_template("decks.html",decks = get_decks())
    return redirect(url_for('signin'))

@app.route('/quiz_loader',methods = ['GET','POST'])
def quiz_loader():
    if g.user:
        if get_decks() == None:
            return render_template("decks.html")
        return render_template("quiz_loader.html",decks = get_decks())
    return redirect(url_for('signin'))
data = None
@app.route('/quiz/<int:deck_id>/<int:current>',methods = ['GET','POST'])
def quiz(deck_id,current):
    global data
    if g.user:
        if get_cards(deck_id) == None:
            return render_template("decks.html")
        if data == None:
            data = option_gen(get_cards(deck_id))
        n = len(data)-1
        user_id = get_user_id(session["user"])
        return render_template("quiz.html",data = data,current = int(current),size = n,deck_id=deck_id,user_id=user_id)
    return redirect(url_for('signin'))

@app.route('/deck/<int:deck_id>',methods = ['GET','POST'])
def deck(deck_id):
    if g.user:
        if get_cards(deck_id) == None:
            return render_template("cards.html")
        return render_template("cards.html",deck = get_deck(deck_id),cards = get_cards(deck_id))
    return redirect(url_for('signin'))

@app.route('/<int:deck_id>/add_card',methods = ['GET','POST'])
def add_card(deck_id):
    if g.user:
        return render_template("add_card.html",deck = get_deck(deck_id))
    return redirect(url_for('signin'))

@app.route('/<int:deck_id>/delete_card',methods = ['GET','POST'])
def delete_card1(deck_id):
    if g.user:
        return render_template("delete_card.html",cards = get_cards(deck_id) ,deck = get_deck(deck_id))
    return redirect(url_for('signin'))
@app.route('/<int:deck_id>/edit_deck',methods = ['GET','POST'])
def edit_deck(deck_id):
    if g.user:
        return render_template("edit_deck.html" ,deck = get_deck(deck_id))
    return redirect(url_for('signin'))
@app.route('/deck/add',methods = ['GET','POST'])
def add_deck():
    if g.user:
        return render_template("add_deck.html")
    return redirect(url_for('signin'))
@app.route('/deck/delete',methods = ['GET','POST'])
def delete_deck1():
    if g.user:
        return render_template("delete_deck.html",decks = get_decks())
    return redirect(url_for('signin'))


api.add_resource(CardAddAPI,"/cardapi/add")
api.add_resource(CardDelAPI,"/cardapi/delete")
api.add_resource(DeckAddAPI,"/deckapi/add")
api.add_resource(DeckUpdateAPI,"/deckapi/update")
api.add_resource(DeckDelAPI,"/deckapi/delete")
api.add_resource(QuizApi,"/quizapi/next")

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

if __name__ == "__main__":
    app.run()