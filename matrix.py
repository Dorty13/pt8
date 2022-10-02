import sys

import pygame as pg
import random


class MatrixLetters:
    """Класс для отрисовки матрицы"""

    def __init__(self, app):
        """Инилизация класса"""
        self.app = app
        self.letters = 'ASDFGDGDFHSYHFSGFSGGFJJJHGHHFHS95738866583865384658'
        self.font_size = 8
        self.font = pg.font.SysFont('arial', self.font_size, bold=True)
        self.column = self.app.width // self.font_size
        self.drops = [1 for i in range(0,self.column)]

    def _draw_symbols(self):
        """Отрисовка символов на экране"""
        for i in range(0, len(self.drops)):
            char = random.choice(self.letters)
            char_render = self.font.render(char, False, (0, 255, 0))
            position = i * self.font_size, (self.drops[i] - 1) * self.font_size
            self.app.surface.blit(char_render, position)
            if self.drops[i] * self.font_size > self.app.height and random.uniform(0,1) > 0.975:
                self.drops[i] = 0
            self.drops[i] = self.drops[i] + 1


    def run(self):
        self._draw_symbols()


class MatrixApp:
    """Класс приложения"""
    def __init__(self):
        """Инилизация приложения"""
        self.WINDOW = self.width, self.height = 1000, 700
        pg.init()
        self.screen = pg.display.set_mode(self.WINDOW)
        self.surface = pg.Surface(self.WINDOW, pg.SRCALPHA)
        self.clock = pg.time.Clock()
        self.letters = MatrixLetters(self)

    def _draw_screen(self):
        """Отрисовка экрана"""
        self.surface.fill((0, 0, 0, 10))
        self.letters.run()
        self.screen.blit(self.surface, (0,0))

    def run(self):
        while True:
            self._draw_screen()
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    sys.exit()
            pg.display.flip()
            self.clock.tick(500)


if __name__ == "__main__":
    app = MatrixApp()
    app.run()
