
from flask import Flask, session,render_template,request,redirect,g,url_for
from flask_restful import Api
import os
from api.api import CardAddAPI, CardDelAPI,DeckAddAPI,DeckUpdateAPI,DeckDelAPI, QuizApi, RatingApi
from application.configuration import appConfig
from controllers.functions import add_user,gen_hist_img, get_decks,get_card, get_performance, get_rating, get_score_breakdown, get_user_id, option_gen, reset_result, user_exists,authenticate_user,get_cards,get_deck,get_result
from db.database import db
import matplotlib
matplotlib.use('Agg')




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
    try:
        print(g.user)
        if request.method == 'GET':
            if g.user:
                return redirect(url_for('dashboard'))
        session.clear()
        return render_template("login.html")
    except:
        return render_template("error.html")



@app.route('/signin',methods=['GET','POST'])
def signin():
    print(g.user)
    status = "" 
    if g.user:
        return redirect(url_for('dashboard'))
    try:
        if request.method == 'POST':
            session.pop('user',None)
            if authenticate_user(request.form['username'],request.form['password']):
                session['user'] = request.form['username']
                return redirect(url_for('dashboard'))
            else:
                status = "Incorrect username or login"
    except:
        return render_template("error.html")
    return render_template("signin.html",message=status)

@app.route('/cheemserror')
def cheemserror():
    return render_template('error.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
    status = ""
    if g.user:
        return redirect(url_for('dashboard'))
    try:
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
    except:
        return render_template("error.html")
    return render_template("signup.html",message=status)


@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
    try:
        reset_result()
    except:
        return render_template("error.html")
    if g.user:
        try:
            scores = []
            images = []
            ratings = []
            decks_studied,averages,points,times = get_performance(get_user_id(session['user']))
            for deck in decks_studied:
                scores.append(get_score_breakdown(get_user_id(session['user']),deck[0]))
            for deck in decks_studied:
                ratings.append(get_rating(deck[0]))
            print(scores)
            for i in scores:
                print(i)
                images.append(gen_hist_img(i))
            return render_template("dashboard.html",user=session['user'],decks = decks_studied,averages=averages,points=points,times=times,size = len(points),images = images,ratings=ratings)
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))






@app.route('/results',methods = ['GET','POST'])
def results():
    global visited
    visited = []
    if g.user:
        try:
            deck_id=request.args.get('deck_id')
            points,wrong_cards = get_result(get_user_id(session["user"]))
            if int(points) >= 100:
                message = "Excellent"
                color = "#008000"
            elif int(points) >=70:
                message = "Good"
                color = "#f8bb00"
            elif int(points) >= 40:
                color = "#808080"
                message = "Passed"
            else:
                color = '#ff0000'
                message = "Try again"
        
            if points !=None and wrong_cards != None:
                cards = [get_card(x) for x in wrong_cards]
                perfect = "No reviews recommended for now. You got a perfect score!"
                print(cards)
                if cards != []:
                    perfect = ""
                return render_template("results.html",points=points,cards=cards,perfect = perfect,deck_id = deck_id,message = message, color = color)
        except:
            return render_template("error.html")   
    return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    session.pop('user',None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/decks',methods = ['GET','POST'])
def decks():
    if g.user:
        try:
            if get_decks() == None:
                return render_template("decks.html")
            return render_template("decks.html",decks = get_decks())
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))

@app.route('/quiz_loader',methods = ['GET','POST'])
def quiz_loader():
    global visited
    visited = []
    try:
        reset_result()
    except:
        return render_template("error.html")
    if g.user:
        try:
            if get_decks() == None:
                return render_template("decks.html")
            decks = []
            temp = get_decks()
            for i in temp:
                if get_cards(i[0]) != []:
                    decks.append(i)
            return render_template("quiz_loader.html",decks = decks)
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))
#global data
visited = []
data = None
@app.route('/quiz/<int:deck_id>/<int:current>',methods = ['GET','POST'])
def quiz(deck_id,current):
    print("selected deck = ",deck_id)
    global data
    global visited
    if g.user:
        try:
            if get_cards(deck_id) == None:
                return render_template("decks.html")
            if data != option_gen(get_cards(deck_id)):
                data = None
            if data == None:
                data = option_gen(get_cards(deck_id))
            n = len(data)-1
            user_id = get_user_id(session["user"])
            if current not in visited:
                visited.append(current)
                return render_template("quiz.html",data = data,current = int(current),size = n,deck_id=deck_id,user_id=user_id)
            else:
                reset_result()
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))

@app.route('/deck/<int:deck_id>',methods = ['GET','POST'])
def deck(deck_id):
    if g.user:
        try:
            if get_cards(deck_id) == None:
                return render_template("cards.html")
            return render_template("cards.html",deck = get_deck(deck_id),cards = get_cards(deck_id), size = len(get_cards(deck_id)))
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))

@app.route('/<int:deck_id>/add_card',methods = ['GET','POST'])
def add_card(deck_id):
    if g.user:
        try:
            return render_template("add_card.html",deck = get_deck(deck_id))
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))

@app.route('/<int:deck_id>/delete_card',methods = ['GET','POST'])
def delete_card1(deck_id):
    if g.user:
        try:
            return render_template("delete_card.html",cards = get_cards(deck_id) ,deck = get_deck(deck_id))
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))
@app.route('/<int:deck_id>/edit_deck',methods = ['GET','POST'])
def edit_deck(deck_id):
    if g.user:
        try:
            return render_template("edit_deck.html" ,deck = get_deck(deck_id))
        except:
            return render_template("error.html")   
    return redirect(url_for('signin'))
@app.route('/deck/add',methods = ['GET','POST'])
def add_deck():
    if g.user:
        try:
            return render_template("add_deck.html")
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))
@app.route('/deck/delete',methods = ['GET','POST'])
def delete_deck1():
    if g.user:
        try:
            return render_template("delete_deck.html",decks = get_decks())
        except:
            return render_template("error.html")
    return redirect(url_for('signin'))


api.add_resource(CardAddAPI,"/cardapi/add")
api.add_resource(CardDelAPI,"/cardapi/delete")
api.add_resource(DeckAddAPI,"/deckapi/add")
api.add_resource(DeckUpdateAPI,"/deckapi/update")
api.add_resource(DeckDelAPI,"/deckapi/delete")
api.add_resource(QuizApi,"/quizapi/next")
api.add_resource(RatingApi,"/ratingapi/update")

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

if __name__ == "__main__":
    app.run(host='0.0.0.0')