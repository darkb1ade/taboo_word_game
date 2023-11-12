import random


class Randomizer:
    def __init__(self) -> None:
        self.words = []

    def __len__(self):
        return len(self.words)

    def add(self, word):
        if word in self.words:
            msg = f"[!] Duplicated word! Please insert again. Total {len(self.words)} word added"
        else:
            self.words.append(word)
            msg = f"Word added. Total {len(self.words)} word added"
        return msg
        # TODO not allow similar word

    def random(self):
        word = random.choice(self.words)
        self.words.remove(word)
        return word
