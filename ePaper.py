#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

class ePaper:
    def __init(self):
        logging.info("epd2in13_V3 Demo")
    
        self.epd = epd2in13_V3.EPD()
        logging.info("init and Clear")
        self.epd.init()
        self.epd.Clear(0xFF)

        self.font8 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 8)
        self.font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        self.font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

        self.cleared = False

    def clearScreen(self, color=None):
        if color == None:
            self.image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame    
            self.canvas = ImageDraw.Draw(self.image)
        else:
            self.image = Image.new('1', (self.epd.height, self.epd.width), color)  # 255: clear the frame    
            self.canvas = ImageDraw.Draw(self.image)

        self.cleared = True

        # image = image.rotate(180) # rotate
        self.epd.display(self.epd.getbuffer(self.image))

    def drawText(self, x, y, fontsize, text):
        if self.cleared == False:
            logging.warn('Canvas not cleared, I will clear all')
            self.clearScreen()

        # self.canvas.text((120, 60), 'e-Paper demo', font = self.font15, fill = 0)
        self.canvas.text((x, y), u'text', font = self.font8, fill = 0)
        # image = image.rotate(180) # rotate
        self.epd.display(self.epd.getbuffer(self.image))

    # def drawBmp(self, x, y, width, height, path):

    # def drawJpg(self, x, y, width, height, path):