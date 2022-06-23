import random
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import os
from PIL import Image, ImageFont, ImageDraw
from config import Conf
from dropbox_api import upload_img
import datetime
#players = ['ปานวาด', 'น้ำฝน', 'มอส', 'ออฟ']
#words = ['อาหาร','หน้าฝน','ไทย','ร้อน','เที่ยว','ลาออก']


def word_random(words):
    word = random.choice(words)
    words.remove(word)
    return word
def gen_color(N):
    HSV_tuples = [((x * 1.0 / N), 0.5, 0.5) for x in range(N)]
    return list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))

class TabooImage():
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.out =os.path.join(self.out, datetime.datetime.now().strftime('%Y%m%d_%H'))
        os.makedirs(os.path.join(self.out, 'answer'), exist_ok=True)
        fontpath = "front/PK Phuket Medium.ttf"  # <== download font
        self.font = ImageFont.truetype(fontpath, self.font_size)
        self.font_name = ImageFont.truetype(fontpath, self.font_size-10)
        self.get_round()

    def get_round(self):
        round = len(os.listdir(os.path.join(self.out, 'answer')))+1
        self.round = round

    def gen_img(self,N, H = 50):
        colors = gen_color(N)
        img = np.zeros((N * self.H, 500, 3))
        for i in range(N):
            img[H*i:H*(i+1),:,:] = (colors[i][0],colors[i][1],colors[i][2])
        return img
    def gen_ans_img(self,result, save = False):
        img = self.gen_img(len(result), H=self.H)
        img_pil = Image.fromarray(np.uint8((img) * 255))
        draw = ImageDraw.Draw(img_pil)
        for i, (k,v) in enumerate(result.items()):
            #print(k,v)
            draw.text((self.st_name, 20+i*self.H), k, font=self.font_name)
            draw.text((self.st_word, 10 + i * self.H), v, font=self.font)
        if save:
            pathOut = os.path.join(self.out, 'answer',f"round_{self.round:04d}.jpg")
            img_pil.save(pathOut)
            upload_img(pathOut)
        return np.array(img_pil)
    def gen_player_img(self,img,players, save = False):
        imgs = {}
        for i, player in enumerate(players):
            out = img.copy()
            out[self.H*i:self.H*(i+1),:,:] = (0,0,0)

            imgs[player] = out
            if save:
                out = Image.fromarray(out)
                os.makedirs(os.path.join(self.out,'players',player), exist_ok=True)
                pathOut = os.path.join(self.out,'players',player,f"round_{self.round:04d}.jpg")
                out.save(os.path.join(pathOut))
                upload_img(pathOut)
        return imgs
    def fix_path(self,path):
        return path.replace('\\','/')
    def single_turn(self, result, players):
        ans = self.gen_ans_img(result, save = True)
        _ = self.gen_player_img(ans, players, save = True)

def get_player():
    n = int(input("Enter number of players: "))
    players = []
    for i in range(n):
        player = input("Enter player's name: ")
        players.append(player)
    return players
def get_word(n, words = []):
    while(True):

        print(f'Total number of words: {len(words)}')
        w = input("Enter word: ")
        #print(w)
        if w.lower()=='stop':
            if len(words)>=n:
                print('Stop collecting word...')
                return words
            else:
                print('number of word should greater or equal to number of player')
                print('please insert again')
        else:
            if w in words:
                print('duplicate word, please insert again')
            else:
                words.append(w)
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
    return words

def get_state(words0,n):
    prev_word = True
    extend = True
    while(prev_word):
        act = input("use previous words collection?? <y/n>: ")

        # User previous word collection
        if act.lower() == 'y':
            if len(words0)<n:
                print('WARNING: NUMBER OF PLAYER LESS THAN WORD')
                extend = True
                prev_word = False
            else:
                return 1 # use previous word collection

        elif act.lower() =='n':
            prev_word = False
            #return 0 # recollect word
        elif act.lower()=='stop':
            return -1
        else:
            print('Incorrect input')

    while(extend):
        act = input("extend words collection?? <y/n>: ")

        if act.lower()=='y':
            print('extend word')
            return 2 # extend word
        elif act.lower()=='n':
            if len(words0)<n:
                print('WARNING: NUMBER OF PLAYER LESS THAN WORD')
                print('extend word collection')
                return 2
            else:
                return 1 # use previous word collection
        elif act.lower()=='stop':
            return -1
        else:
            print('Incorrect input')

def act(state, words,n):
    if state==0:
        print('recollect word collection')
        return get_word(n,words = [])
    if state==1:
        print('use previous word collection')
        return words
    if state ==2:
        print('extend word collection')
        return get_word(n, words=words)
    if state ==-1:
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print('Thank you for playing')
        exit()

def run():
    start = True
    while (True):
        if start:
            players = get_player()
            num_player = len(players)
            start = False
            print(f"Welcome {players}")
            words = get_word(num_player, words=[])
        # words = words0#.copy()
        print(f'number of word = {len(words)}, number of player = {num_player}')
        result = {p: word_random(words) for p in players}
        tb = TabooImage(**conf.img)
        tb.single_turn(result, players)
        print(f'---------------------------------------- DONE: {tb.out}, {tb.round:04d}.jpg ----------------------------------------')
        print(f'word left = {len(words)}')
        words = act(get_state(words, num_player), words, num_player)

if __name__ == '__main__':
    conf = Conf()
    run()





