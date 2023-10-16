from flask import Flask, request
from flask_cors import CORS
import chess_guess
import QHO
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
   return '<div>HELLO WORLD</div>'

if __name__ == '__main__':
    app.run()
    #app.run(ssl_context='adhoc', port=5000)