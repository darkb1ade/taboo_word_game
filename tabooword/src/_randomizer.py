import random


class Randomizer:
    def __init__(self) -> None:
        self.words = []

    def __len__(self):
        return len(self.words)

    def add(self, word):
        if word in self.words:
            msg = "[!] Duplicated word! Please insert again."
        else:
            self.words.append(word)
            msg = "Word added"
        return msg
        # TODO not allow similar word

    def random(self):
        word = random.choice(self.words)
        self.words.remove(word)
        return word
