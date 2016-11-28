import pygame
from eztext import Input

class InputBox(Input):
    BG_COLOR = 0, 0, 0 # black
    PROMPT_COLOR = 255, 0, 0 # red
    IN_BG = 255, 255, 255 # white
    IN_COLOR = 0, 0, 0 # black
    BORDER = 5
    FONT_SIZE = 30

    def __init__(self, x, y, w, h, prompt="", border=BORDER, font_size=FONT_SIZE):
        Input.__init__(self, x=x, y=y, prompt=prompt, maxlength=100)

        # positioning
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.border = border
        self.font_size = font_size

        # prompt stuff
        self.prompt = prompt
        self.pr_x = x + border
        self.pr_y = y + border

        # input area stuff
        self.value = ""
        self.in_x = x + border
        self.in_y = y + int(h * 0.4) + border
        self.in_w = w - 2 * border
        self.in_h = int(h * 0.6) - 2 * border

    def getInput(self):
        return self.value

    def blit(self, screen):
        # prepare text
        font = pygame.font.Font(None, self.font_size)
        prompt_text = font.render(self.prompt, 1, InputBox.PROMPT_COLOR)
        input_text = font.render(self.value, 1, InputBox.IN_COLOR)

        # blit stuff
        bg = pygame.Rect(self.x, self.y, self.w, self.h) # box first
        pygame.draw.rect(screen, InputBox.BG_COLOR, bg)
        screen.blit(prompt_text, (self.pr_x, self.pr_y)) # prompt text
        in_area = pygame.Rect(self.in_x, self.in_y, self.in_w, self.in_h) # input area
        pygame.draw.rect(screen, InputBox.IN_BG, in_area)
        screen.blit(input_text, in_area)#, area=in_area)
