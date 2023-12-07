from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

class Event:
    def __init__(self, paper, name, started_at, ended_at):
        self.name = name
        self.started_at = started_at
        self.ended_at = ended_at
        self.inky = auto(ask_user=True, verbose=True)


    def show(self):
        img = Image.open("./template/event.png")
        img = img.resize(self.inky.resolution)

        self.__header(img)
        self.__body(img)
        self.__footer(img)

        self.inky.set_image(img, saturation = 0.5)
        self.inky.show()


    def __header(self, img):
        now = datetime.now()
        font = ImageFont.truetype('./GenShinGothic-Normal.ttf', 32)
        draw = ImageDraw.Draw(img)
        draw.text((260, 20), f'{now.year}年{now.month}月{now.day}日\n本日のイベント', 'black', font=font)
    

    def __body(self, img):
        font = ImageFont.truetype('./GenShinGothic-Normal.ttf', 28)
        draw = ImageDraw.Draw(img)
        draw.text((260, 80), f"""
{self.started_at}-{self.ended_at}
{self.name}
""", 'black', font=font)


    def __footer(self, img):
        font = ImageFont.truetype('./GenShinGothic-Normal.ttf', 28)
        draw = ImageDraw.Draw(img)
        draw.text((260, 340), 'ぜひご参加ください！', 'black', font=font)

