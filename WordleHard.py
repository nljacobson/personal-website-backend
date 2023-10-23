import random
import GuessOutput

class WordleHard:
    max_guesses = 6
    # Constructor for mid game api call
    def __init__(self, word = None, guesses: list[str] = None):
        self.wordlist = self.get_word_list()
        self.guesslist = self.get_guess_list()
        if word is None:
            word = random.choice(self.wordlist)
        self.word = word
        self.possibilities = self.guesslist.copy()
        self.guess_output_factory = GuessOutput.GuessOutputFactory()
        self.playing = True
        self.guess_count = 0
        self.guesses = []
        if guesses is not None:
            for guess in guesses:
                self.guess(guess)
    def guess(self, guess: str) -> int:
        if not self.playing:
            return 2
        if guess not in self.get_possibilities():
            return 1
        guess_output = self.guess_output_factory.create_guess_output(guess, self.get_word())
        if type(guess_output) == GuessOutput.GuessOutput:
            self.guess_count += 1
            if guess_output.get_letter_colors() == 'GGGGG':
                self.playing = False
            if self.guess_count >= self.max_guesses:
                self.playing = False
            self.append_guesses(guess_output)
            self.narrow_possibilities()
            return 0
    def narrow_possibilities(self) -> None:
        last_guess = self.get_last_guess()
        if last_guess == None:
            raise Exception('Cannot find previously stored guess')
        mask = last_guess.get_mask()
        # Iterate over possibilities removing any that either do not have green letters in their correct place, or are missing req letters
        new_possibilities = []
        for p in self.get_possibilities():
            add = True
            for i in range(len(mask)):
                if mask[i] != ' ' and mask[i] != p[i]:
                    add = False
            for req in last_guess.get_req_letters():
                if req not in p:
                    add = False
            if add:
                new_possibilities.append(p)
        self.set_possibilities(new_possibilities)
    # Getters
    def get_playing(self) -> bool:
        return self.playing
    def get_word(self) -> str:
        return self.word
    def get_guesses(self) -> list[GuessOutput.GuessOutput]:
        return self.guesses
    def get_guesses_list(self) -> list[str]:
        outlist = []
        for guess in self.get_guesses():
            outlist.append(guess.get_guess())
        return outlist
    def get_letter_colors_list(self) -> list[str]:
        outlist = []
        for guess in self.get_guesses():
            outlist.append(guess.get_letter_colors())
        return outlist
    def get_last_guess(self) -> GuessOutput.GuessOutput:
        if len(self.guesses) > 0:
            return self.guesses[-1]
        else:
            return None
    def get_possibilities(self) -> list[str]:
        return self.possibilities
    def get_word_list(self) -> list[str]:
        if not hasattr(self, 'wordlist'):
            file = open('wordlist.txt')
            self.wordlist = []
            while line := file.readline():
                self.wordlist.append(line.rstrip())
        return self.wordlist
    def get_guess_list(self):
        if not hasattr(self, 'guesslist'):
            file = open('guesslist.txt')
            self.guesslist = []
            while line := file.readline():
                self.guesslist.append(line.rstrip())
        return self.guesslist
    
    # Setters
    def append_guesses(self, guess_output: GuessOutput.GuessOutput):
        self.guesses.append(guess_output)
    def set_possibilities(self, new_possibilities: list[str]):
        self.possibilities = new_possibilities