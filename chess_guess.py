from top_players import get_player_name
import numpy as np
import tensorflow as tf

piece_to_int = {
        'p':21,
        'P':11,
        'n':22,
        'N':12,
        'b':23,
        'B':13,
        'r':24,
        'R':14,
        'q':25,
        'Q':15,
        'k':26,
        'K':16,
    }
int_to_piece = {
        21:'p',
        11:'P',
        22:'n',
        12:'N',
        23:'b',
        13:'B',
        24:'r',
        14:'R',
        25:'q',
        15:'Q',
        26:'k',
        16:'K',
    }

def get_chess_guesses(fen):
    # Split into lines
    game = fen_to_numeric(fen)
    white_model = tf.keras.models.load_model('./white_player_model')
    black_model = tf.keras.models.load_model('./black_player_model')
    white_output = white_model.predict(game).ravel()
    black_output = black_model.predict(game).ravel()
    white_sum = sum(white_output)
    black_sum = sum(black_output)
    whiteGuesses = []
    blackGuesses = []
    for i in range(10):
        print(white_output.argmax())
        white_player = str(get_player_name(white_output.argmax()))
        black_player = str(get_player_name(black_output.argmax()))
        white_player_certainty = white_output[white_output.argmax()]/white_sum
        black_player_certainty = black_output[black_output.argmax()]/black_sum
        if white_player_certainty > 0:
            whiteGuesses.append([white_player, "{cert:.2f}%".format(cert=100*white_player_certainty)])
        if black_player_certainty > 0:
            blackGuesses.append([black_player, "{cert:.2f}%".format(cert=100*black_player_certainty)])
        white_output[white_output.argmax()] = -1.0
        black_output[black_output.argmax()] = -1.0
        print(white_player)
    return {'whiteGuesses': whiteGuesses, 'blackGuesses': blackGuesses}

def numeric_to_fen(numeric_game):
    numpy_game = (numeric_game.numpy()[0]).T
    rows = list(reversed(np.array_split(numpy_game, indices_or_sections=8)))
    #Game is now seperated into rows starting at "Row 8", down to "Row 1" in chess notation
    fen = ""
    for row in rows:
        # Convert row to fen format
        space_counter = 0
        for item in row[0].tolist():
            if item == 0:
                space_counter += 1
            else:
                if space_counter != 0:
                    fen += str(space_counter)
                    space_counter = 0
                fen += int_to_piece[item]
        if space_counter != 0:
            fen += str(space_counter)
            space_counter = 0
        fen += "/"
    # Remove final slash on last line
    fen = fen[:-1]
    return fen

def fen_to_numeric(fen):
    fen_first_split = fen.split(sep='/')
    # Remove win loss info from the end of fen
    fen_first_split[7] = fen_first_split[7].split(sep = ' ')[0]
    game = []
    for input_row in reversed(fen_first_split):
        output_row = []
        for input_item in input_row:
            if input_item in piece_to_int:
                output_row.append(int(piece_to_int[input_item]))
            elif input_item.isnumeric():
                for i in range(int(input_item)):
                    output_row.append(0)
            else:
                assert False
        game.append(output_row)
    game = np.array(game).T
    game_tensor = tf.convert_to_tensor([game])
    return game_tensor