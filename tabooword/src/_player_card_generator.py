import os

# import qrcode
from imagekitio import ImageKit
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import yaml


# TODO: Move qrcode generator to js in webapp
# def generate_qrcode(
#     url: str,
# ):  # move to javascript part, api will send only the url(https://davidshimjs.github.io/qrcodejs/)
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)

#     # Add URL link
#     qr.add_data(url)

#     # Make the QR code
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")
#     return img


class PlayersCardGenerator:
    def __init__(self, font_name: str = "PK Phuket Medium.ttf") -> None:
        """_summary_

        Args:
            font_name (str, optional): Font's filename, should be the file stored under storage/font. Defaults to "PK Phuket Medium.ttf".
        """
        self._set_directory()  # set font and cache directory
        self.fontpath = f"{self.font_dir}/{font_name}"
        self.imagekit = ImageKit(
            private_key=os.environ["IMAGEKIT_PRIVATE_KEY"],
            public_key=os.environ["IMAGEKIT_PUBLIC_KEY"],
            url_endpoint=os.environ["URL_ENDPOINT"],
        )

    def _set_directory(self) -> None:
        """_summary_
        Set font and cache directory.
        """
        with open("/workdir/tabooword/config/directory.yml", "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        self.font_dir = config["font_dir"]
        self.cache_dir = config["cache_dir"]

    def _generate_card(
        self, player, height: int, width: int, add_word: bool = True
    ) -> Image.Image:
        """_summary_

        Args:
            player (Player): Each player object storing name, avatar, word, url.
            height (int): Height of player's avatar.
            width (int): width of player's avatar.
            add_word (bool, optional): Add player's taboo word to player's card or not. Defaults to True.

        Returns:
            card (Image.Image): Player's card containing avatar, name and tabooword(optional).
        """
        # png file: transparent channel to white
        img = Image.open(player.avatar)
        if player.avatar.split(".")[-1] == "png":
            img = np.array(img)
            img[img[..., -1] == 0] = [255, 255, 255, 0]
            img = Image.fromarray(img)

        # incorrect size: resize
        if (img.height != height) and (img.width != width):
            img = img.resize((width, height))

        card = Image.new("RGB", (width, int(height * 1.5)))
        card.paste(img, (0, 0))
        draw = ImageDraw.Draw(card)
        self._add_txt(player.name, font_size=int(height * 0.2), draw=draw, y=height)
        if add_word is True:
            self._add_txt(
                f"Word: {player.word}",
                font_size=int(height * 0.07),
                draw=draw,
                y=int(height * 1.3),
            )
        return card

    def _add_txt(
        self, txt: str, font_size: int, draw: ImageDraw.ImageDraw, y: int
    ) -> None:
        """_summary_
        Add text to the image.
        Args:
            txt (str): Text that want to add to the image
            font_size (int): Size of the text.
            draw (ImageDraw.ImageDraw): _description_
            y (int): Y-axis position to start writing text.
        """
        w, _ = draw.im.size
        font_name = ImageFont.truetype(self.fontpath, font_size)
        _, _, w_txt, _ = draw.textbbox((0, 0), txt, font=font_name)
        draw.text(((w - w_txt) / 2, y), txt, font=font_name)

    def _generate_cards(self, players: list):
        """_summary_

        Args:
            players (list): List of all Player object with name, avatar and taboo word. 

        Returns:
            cards_word (list): List of all player's card with taboo word.
            cards_no_word (list): List of all player's card without taboo word.
        """
        # Maximum height and width of players' avatar.
        h = max([Image.open(player.avatar).height for player in players])
        w = max([Image.open(player.avatar).width for player in players])

        cards_word, cards_no_word = [], []
        for player in players:
            cards_word.append(
                self._generate_card(player=player, height=h, width=w, add_word=True)
            )
            cards_no_word.append(
                self._generate_card(player=player, height=h, width=w, add_word=False)
            )
        return cards_word, cards_no_word

    def run(self, players: list):
        """_summary_
        Generate url of all player's cards.
        Args:
            players (list[Player]): List of Player object with name, avatar and word.
        """
        dt = datetime.now().strftime("%m%d%Y")
        list_card_word, list_card_no_word = self._generate_cards(players)
        w = [card_word.width for card_word in list_card_word]
        h = max([card_word.height for card_word in list_card_no_word])
        card = Image.new("RGB", (sum(w), h))

        w_offset = 0
        for card_word in list_card_word:
            card.paste(card_word, (w_offset, 0))
            w_offset += card_word.width

        for idx, (player, card_no_word) in enumerate(zip(players, list_card_no_word)):
            player_card = card.copy()
            player_card.paste(card_no_word, (idx * w[idx - 1], 0))
            player_card.save(f"{self.cache_dir}/result_{idx:02d}.png")
            upload_status = self.imagekit.upload_file(
                file=open(f"{self.cache_dir}/result_{idx:02d}.png", "rb"),  # required
                file_name=f"{dt}_result_{idx:02d}.png",  # required
            )
            player.url = upload_status.url
        # return player
