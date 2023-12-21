import json
import random
import numpy
import telegram
from PIL import Image, ImageDraw, ImageFont
import random
class UpGame:
    def __init__(self):
        self.bm = self.bm()

    class bm:
        def __init__(self, bid=None):
            self.bid = None
            self.number = random.randint(10000, 999999)
            self.kef = 2
            self.check_number = 0

        def big_or_small(self, choise):
            self.check_number = random.randint(-1000, 1000)
            print(self.check_number)
            if choise == "Больше":

                if self.check_number > 0:
                    return True
                else:
                    return False
            elif choise == "Меньше":

                if self.check_number < 0:
                    return True
                else:
                    return False


        def generate(self, user:telegram.User):
            # Создаем изображение
            image = Image.new('RGB', (200, 100), color=(255, 0, 255))

            # Загружаем своё собственное изображение фона
            background_image = Image.open("roul_bg.jpg")

            # Масштабируем своё изображение до размеров созданного изображения
            background_image = background_image.resize((200, 100))

            # Наложение изображения фона
            image.paste(background_image, (0, 0))

            # Создаем объект "рисунок"
            draw = ImageDraw.Draw(image)

            # Устанавливаем шрифт и размер
            font = ImageFont.truetype('arial.ttf', 60)

            # Отображаем шестизначное число
            number = random.randint(100000, 999999)

            # Получаем размер текста
            text_bbox = draw.textbbox((0, 0), str(number), font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Определяем координаты для центрирования текста
            text_x = (image.width - text_width) // 2
            text_y = (image.height - text_height) // 2

            # Рисуем текст в центре изображения
            draw.text((text_x, text_y), str(number), font=font, fill=(255, 255, 255))

            # Сохраняем изображение
            image.save(f"{user.id}.png")
            return f"{user.id}.png"


    def selector(self, user_id):
        return True


class Game:
    def __init(self):
        with open("data.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def game_selector(self, user_id, message='debug_mode'):
        games = UpGame()

import Bot