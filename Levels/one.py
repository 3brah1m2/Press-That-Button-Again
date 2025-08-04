import pygame as pg
from two import Two
pg.init()

class One():
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        # Load both button states
        idle = pg.image.load("resources/open.png").convert_alpha()
        clicked = pg.image.load("resources/closed.png").convert_alpha()

        self.button_idle = pg.transform.scale(idle, (350, 200))
        self.button_click = pg.transform.scale(clicked, (350, 200))

        self.button_rect = self.button_idle.get_rect(topleft=(220, 175))
        self.button_current = self.button_idle
        self.clicked_time = None

        # Font for text
        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 1: Press", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(topleft=(20, 20))

        self.fontl = pg.font.SysFont(None, 100)
        self.textl = self.fontl.render("Level Passed", True, (0, 255, 0))
        self.text_rectl = self.textl.get_rect(center=(self.width // 2, self.height // 2))
    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            now = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        print("Button clicked!")
                        self.button_current = self.button_click
                        self.clicked_time = now
                        pg.display.flip()
                        self.screen.blit(self.textl, self.text_rectl)
                        pg.display.flip()
                        pg.time.delay(1000) 
                        Two().run()


            if self.clicked_time and now - self.clicked_time > 100:
                self.button_current = self.button_idle
                self.clicked_time = None

            self.screen.blit(self.button_current, self.button_rect.topleft)
            self.screen.blit(self.text, self.text_rect)

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()


if __name__ == "__main__":
    One().run()
