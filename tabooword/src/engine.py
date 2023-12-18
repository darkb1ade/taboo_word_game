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
    image: str = None
    url: str = ""

    def __repr__(self):
        return repr(
            f"name = {self.name}\n image = {self.image}\n word = {self.word}\n avatar = {self.avatar}\n url = {self.url}"
        )


class Engine:
    def __init__(self) -> None:
        """_summary_

        Args:
            names (list): players' name
            avatar_list (dict, optional): List of avatar's file name. Defaults to None (randomly select avatar).
        """
        self.card_mode = False
        self.randomizer = None
        self.player_card_generator = PlayersCardGenerator()

    def __repr__(self) -> str:
        if hasattr(self, "players"):
            players = [player.name for player in self.players]
        else:
            players = []
        return f"Engine(players = {players}, num_words = {len(self.randomizer)} card_mode = {self.card_mode})"

    def init_engine(self, names: list, avatar_list: list, card_mode=False):
        self.card_mode = card_mode  # set card mode
        self.randomizer = Randomizer(
            card_mode=card_mode
        )  # init randomizer for card mode
        if avatar_list is not None:
            assert len(names) == len(
                avatar_list
            ), "[!] Lenght of player's name and avatar not match"
        self._set_directory()
        self.num_player = len(names)
        self._set_player(name=names, avatar_list=avatar_list)

    def _set_directory(self):
        with open("/workdir/tabooword/config/directory.yml", "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        self.avatar_files = glob(f'{config["avatar_dir"]}/*.png')
        self.avart_dir = config["avatar_dir"]

        if self.card_mode is True:  # In card mode, store storage to card image
            self.img_dir = config["image_dir"]

    def _set_player(self, name: list, avatar_list: list = None) -> None:
        """_summary_
        Initialize Player base on given inputs(name and avatar's file name)

        Args:
            name (list): List of players' name
            avatar_list (list, optional): List of avatar's file name. Defaults to None (randomly select avatar).
        """
        players = []
        if avatar_list is None:  # not given avatar do random
            avatar_list = [
                self.avatar_files[random.randint(0, len(self.avatar_files) - 1)]
                for _ in range(self.num_player)
            ]
        else:
            try:
                avatar_list = [f"{self.avart_dir}/{avatar}" for avatar in avatar_list]
            except ValueError as e:
                raise e
        for name, avatar in zip(name, avatar_list):
            assert (
                avatar in self.avatar_files
            ), f"[!] Avatar not found for {avatar.split('/')[-1]}"
            players.append(Player(name=name, avatar=avatar))
        self.players = players

    ## restart game, if continue game(not reset word vocab) = no need to reset
    def reset(self) -> None:
        """_summary_
        Restart the randomizer to reset all added words. 
        """
        self.randomizer = Randomizer(self.card_mode)

    def add(self, word: str) -> str:
        """_summary_
        Add word to the randomizer
        Args:
            word (str): Taboo word

        Returns:
            str: status message. Successfully added or not.
        """
        return self.randomizer.add(word)

    def run_card(self):
        """_summary_
            Run the engine to randomize playing card and reset the deck in card game mode.
        """
        assert hasattr(self, "num_player"), "[!] Object is not initialized!"
        assert (
            len(self.randomizer.words) >= self.num_player
        ), f"[!] Not enough card for this round. Have {len(self.randomizer)} card for {self.num_player} players."

        # Add random word to players' attribute.
        for player in self.players:
            word = self.randomizer.random()
            player.word = f"{word[0]}_of_{word[-1].lower()}.png"
            player.image = f"{self.img_dir}/{player.word}"

        # Add image url to players' attribute (inplace)
        self.player_card_generator.run_card(self.players)
        msg = f"Finished random. Total {len(self.randomizer)} card left."

        # reset deck
        self.randomizer._init_card()

        return msg

    def run(self):
        """_summary_
            Run the engine to add the taboo word for each player as well as generate player's card.
        """
        assert hasattr(self, "num_player"), "[!] Object is not initialized!"
        assert (
            len(self.randomizer.words) >= self.num_player
        ), f"[!] Not enough word for this round. Have {len(self.randomizer)} word for {self.num_player} players."

        # Add random word to players' attribute.
        for player in self.players:
            player.word = self.randomizer.random()

        # Add image url to players' attribute (inplace)
        self.player_card_generator.run(self.players)
        msg = f"Finished random. Total {len(self.randomizer)} word left."
        return msg
