from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def say_hello():
    return 'Hello World!'

@app.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    output = []
    for game in games:
        output.append( {'name' : game.name, 'description' : game.description} )
    return { "games" : output }

@app.route('/games/<id>', methods=['GET'])
def get_game_by_id(id):
    game = Game.query.get_or_404(id)
    return {'name' : game.name, 'description' : game.description}

@app.route('/games', methods=['POST'])
def add_game():
    game = Game(name=request.json['name'], description=request.json['description'])
    db.session.add(game)
    db.session.commit()
    return {"id" : game.id}


@app.route('/games/<id>', methods=['DELETE'])
def delete_game(id):
    game = Game.query.get(id)
    if game is None:
        return { "error" : "Game Not Found"}
    db.session.delete(game)
    db.session.commit()
    return { "message" : "Game deleted"}