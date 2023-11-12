from ._randomizer import Randomizer
from ._player_card_generator import PlayersCardGenerator
from dataclasses import dataclass
import random
from glob import glob
import yaml


@dataclass
class Player:
    name: str
    avatar: str
    word: str = None
    url: str = ""

    def __repr__(self):
        return repr(
            f"name = {self.name}\n word = {self.word}\n avatar = {self.avatar}\n url = {self.url}"
        )


class Engine:
    def __init__(self, names: list, avatar_list: dict = None) -> None:
        """_summary_

        Args:
            names (list): players' name
            avatar_list (dict, optional): List of avatar's file name. Defaults to None (randomly select avatar).
        """
        if avatar_list is not None:
            assert len(names) == len(
                avatar_list
            ), "[!] Lenght of player's name and avatar not match"
        self._set_directory()
        self.num_player = len(names)
        self.randomizer = Randomizer()
        self.player_card_generator = PlayersCardGenerator()
        self._set_player(name=names, avatar_list=avatar_list)

    def _set_directory(self):
        with open("/workdir/tabooword/config/directory.yml", "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        self.avatar_files = glob(f'{config["avatar_dir"]}/*')

    def _set_player(self, name: list, avatar_list: dict = None) -> None:
        """_summary_
        Initialize Player base on given inputs(name and avatar's file name)

        Args:
            name (list): List of players' name
            avatar_list (dict, optional): List of avatar's file name. Defaults to None (randomly select avatar).
        """
        players = []
        if avatar_list is None:  # not given avatar do random
            avatar_list = [
                self.avatar_files[random.randint(0, 299)]
                for _ in range(self.num_player)
            ]

        for name, avatar in zip(name, avatar_list):
            players.append(Player(name=name, avatar=avatar))
        self.players = players

    ## restart game, if continue game(not reset word vocab) = no need to reset
    def reset(self) -> None:
        """_summary_
        Restart the randomizer to reset all added words. 
        """
        self.randomizer = Randomizer()

    def add(self, word: str) -> str:
        """_summary_
        Add word to the randomizer
        Args:
            word (str): Taboo word

        Returns:
            str: status message. Successfully added or not.
        """
        return self.randomizer.add(word)

    def run(self):
        """_summary_
            Run the engine to add the taboo word for each player as well as generate player's card.
        """
        assert (
            len(self.randomizer.words) > self.num_player
        ), f"[!] Not enough word for this round. Have {len(self.randomizer)} word for {self.num_player} players."

        # Add random word to players' attribute.
        for player in self.players:
            player.word = self.randomizer.random()

        # Add image url to players' attribute (inplace)
        self.player_card_generator.run(self.players)


# TODO add class representative description, len of this object
