import pygame

class Button:
    def __init__(self, view, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.view = view
        self.hovered = False

    def draw(self):
        color_bg = self.view.rock if self.hovered else self.view.color_bg2

        pygame.draw.rect(self.view.screen, color_bg, [
                         self.x, self.y, self.width, self.height])
        self.view.print_text(self.text, self.view.player,
                             self.x, self.y, self.view.font_small)

    def inside(self, x, y):
        return self.x <= x <= self.x+self.width and self.y <= y <= self.y+self.height