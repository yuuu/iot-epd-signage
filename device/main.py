#!/usr/bin/env python3

import signal
import RPi.GPIO as GPIO
from paper import Paper
from logo import Logo
from event import Event
from message import Message

from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto

def show(img):
    inky = auto(ask_user=True, verbose=True)
    img = img.resize(inky.resolution)
    inky.set_image(img, saturation = 0.5)
    inky.show()


def show_logo():
    paper = Paper()
    logo = Logo(paper)
    logo.show()

def show_event(msg):
    print(msg)
    paper = Paper()
    event = Event(
        paper,
        "ハイブリッドで\nFusic Tech Live Vol.17\nAWS re:Invent 振り返り会",
        "19:00",
        "21:00"
    )
    event.show()

message = Message()
message.publish()
message.subscribe(show_event)

