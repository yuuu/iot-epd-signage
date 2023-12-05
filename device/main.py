#!/usr/bin/env python3

import signal
import RPi.GPIO as GPIO

from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto

BUTTONS = [5, 6, 16, 24]
LABELS = ['A', 'B', 'C', 'D']

def show(img):
    inky = auto(ask_user=True, verbose=True)
    img = img.resize(inky.resolution)
    inky.set_image(img, saturation = 0.5)
    inky.show()


def show_logo():
    show(Image.open("./template/logo.png"))


def show_event_header(img):
    font = ImageFont.truetype('./GenShinGothic-Normal.ttf', 32)
    draw = ImageDraw.Draw(img)
    draw.text((260, 20), '2023年11月17日(金曜日)\n本日のイベント', 'black', font=font)


def show_event_body(img):
    font = ImageFont.truetype('./GenShinGothic-Normal.ttf', 28)
    draw = ImageDraw.Draw(img)
    draw.text((260, 80), """
19:00-21:00
ハイブリッドで
Fusic Tech Live Vol.17
AWS re:Invent 振り返り会
""", 'black', font=font)


def show_event_footer(img):
    font = ImageFont.truetype('./GenShinGothic-Normal.ttf', 28)
    draw = ImageDraw.Draw(img)
    draw.text((260, 340), 'ぜひご参加ください！', 'black', font=font)


def show_event():
    inky = auto(ask_user=True, verbose=True)
    img = Image.open("./template/event.png")
    img = img.resize(inky.resolution)
    show_event_header(img)
    show_event_body(img)
    show_event_footer(img)
    show(img)


def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    if label == 'A':
        show_logo()
    elif label == 'B':
        show_event()


def init_buttons():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for pin in BUTTONS:
        GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)


init_buttons()
signal.pause()
