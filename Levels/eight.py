import pygame as pg
import random
from nine import Nine
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

class Eight:
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        # Load button images
        idle = pg.image.load("resources/open.png").convert_alpha()
        clicked = pg.image.load("resources/closed.png").convert_alpha()

        self.button_idle = pg.transform.scale(idle, (100, 55))
        self.button_click = pg.transform.scale(clicked, (100, 55))

        self.button_pos_w, self.button_pos_h = random.randint(100, 700), random.randint(55, 445)
        self.button_rect = self.button_idle.get_rect(topleft=(self.button_pos_w, self.button_pos_h))
        self.button_current = self.button_idle

        # Load sound effect
        self.click_sound = pg.mixer.Sound("resources/button click.mp3")
        self.click_duration = int(self.click_sound.get_length() * 1000)  # duration in milliseconds
        self.level_passed_sound = pg.mixer.Sound('resources/level passed.mp3')
        # Font for text
        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 8: Hidden in The Shadows", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(topleft=(20, 20))

        self.fontl = pg.font.SysFont(None, 100)
        self.textl = self.fontl.render("Level Passed", True, (0, 255, 0))
        self.text_rectl = self.textl.get_rect(center=(self.width // 2, self.height // 2))

        # Timing control
        self.click_start_time = None
        self.show_text_time = None
        
    def run(self):
        print(self.button_pos_w, self.button_pos_h)
        RADIUS = 120  # circle radius
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            now = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos) and not self.click_start_time:
                        self.click_sound.play()
                        self.button_current = self.button_click
                        self.click_start_time = now

            mx, my = pg.mouse.get_pos()

            # --- Draw text (always visible) ---
            self.screen.blit(self.text, self.text_rect)

            # --- Create spotlighted button surface ---
            button_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
            button_surface.blit(self.button_current, self.button_rect.topleft)

            # Create a circular mask (white = visible, black = hidden)
            mask_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
            mask_surface.fill((0, 0, 0, 255))
            pg.draw.circle(mask_surface, (255, 255, 255, 255), (mx, my), RADIUS)

            # Apply the mask
            button_surface.blit(mask_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

            # Handle click sequence
            if self.click_start_time:
                elapsed = now - self.click_start_time
                if elapsed < self.click_duration:
                    self.screen.blit(button_surface, (0, 0))
                elif not self.show_text_time:
                    self.show_text_time = now
                elif now - self.show_text_time < 1000:
                    self.screen.fill((0,0,0))
                    self.screen.blit(self.textl, self.text_rectl)
                    self.level_passed_sound.play()
                else:
                    Nine().run()
                    return
            else:
                self.screen.blit(button_surface, (0, 0))

            # Draw the outline of the radius
            pg.draw.circle(self.screen, (0, 100, 255), (mx, my), RADIUS, 2)

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()


if __name__ == "__main__":
    Eight().run()
