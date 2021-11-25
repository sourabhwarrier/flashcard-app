
from flask.templating import render_template
from flask_restful import Resource
from flask import request,url_for
from sqlalchemy.sql.expression import update
from werkzeug.utils import redirect
from datetime import datetime

from controllers.functions import add_card, add_misc,delete_card,add_deck, delete_deck, get_card, get_cards, get_misc, get_result, reset_result,update_deck, update_misc, update_performance, update_result

class CardAddAPI(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        question = request.form['question']
        answer = request.form['answer']
        deck_id = int(request.form['deck_id'])
        add_card(question,answer,deck_id)
        return redirect("/deck/{}".format(deck_id))
    def delete(self):
        pass

class CardDelAPI(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self): 
        #print(request)
        to_delete =request.form.getlist("to_delete")
        if to_delete != []:
            for x in to_delete:
                print(x)
                
            
                delete_card(x)
        return redirect("/{}".format("dashboard"))
    def delete(self):
        pass

class DeckAddAPI(Resource):
    def get(self):
        pass 
    def put(self):
        pass
    def post(self):
        name = request.form['name']
        description = request.form['description']
        add_deck(name,description)
        return redirect("/decks")
    def delete(self):
        pass


class DeckUpdateAPI(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        name = request.form['name']
        description = request.form['description']
        deck_id = request.form['deck_id']
        update_deck(deck_id,name,description)
        return redirect("/decks")
    def delete(self):
        pass


class DeckDelAPI(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self): 
        #print(request)
        to_delete =request.form.getlist("to_delete")
        if to_delete != []:
            for x in to_delete:
                print(x)
                cards = get_cards(x)
                for y in cards:
                    delete_card(y[0])
                delete_deck(x)
        return redirect("/{}".format("decks"))
    def delete(self):
        pass


class QuizApi(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        submission = None
        user_id=request.form["user_id"]
        card_id = request.form["card_id"]
        current = request.form["current"]
        try:
            submission = request.form["option"]
        except:
            submission = "-1111111111"
        deck_id=request.form["deck_id"]
        size = request.form["size"]
        answer = get_card(card_id)[2]
        if submission == answer:
            score = 1
        else:
            score = 0
        update_result(user_id=user_id,card_id=card_id,answer=answer,submission=submission,score=score)
        update_performance(user_id=user_id,card_id=card_id,deck_id=deck_id,score=score)
        
        if int(current)<int(size):
            return redirect('/quiz/{}/{}'.format(deck_id,str(int(current)+1)))
        else:
            new_time = datetime.now().strftime("%b %d %Y %H:%M:%S")
            check = get_misc(user_id,deck_id)
            if check == []:
                add_misc(user_id,deck_id,new_time)
            else:
                update_misc(user_id,deck_id,new_time)
            print("value of check ************ is : {}".format(check))
            #points,wrong_cards = get_result(user_id)
            #reset_result()
            return redirect(url_for('results'))

    def delete(self):
        pass