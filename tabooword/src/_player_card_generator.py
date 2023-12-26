import os

# import qrcode
from ._link_shorten import create_url, update_url, get_url_id
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import yaml
import math

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
    def __init__(self, font_name: str = "PK Phuket Medium.ttf", max_player_row:int = 4) -> None:
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
        self.imagekit_options = UploadFileRequestOptions(
            use_unique_file_name=True,
            # overwrite_file=True,
            # overwrite_tags=True,
            folder = f'/{datetime.now().strftime("%m%d%Y")}'
        )
        self.max_player_row = max_player_row # max number of player in 1 row inside the card

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

    def _generate_card_image(
        self,
        player,
        height: int,
        width: int,
        add_word: bool = True,
        image_height: int = 363,
    ) -> Image.Image:
        """_summary_

        Args:
            player (Player): Each player object storing name, avatar, word, url, image.
            height (int): Height of player's avatar.
            width (int): width of player's avatar.
            add_word (bool, optional): Add player's taboo card to player's card or not. Defaults to True.
            image_height (int, optional): Height of the card image to be added in player's card.

        Returns:
            card (Image.Image): Player's card containing avatar, name, tabooword(optional) and taboocard(optional).
        """
        # png file: transparent channel to white
        img = Image.open(player.avatar)
        if player.avatar.split(".")[-1] == "png":
            img = np.array(img)
            img[img[..., -1] == 0] = [255, 255, 255, 0]
            img = Image.fromarray(img)

        card_img = Image.open(player.image)
        if player.image.split("/")[-1].split(".")[0] == "png":
            card_img = np.array(card_img)
            card_img[card_img[..., -1] == 0] = [255, 255, 255, 0]
            card_img = Image.fromarray(card_img)
        card_img = card_img.resize((width, image_height))

        # incorrect size: resize
        if (img.height != height) and (img.width != width):
            img = img.resize((width, height))

        card = Image.new("RGB", (width, int(height * 1.5) + image_height))
        card.paste(img, (0, 0))
        draw = ImageDraw.Draw(card)
        self._add_txt(player.name, font_size=int(height * 0.2), draw=draw, y=height)
        if add_word is True:
            # player.word = path to image
            self._add_txt(
                f"Card: {player.word.split('.')[0].replace('_', ' ')}",  # ex:
                font_size=int(height * 0.07),
                draw=draw,
                y=int(height * 1.3),
            )
            card.paste(card_img, (0, int(height * 1.5)))

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

    def _generate_cards_image(self, players: list, h=300, w=250):
        """_summary_

        Args:
            players (list): List of all Player object with name, avatar and taboo word. 
            h (int, optional): Height of the avatar.
            w (int, optional): Width of the avatar.

        Returns:
            cards_image (list): List of all player's card with taboo image.
            cards_no_image (list): List of all player's card without taboo image.
        """
        # image size = 250x363
        cards_image, cards_no_image = [], []
        for player in players:
            cards_image.append(
                self._generate_card_image(
                    player=player, height=h, width=w, add_word=True
                )
            )
            cards_no_image.append(
                self._generate_card_image(
                    player=player, height=h, width=w, add_word=False
                )
            )
        return cards_image, cards_no_image

    def run(self, players: list):
        """_summary_
        Generate url of all player's cards.
        Args:
            players (list[Player]): List of Player object with name, avatar and word.
        """
        num_row = math.ceil(len(players)/self.max_player_row)
        if num_row==1:
            num_col = len(players)
        else:
            num_col = self.max_player_row
        list_card_word, list_card_no_word = self._generate_cards(players) # all card have same height and width
        w, h = list_card_word[0].width, list_card_word[0].height
        card = Image.new("RGB", (int(w*num_col), int(h*num_row)))###

        for idx, card_word in enumerate(list_card_word):
            w_loc = int((idx%num_col)*w)
            h_loc = int((idx//num_col)*h)
            card.paste(card_word, (w_loc, h_loc))


        for idx, (player, card_no_word) in enumerate(zip(players, list_card_no_word)):
            player_card = card.copy()
            w_loc = int((idx%num_col)*w)
            h_loc = int((idx//num_col)*h)
            player_card.paste(card_no_word, (w_loc, h_loc))
            player_card.save(f"{self.cache_dir}/result_{idx:02d}.png")
            upload_status = self.imagekit.upload_file(
                file=open(f"{self.cache_dir}/result_{idx:02d}.png", "rb"),  # required
                file_name=f"defaultMode_result_{idx:02d}.png",  # required
            )
            player.url = upload_status.url
        # return player

    def run_card(self, players: list):
        """_summary_
        Generate url of all player's cards.
        Args:
            players (list[Player]): List of Player object with name, avatar and word.
        """
        num_row = math.ceil(len(players)/self.max_player_row)
        if num_row==1:
            num_col = len(players)
        else:
            num_col = self.max_player_row
        list_card_image, list_card_no_image = self._generate_cards_image(players)
        w, h = list_card_image[0].width, list_card_image[0].height
        card = Image.new("RGB", (int(w*num_col), int(h*num_row)))###

        for idx, card_word in enumerate(list_card_image):
            w_loc = int((idx%num_col)*w)
            h_loc = int((idx//num_col)*h)
            card.paste(card_word, (w_loc, h_loc))


        for idx, (player, card_no_image) in enumerate(zip(players, list_card_no_image)):
            player_card = card.copy()
            w_loc = int((idx%num_col)*w)
            h_loc = int((idx//num_col)*h)
            player_card.paste(card_no_image, (w_loc, h_loc))
            player_card.save(f"{self.cache_dir}/result_{idx:02d}.png")
            upload_status = self.imagekit.upload_file(
                file=open(f"{self.cache_dir}/result_{idx:02d}.png", "rb"),  # required
                file_name=f"cardMode_result_{idx:02d}.png",  # required
                options = self.imagekit_options
            )
            pathname = f"cardMode/{idx:02d}"
            url = create_url(originalURL=upload_status.url, pathname=pathname)
            if url is None:
                if player.url_id is None:
                    url_id = get_url_id(pathname = pathname)
                    player.url_id = url_id
                else:
                    url_id = player.url_id
                url = update_url(idString=url_id, originalURL=upload_status.url)
            player.url = url
            #player.tmp = upload_status
        # return player
