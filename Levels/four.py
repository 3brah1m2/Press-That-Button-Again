import pygame as pg
from five import Five

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

class Four():
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        # Load images
        idle = pg.image.load("resources/open.png").convert_alpha()
        clicked = pg.image.load("resources/closed.png").convert_alpha()
        self.boulder = pg.transform.scale(pg.image.load('resources/boulder.png').convert_alpha(), (120, 120))
        self.feather = pg.transform.scale(pg.image.load('resources/feather.png').convert_alpha(), (120, 120))
        self.trophy = pg.transform.scale(pg.image.load('resources/trophy.png').convert_alpha(), (120, 120))
        self.button_idle = pg.transform.scale(idle, (350, 200))
        self.button_click = pg.transform.scale(clicked, (350, 200))

        self.button_rect = self.button_idle.get_rect(topleft=(220, 175))
        self.button_current = self.button_idle

        # Track draggable objects
        self.objects = {
            "boulder": {"surf": self.boulder, "rect": self.boulder.get_rect(topleft=(50, 200)), "dragging": False},
            "feather": {"surf": self.feather, "rect": self.feather.get_rect(topleft=(600, 200)), "dragging": False},
            "trophy": {"surf": self.trophy, "rect": self.trophy.get_rect(topleft=(330, 380)), "dragging": False},
        }
        for obj in self.objects.values():
            obj["original_y"] = obj["rect"].y
            obj["falling"] = False

        # Font and text
        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 4: Something Heavy", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(topleft=(20, 20))
        self.fontl = pg.font.SysFont(None, 100)
        self.textl = self.fontl.render("Level Passed", True, (0, 255, 0))
        self.text_rectl = self.textl.get_rect(center=(self.width // 2, self.height // 2))

        # Load sounds
        self.click_sound = pg.mixer.Sound("resources/button click.mp3")
        self.stone_sound = pg.mixer.Sound("resources/stone drop.mp3")
        self.metal_sound = pg.mixer.Sound("resources/metal falling.mp3")
        self.level_passed_sound = pg.mixer.Sound('resources/level passed.mp3')
        # State
        self.transitioning = False
        self.transition_start = None
        self.sfx_played = set()

    def run(self):
        running = True
        selected_obj = None
        offset_x = 0
        offset_y = 0

        while running:
            self.screen.fill((0, 0, 0))
            now = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    for key, obj in self.objects.items():
                        if obj["rect"].collidepoint(event.pos):
                            selected_obj = key
                            obj["dragging"] = True
                            offset_x = obj["rect"].x - event.pos[0]
                            offset_y = obj["rect"].y - event.pos[1]

                elif event.type == pg.MOUSEBUTTONUP:
                    if selected_obj:
                        obj = self.objects[selected_obj]
                        obj["dragging"] = False
                        obj["falling"] = True
                    selected_obj = None

                elif event.type == pg.MOUSEMOTION and selected_obj:
                    obj = self.objects[selected_obj]
                    if obj["dragging"]:
                        obj["rect"].x = event.pos[0] + offset_x
                        obj["rect"].y = event.pos[1] + offset_y

            # Handle falling animation
            for key, obj in self.objects.items():
                if obj["falling"]:
                    if obj["rect"].y < obj["original_y"]:
                        obj["rect"].y += 10
                        if obj["rect"].y > obj["original_y"]:
                            obj["rect"].y = obj["original_y"]
                    else:
                        obj["falling"] = False

                    # Play sound once when it hits ground level (not necessarily the button)
                    if key not in self.sfx_played and obj["rect"].y >= obj["original_y"]:
                        self.sfx_played.add(key)
                        if key == "boulder":
                            if obj["rect"].colliderect(self.button_rect) and not self.transitioning:
                                self.stone_sound.play()
                                self.click_sound.play()
                                self.transitioning = True
                                self.transition_start = now
                                self.button_current = self.button_click
                            else:
                                self.stone_sound.play()
                        elif key == "trophy":
                            self.metal_sound.play(maxtime=900)  # Play only ~0.9 sec of metal sound

            # Handle transition after button press
            if self.transitioning:
                if now - self.transition_start >= int(self.click_sound.get_length() * 1000) + 200:
                    self.screen.fill((0, 0, 0))
                    self.screen.blit(self.textl, self.text_rectl)
                    self.level_passed_sound.play()
                    pg.display.flip()
                    pg.time.delay(1000)
                    Five().run()
                    return

            self.screen.blit(self.button_current, self.button_rect.topleft)
            for obj in self.objects.values():
                self.screen.blit(obj["surf"], obj["rect"].topleft)
            self.screen.blit(self.text, self.text_rect)

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

if __name__ == "__main__":
    Four().run()
