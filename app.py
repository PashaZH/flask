from flask import Flask, request, jsonify, abort
import random


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

about_me = {
    "name": "Pasha",
    "surname": "ZH",
    "email": "pashaZH@specialist.ru"
}
@app.route("/about")
def about():
    return about_me

app.config['JSON_AS_ASCII'] = False

quotes = [
    {
        "id": 3,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка"

    },
    {
        "id": 5,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 6,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 8,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так."
    },
]


@app.route("/quotes/<int:id>")
def get_quote(id):
    for quote in quotes:
        if quote['id'] == id:
            return quote
    abort(404)

@app.route("/quotes/count")
def quote_count():
    return {"count": len(quotes)}

@app.route("/quotes", methods=['POST'])
def create_quote():
    data = request.json
    
    new_id = quotes[-1]['id'] + 1
    
   
    new_quote = {
        "id": new_id,
        "author": data.get('author'),
        "text": data.get('text'),
        "rating": data.get('rating', 1)  
    }
    
    quotes.append(new_quote)
    
    
    return new_quote, 201

@app.route("/quotes/random")
def random_quote():
    return random.choice(quotes)



if __name__ == "__main__":
    app.run(debug=True)