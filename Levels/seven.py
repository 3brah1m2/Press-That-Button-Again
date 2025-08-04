import pygame as pg

pg.init()

class Seven:
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        self.idle = pg.transform.scale(pg.image.load('resources/open.png'), (350, 200))
        self.closed = pg.transform.scale(pg.image.load('resources/closed.png'), (350, 200))
        self.button_rect = self.idle.get_rect(topleft=(220, 175))
        self.button_current = self.idle
        self.clicked_time = None
        self.checking_cursor = False

        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 7: Hit & Run", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(topleft=(20, 20))

        self.font_large = pg.font.SysFont(None, 100)
        self.text_pass = self.font_large.render("Level Passed", True, (0, 255, 0))
        self.text_fail = self.font_large.render("Level Failed", True, (255, 0, 0))
        self.text_rect_large = self.text_pass.get_rect(center=(self.width // 2, self.height // 2))

        self.status = None
        self.status_time = None

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
                        self.button_current = self.closed
                        self.clicked_time = now
                        self.checking_cursor = True
                        self.status = None

            # Check if cursor was removed from the button within 50ms
            if self.checking_cursor and self.clicked_time:
                elapsed = now - self.clicked_time
                if elapsed > 100:
                    if self.button_rect.collidepoint(pg.mouse.get_pos()):
                        self.status = "fail"
                    else:
                        self.status = "pass"
                    self.status_time = now
                    self.checking_cursor = False
                    self.button_current = self.idle

            # Show result
            if self.status == "pass":
                self.screen.fill((0,0,0))
                self.screen.blit(self.text_pass, self.text_rect_large)
                pg.display.flip()
                pg.time.delay(1000)
            elif self.status == "fail":
                self.screen.fill((0,0,0))
                self.screen.blit(self.text_fail, self.text_rect_large)
                pg.display.flip()
                pg.time.delay(1000)
                if now - self.status_time > 1000:
                    self.status = None  # Reset for retry

            self.screen.blit(self.button_current, self.button_rect.topleft)
            self.screen.blit(self.text, self.text_rect)

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

if __name__ == "__main__":
    Seven().run()
