import pygame as pg
from three import Three

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

class Two():
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        # Load button images
        idle = pg.image.load("resources/open.png").convert_alpha()
        clicked = pg.image.load("resources/closed.png").convert_alpha()

        self.button_idle = pg.transform.scale(idle, (350, 200))
        self.button_click = pg.transform.scale(clicked, (350, 200))
        self.button_rect = self.button_idle.get_rect(topleft=(220, 175))
        self.button_current = self.button_idle

        # Load sound
        self.click_sound = pg.mixer.Sound("resources/button click.mp3")
        self.click_duration = int(self.click_sound.get_length() * 1000)

        # Font
        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 2: Double Trouble", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(topleft=(20, 20))

        self.fontl = pg.font.SysFont(None, 100)
        self.textl = self.fontl.render("Level Passed", True, (0, 255, 0))
        self.text_rectl = self.textl.get_rect(center=(self.width // 2, self.height // 2))

        # Timing control
        self.clicked = 0
        self.click_start_time = None
        self.show_text_time = None

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            now = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Prevent new click during sound or after 2 clicks
                    if self.button_rect.collidepoint(event.pos) and not self.click_start_time and self.clicked < 2:
                        self.click_sound.play()
                        self.button_current = self.button_click
                        self.click_start_time = now
                        self.clicked += 1

            # Handle click animation
            if self.click_start_time:
                elapsed = now - self.click_start_time
                if elapsed < self.click_duration:
                    self.screen.blit(self.button_current, self.button_rect.topleft)
                elif not self.show_text_time and self.clicked == 2:
                    self.show_text_time = now
                elif self.clicked < 2:
                    self.button_current = self.button_idle
                    self.click_start_time = None

            else:
                self.screen.blit(self.button_current, self.button_rect.topleft)

            # Draw level text unless we're transitioning
            if not self.show_text_time:
                self.screen.blit(self.text, self.text_rect)

            # After 2 clicks and sound is done, show "Level Passed"
            if self.show_text_time:
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.textl, self.text_rectl)
                if now - self.show_text_time > 1000:
                    Three().run()
                    return

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

if __name__ == "__main__":
    Two().run()
