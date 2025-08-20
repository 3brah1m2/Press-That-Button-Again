import pygame as pg

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

class Nine():
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        # Load button images (hidden at first)
        idle = pg.image.load("resources/open.png").convert_alpha()
        clicked = pg.image.load("resources/closed.png").convert_alpha()
        self.button_idle = pg.transform.scale(idle, (350, 200))
        self.button_click = pg.transform.scale(clicked, (350, 200))
        self.button_rect = self.button_idle.get_rect(center=(self.width // 2, self.height // 2))
        self.button_current = self.button_idle
        self.show_button = False

        # Load sound effect
        self.click_sound = pg.mixer.Sound("resources/button click.mp3")
        self.click_duration = int(self.click_sound.get_length() * 1000)
        self.level_passed_sound = pg.mixer.Sound('resources/fanfare.mp3')
        self.light = pg.mixer.Sound('resources/light turn on.mp3')

        # Font for text
        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 9: The Last of Them All and The Brightest", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(topleft=(20, 20))

        self.fontl = pg.font.SysFont(None, 75)
        self.textl = self.fontl.render("You Finished The Game!!", True, (0, 255, 0))
        self.text_rectl = self.textl.get_rect(center=(self.width // 2, self.height // 2))

        # Timing control
        self.click_start_time = None
        self.show_text_time = None

        # Light bulb images (smaller)
        bulb_off = pg.image.load("resources/lightbulb.png").convert_alpha()
        bulb_on = pg.image.load("resources/light bulb lit.png").convert_alpha()
        self.bulb_off = pg.transform.scale(bulb_off, (70, 100))
        self.bulb_on = pg.transform.scale(bulb_on, (70, 100))

        # Predetermined positions (left, right, bottom)
        margin = 20
        self.positions = [
            self.bulb_off.get_rect(midleft=(margin, self.height // 2)),        # left
            self.bulb_off.get_rect(midright=(self.width - margin, self.height // 2)), # right
            self.bulb_off.get_rect(midbottom=(self.width // 2, self.height - margin)) # bottom
        ]

        # Start with only the first bulb
        self.bulbs = [{"rect": self.positions[0], "lit": False}]
        self.current_index = 0

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            now = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Handle bulbs in order
                    for i, bulb in enumerate(self.bulbs):
                        if bulb["rect"].collidepoint(event.pos) and not bulb["lit"]:
                            bulb["lit"] = True
                            self.light.play()

                            # If more bulbs are left, add the next one
                            if self.current_index + 1 < len(self.positions):
                                self.current_index += 1
                                self.bulbs.append({"rect": self.positions[self.current_index], "lit": False})
                            break

                    # Check if all bulbs are lit → show button
                    if len(self.bulbs) == len(self.positions) and all(b["lit"] for b in self.bulbs):
                        self.show_button = True

                    # Handle button click if visible
                    if self.show_button and self.button_rect.collidepoint(event.pos) and not self.click_start_time:
                        self.click_sound.play()
                        self.button_current = self.button_click
                        self.click_start_time = now

            # Draw bulbs
            for bulb in self.bulbs:
                img = self.bulb_on if bulb["lit"] else self.bulb_off
                self.screen.blit(img, bulb["rect"].topleft)

            # Draw button if unlocked
            if self.show_button:
                if self.click_start_time:
                    elapsed = now - self.click_start_time
                    if elapsed < self.click_duration:
                        self.screen.blit(self.text, self.text_rect)
                        self.screen.blit(self.button_current, self.button_rect.topleft)
                    elif not self.show_text_time:
                        self.show_text_time = now
                    elif now - self.show_text_time < 13000:
                        self.screen.fill((0, 0, 0))
                        self.screen.blit(self.textl, self.text_rectl)
                        self.level_passed_sound.play()
                else:
                    self.screen.blit(self.button_current, self.button_rect.topleft)

            # Always draw level text
            self.screen.blit(self.text, self.text_rect)

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

if __name__ == "__main__":
    Nine().run()
