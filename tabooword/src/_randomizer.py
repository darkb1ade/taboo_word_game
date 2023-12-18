import random
import itertools


class Randomizer:
    def __init__(self, card_mode=False) -> None:
        self.words = []
        if card_mode is True:
            self._init_card()

    def __len__(self):
        return len(self.words)

    def _init_card(self):
        suits = ["Diamonds", "Spades", "Hearts", "Clubs"]
        ranks = [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "Jack",
            "Queen",
            "King",
            "Ace",
        ]
        self.words = list(itertools.product(ranks, suits))

    def add(self, word):
        assert (
            word not in self.words
        ), f"[!] Duplicated word! Please insert again. Total {len(self.words)} word added"
        self.words.append(word)
        msg = f"Word added. Total {len(self.words)} word added"
        return msg
        # TODO not allow similar word

    def random(self):
        word = random.choice(self.words)
        self.words.remove(word)
        return word
