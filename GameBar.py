import pygame
from Constants import *
from button import *

class GameBar(object):
    BG_COLOR = 0, 0, 0 # black
    QBTN_BG = 255, 0, 0 # red
    QBTN_HOVER = 255, 255, 0 # yellow
    QBTN_TXT = "Quit"
    SCORE_COLOR = 255, 255, 255 # white
    SCORE_FONT_SIZE = 25

    def __init__(self, qfn=None, pid=None, snakes=None, font_size=SCORE_FONT_SIZE):
        # bar stuff
        self.x = SCR_WID
        self.y = 0
        self.w = BAR_WID
        self.h = SCR_HGT

        # quit button stuff
        self.qbtn_x = SCR_WID + int(BAR_WID * 0.1)
        self.qbtn_y = int(SCR_HGT * 0.82)
        self.qbtn_w = int(BAR_WID * 0.8)
        self.qbtn_h = int(SCR_HGT * 0.16)
        self.qfn = qfn

        # score stuff
        self.player_id = pid
        self.snakes = snakes # hold snakes for score
        self.score_x = SCR_WID + int(BAR_WID * 0.1)
        self.score_y = int(SCR_HGT * 0.02)
        self.score_w = int(BAR_WID * 0.8)
        self.font_size = font_size
        self.score_gap = int(SCR_HGT * 0.01)

    def blitText(self, screen, text, x, y):
        font = pygame.font.Font(None, self.font_size)
        show_text = font.render(text, 1, GameBar.SCORE_COLOR)
        screen.blit(show_text, (x, y))

    def blit(self, screen):
        # draw background first
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, GameBar.BG_COLOR, rect)

        # scores
        entry_y = self.score_y
        if self.player_id and self.player_id in self.snakes:
            player_text = "You: " + self.snakes[self.player_id].getName()
            self.blitText(screen, player_text, self.score_x, entry_y)
            entry_y += self.font_size + 5 * self.score_gap

        if self.snakes:
            scores = [(s.getName(), s.getScore()) for s in self.snakes.values()]
            scores.sort(key=lambda x: x[1], reverse=True)
            for name, score in scores:
                score_text = name + ": " + str(score)
                self.blitText(screen, score_text, self.score_x, entry_y)
                entry_y += self.font_size + self.score_gap / 5

        # quit btn
        self.qbtn = button(GameBar.QBTN_TXT, self.qbtn_x, self.qbtn_y, 
                           self.qbtn_w, self.qbtn_h, GameBar.QBTN_BG,
                           GameBar.QBTN_HOVER, screen, self.qfn)
