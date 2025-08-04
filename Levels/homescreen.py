import pygame as pg
from one import One
pg.init()
class Menu():
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)

        image = pg.image.load("resources/title.png").convert_alpha()
        self.image = pg.transform.scale(image, (600, 270))

        start_image = pg.image.load("resources/start.png").convert_alpha()
        self.start = pg.transform.scale(start_image, (250, 100))
        self.start_rect = self.start.get_rect(topleft=(250, 350))

    def run(self):
        running = True
        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.start_rect.collidepoint(event.pos):
                        print("Start Button Clicked")
                        One().run()


            self.screen.blit(self.image, (90, 50))
            self.screen.blit(self.start, self.start_rect.topleft)
            pg.display.flip()

Menu().run()
