import pygame as pg
from seven import Seven
pg.init()

class Six:
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        # Button images
        self.idle = pg.transform.scale(pg.image.load('resources/open.png'), (350, 200))
        self.closed = pg.transform.scale(pg.image.load('resources/closed.png'), (350, 200))
        self.button_rect = self.idle.get_rect(topleft=(220, 175))
        self.button_current = self.idle
        self.clicked_time = None

        # Clock faces (images)
        self.clock_faces = ["3", "6", "9", "12"]
        self.clock_images = {
            face: pg.transform.scale(pg.image.load(f"resources/{face}.png"), (100, 100))
            for face in self.clock_faces
        }
        self.current_clock_index = 3  
        self.current_clock_face = self.clock_faces[self.current_clock_index]
        self.clock_image = self.clock_images[self.current_clock_face]
        self.clock_rect = self.clock_image.get_rect(center=(self.width // 2, 100))

        self.button_enabled = (self.current_clock_face == "6")

        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 6: Time Traveller", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(topleft=(20, 20))

        self.lvl = False
        
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

                    if self.clock_rect.collidepoint(event.pos):
                        self.current_clock_index = (self.current_clock_index + 1) % 4
                        self.current_clock_face = self.clock_faces[self.current_clock_index]
                        self.clock_image = self.clock_images[self.current_clock_face]
                        self.clock_rect = self.clock_image.get_rect(center=(self.width // 2, 100))
                        self.button_enabled = (self.current_clock_face == "6")

                    elif self.button_enabled and self.button_rect.collidepoint(event.pos):
                        print("Button clicked!")
                        self.button_current = self.closed
                        self.clicked_time = now
                        self.lvl = True
                        pg.display.flip()

            if self.clicked_time and now - self.clicked_time > 100:
                self.button_current = self.idle
                self.clicked_time = None

            self.screen.blit(self.clock_image, self.clock_rect)
            self.screen.blit(self.button_current, self.button_rect.topleft)
            self.screen.blit(self.text, self.text_rect)

            if self.lvl:
                self.screen.fill((0,0,0))
                self.screen.blit(self.textl, self.text_rectl)
                pg.display.flip()
                pg.time.delay(1000) 
                Seven().run()
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

if __name__ == "__main__":
    Six().run()
