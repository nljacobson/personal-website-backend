from flask import Flask, request
from flask_cors import CORS
import chess_guess
import QHO
from WordleHard import WordleHard
from GuessOutput import GuessOutput
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
    game_data = json.dumps(
        {
        'result' : 0,    
        'guesses': transform_guesses(game.get_guesses_list()),
        'letterColors': transform_colors(game.get_letter_colors_list()),
        'word': game.get_word()}
        )
    return game_data

@app.route('/api/wordleguess', methods=['POST'])
def guess():
    run_data = request.json['params']['run_data']
    guesses = run_data['guesses']
    new_guesses = []
    for guess in guesses:
        if guess != '     ':
            new_guesses.append(guess)
    word = run_data['word']
    game = WordleHard(word, new_guesses[:-1])
    guessResult = game.guess(new_guesses[-1])
    game_data = json.dumps(
        {
        'result' : guessResult,    
        'guesses': transform_guesses(game.get_guesses_list()),
        'letterColors': transform_colors(game.get_letter_colors_list()),
        'word': game.get_word(),
        'num_possibilities': len(game.get_possibilities()),
        'playing': game.get_playing()}
        )
    return game_data

#Implementation specific transform patterns for frontend rendering
def transform_guesses(guess_objects: list[str]):
    new_guesses = []
    for guess in guess_objects:
        new_guesses.append(guess)
    for i in range(len(new_guesses), 6):
        new_guesses.append('     ')
    return new_guesses

def transform_colors(color_objects: list[str]):
    new_colors = []
    for color in color_objects:
        new_colors.append(color)
    for i in range(len(new_colors), 6):
        new_colors.append('WWWWW')
    return new_colors
if __name__ == '__main__':
    app.run()