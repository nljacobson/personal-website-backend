class GuessOutput:
    def __init__(self, guess:str, word:str):
        self.word = word
        self.guess = guess
        self.letter_colors = self._create_letter_colors(self.guess, self.word)
        self.mask = self._create_mask(self.guess, self.word)
        self.req_letters = self._create_req_letters(self.guess, self.word)


    def _create_letter_colors(self, guess:str, word:str):
        letter_colors = ''
        for i in range(len(word)):
            if guess[i] == word[i]:
                # Letter is correctly placed in word
                letter_colors += 'G'
            elif guess[i] in word:
                # Letter is in wrong place but in word
                letter_colors += 'Y'
            else:
                # Letter is not in word
                letter_colors += ' '
        return letter_colors
    
    def _create_mask(self, guess:str, word:str):
        mask = ''
        for i in range(len(word)):
            if guess[i] == word[i]:
                mask += word[i]
            else:
                mask += ' '
        return mask
    
    def _create_req_letters(self, guess:str, word:str):
        req_letters = []
        for letter in guess:
            if letter in word:
                req_letters.append(letter)
        return req_letters
    # Getters
    def get_word(self):
        return self.word
    def get_guess(self):
        return self.guess
    def get_letter_colors(self):
        return self.letter_colors
    def get_mask(self):
        return self.mask
    def get_req_letters(self):
        return self.req_letters
    # Print
    def print(self):
        class color:
            PURPLE = '\033[95m'
            CYAN = '\033[96m'
            DARKCYAN = '\033[36m'
            BLUE = '\033[94m'
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            RED = '\033[91m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
            END = '\033[0m'
        output = ''
        letter_colors = self.get_letter_colors()
        guess = self.get_guess()
        word = self.get_word()
        for i in range(len(word)):
            if letter_colors[i] == 'G':
                output += color.GREEN
            elif letter_colors[i] == 'Y':
                output += color.YELLOW
            elif letter_colors[i] == ' ':
                output += color.END
            else:
                raise ValueError('Unknown letter_color {} detected'.format(letter_colors[i]))
            output += guess[i]
        output += color.END
        return output
class GuessOutputFactory:
    def create_guess_output(self, guess:str, word:str):
        guess_output = GuessOutput(guess, word)
        return guess_output

