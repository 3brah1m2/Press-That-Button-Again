import pygame as pg
from four import Four

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

class Three():
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
        self.level_passed_sound = pg.mixer.Sound('resources/level passed.mp3')
        # Fonts
        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 3: Hold it", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(topleft=(20, 20))

        self.fontl = pg.font.SysFont(None, 100)
        self.textl = self.fontl.render("Level Passed", True, (0, 255, 0))
        self.text_rectl = self.textl.get_rect(center=(self.width // 2, self.height // 2))

        # State
        self.holding = False
        self.hold_start_time = None
        self.level_passed = False
        self.pass_display_start = None

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            now = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos) and not self.holding and not self.level_passed:
                        self.button_current = self.button_click
                        self.holding = True
                        self.hold_start_time = now

                        # Only play sound once
                        if not pg.mixer.get_busy():
                            self.click_sound.play()

                elif event.type == pg.MOUSEBUTTONUP:
                    if self.holding:
                        self.button_current = self.button_idle
                        self.holding = False
                        self.hold_start_time = None

            # Check if held long enough
            if self.holding and self.hold_start_time:
                if now - self.hold_start_time >= 3000:
                    self.level_passed = True
                    self.holding = False
                    self.button_current = self.button_idle
                    self.pass_display_start = now

            # Handle level passed display
            if self.level_passed:
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.textl, self.text_rectl)
                self.level_passed_sound.play()
                if now - self.pass_display_start >= 1000:
                    Four().run()
                    return
            else:
                self.screen.blit(self.button_current, self.button_rect.topleft)
                self.screen.blit(self.text, self.text_rect)

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

if __name__ == "__main__":
    Three().run()
