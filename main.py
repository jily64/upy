import json
import random
import numpy
from PIL import Image
class UpGame:
    def __init__(self):
        self.saper = self.Saper


    def selector(self, user_id):
        return True

    class Saper:
        def __init__(self):
            self.matrix = [
                [[1, None, "closed"], [0, None, "closed"], [0, None, "closed"]],
                [[0, None, "closed"], [1, None, "closed"], [0, None, "closed"]],
                [[0, None, "closed"], [0, None, "closed"], [1, None, "closed"]]
            ]

        def generate_new_image(self, user):
            background = Image.open(".res/background.png")
            not_opened = Image.open(".res/nop.png")
            #not_opened = not_opened.convert("RGBA")
            not_opened = not_opened.resize((175, 175))
            for i in range(len(self.matrix)):
                pos = ((i)*200+50, None)
                for j in range(len(self.matrix[i])):
                    pos = (pos[0], (j)*200+100)
                    self.matrix[i][j][2] = pos
                    if self.matrix[i][j][1] == None:
                        self.matrix[i][j][1] = not_opened

                    background.paste(self.matrix[i][j][1], pos, mask=self.matrix[i][j][1])

            background.save(f"{user.id}.png")
            self.im = background
            return f"{user.id}.png"

        def regenerate_image_with_bomb_checker(self, point, user):
            background = Image.open(".res/background.png")

            not_opened = Image.open(".res/nop.png")
            not_opened = not_opened.convert("RGBA")
            not_opened = not_opened.resize((175, 175))

            bomb = Image.open(".res/bomb.png")
            bomb = bomb.convert("RGBA")
            bomb = bomb.resize((175, 175))

            coin = Image.open(".res/coin.png")
            coin = bomb.convert("RGBA")
            coin = bomb.resize((175, 175))

            if self.matrix[point[0]][point[1]][2] == "closed":
                    self.matrix[point[0]][point[1]][2] = "opened"

            if self.matrix[point[0]][point[1]][0] == 1:
                self.matrix[point[0]][point[1]][1] = bomb
                return "lose"
            elif self.matrix[point[0]][point[1]][0] == 1:
                self.matrix[point[0]][point[1]][1] = coin
                return self.generate_new_image(user)




class Game:
    def __init(self):
        with open("data.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def game_selector(self, user_id, message='debug_mode'):
        games = UpGame()

import Bot