
from flask_restful import Resource
from flask import request
from werkzeug.utils import redirect

from controllers.functions import add_card,delete_card,add_deck, delete_deck, get_cards,update_deck

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