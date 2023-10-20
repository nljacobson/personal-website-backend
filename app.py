from flask import Flask, request
from flask_cors import CORS
import chess_guess
import QHO
from WordleHard import WordleHard
import json
app = Flask(__name__)
allowed_origins = ["*"]
cors = CORS(app, supports_credentials=True, origins=allowed_origins)

@app.route('/api/chess')
def get_chess_guesses_flask():
    fen = request.args.get('fen')
    return chess_guess.get_chess_guesses(fen)

@app.route('/api/post_qho_first', methods=['POST'])
def post_qho_first_flask():
    n = request.json['params']['n']
    if type(n) != int:
        n = 0
    run_data = QHO.post_qho_first(n)
    run_data_json = json.dumps(run_data)
    return run_data_json

@app.route('/api/post_qho_run', methods=['POST'])
def post_qho_run_flask():
    run_data = request.json['params']['run_data']
    run_data = QHO.post_qho_run(run_data)
    run_data_json = json.dumps(run_data)
    return run_data_json
@app.route('/api/testpost', methods= ['POST'])
def test_post():
    return 'Successful Post'

@app.route('/')
def index():
   print('Request for index page received')
   return '<div></div>'

@app.route('/api/wordlecreate', methods=['GET'])
def createwordle():
    game = WordleHard()
    game_data = json.dumps([
        {'guesses': game.get_guesses_list()},
        {'letterColors': game.get_letter_colors_list()},
        {'word': game.get_word()}
        ])
    return game_data

@app.route('/api/wordleguess', methods=['POST'])
def guess():
    guesses = request.args.get('guesses')[1:-1].split(" ")
    new_guesses = []
    for guess in guesses:
        if guess[-1] == ',':
            guess = guess[0:-1]
        new_guesses.append(guess[1:-1])
    word = request.args.get('word')[1:-1]
    print(word)
    game = WordleHard(word, new_guesses)
    guess_result = game.guess(new_guesses[-1])
    game_data = json.dumps([
        {'guesses': game.get_guesses_list()},
        {'letterColors': game.get_letter_colors_list()},
        {'word': game.get_word()}
        ])
    return game_data

if __name__ == '__main__':
    app.run()