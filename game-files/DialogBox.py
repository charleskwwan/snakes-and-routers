import pygame
from button import *

class DialogBox(object):
    BG_COLOR = 0, 0, 0 # black
    BTN_BG = 255, 0, 0 # red
    BTN_HOVER = 255, 255, 0 # yellow
    DIALOG_COLOR = 255, 255, 255 # white
    BOX_FONT_SIZE = 25

    # msg: to be displayed, action: when button pressed
    def __init__(self, x, y, w, h, dialog=None, btn_txt=None, action=None,
                 font_size=BOX_FONT_SIZE):
        # positioning
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # dialog stufff
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.dialog = []
        # set dialog based on width to wrap in dialog box
        # if too long for h, too bad
        # if word too long for w, too bad
        accu = "" 
        for word in dialog.split(" "):
            test = accu + word + " "
            if self.font.size(test)[0] < int(w * 0.90):
                accu = test
            else:
                self.dialog.append(accu)
                accu = word + " "
        self.dialog.append(accu)

        # btn stuff
        self.btn_txt = btn_txt
        self.action = action # triggered when the button is pressed
        self.btn_x = x + w / 4
        self.btn_y = y + int(h * 0.75)
        self.btn_w = w / 2
        self.btn_h = int(h * 0.2)

    def blit(self, screen):
        # background box
        bg = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, DialogBox.BG_COLOR, bg)

        # dialog
        txt_y = self.y + int(self.h * 0.05)
        for line in self.dialog:
            line_text = self.font.render(line, 1, DialogBox.DIALOG_COLOR)
            txt_x = self.x + (self.w - self.font.size(line)[0]) / 2
            screen.blit(line_text, (txt_x, txt_y))
            txt_y += self.font_size

        # button
        self.btn = button(self.btn_txt, self.btn_x, self.btn_y, self.btn_w, 
                          self.btn_h, DialogBox.BTN_BG, DialogBox.BTN_HOVER,
                          screen, self.action)
