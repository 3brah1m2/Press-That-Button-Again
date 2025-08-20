import pygame as pg
from six import Six
pg.init()

class Five():
    def __init__(self):
        self.width, self.height = 800, 500
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        self.idle = pg.transform.scale(pg.image.load('resources/open.png'), (350, 200))
        self.closed = pg.transform.scale(pg.image.load('resources/closed.png'), (350, 200))

        self.screwdriver = pg.transform.scale(pg.image.load('resources/screwdriver.png').convert_alpha(), (150, 150))
        self.hammer = pg.transform.scale(pg.image.load('resources/hammer.png').convert_alpha(), (120, 220))
        self.wrench = pg.transform.scale(pg.image.load('resources/wrench.png').convert_alpha(), (120, 120))

        self.button_rect = self.idle.get_rect(topleft=(220, 175))
        self.button_current = self.idle
        self.clicked_time = None
        self.level_passed = False
        self.button_enabled = False

        self.wall_rect = pg.Rect(self.button_rect.x, self.button_rect.y, self.button_rect.width, 200)
        self.wall_falling = False
        self.wall_fallen = False
        self.wall_speed = 10

        self.screws = [True] * 4
        self.screw_rects = [
            pg.Rect(self.wall_rect.left + 10, self.wall_rect.top + 10, 20, 20),
            pg.Rect(self.wall_rect.right - 30, self.wall_rect.top + 10, 20, 20),
            pg.Rect(self.wall_rect.left + 10, self.wall_rect.bottom - 30, 20, 20),
            pg.Rect(self.wall_rect.right - 30, self.wall_rect.bottom - 30, 20, 20)
        ]
        self.screws_to_remove = []

        self.objects = {
            "screwdriver": {"surf": self.screwdriver, "rect": self.screwdriver.get_rect(topleft=(50, 200)), "dragging": False},
            "hammer": {"surf": self.hammer, "rect": self.hammer.get_rect(topleft=(600, 200)), "dragging": False},
            "wrench": {"surf": self.wrench, "rect": self.wrench.get_rect(topleft=(330, 380)), "dragging": False},
        }

        for obj in self.objects.values():
            obj["original_y"] = obj["rect"].y
            obj["falling"] = False

        self.selected_obj = None
        self.offset_x = 0
        self.offset_y = 0

        self.unscrew_sound = pg.mixer.Sound("resources/unscrewing.mp3")
        self.metal_fall_sound = pg.mixer.Sound("resources/metal falling.mp3")
        self.button_click_sound = pg.mixer.Sound("resources/button click.mp3")
        self.level_passed_sound = pg.mixer.Sound('resources/level passed.mp3')

        self.metal_fall_played = False
        self.unscrewing_playing = False
        self.unscrew_start_time = 0
        self.unscrew_duration = 1500  # milliseconds

        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render("Lvl 5: Mechanic", True, (255, 255, 255))
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
                    for key, obj in self.objects.items():
                        if obj["rect"].collidepoint(event.pos):
                            if key == "screwdriver" and self.unscrewing_playing:
                                continue
                            self.selected_obj = key
                            obj["dragging"] = True
                            self.offset_x = obj["rect"].x - event.pos[0]
                            self.offset_y = obj["rect"].y - event.pos[1]

                    if self.button_enabled and self.button_rect.collidepoint(event.pos):
                        self.button_click_sound.play()
                        self.button_current = self.closed
                        self.clicked_time = now
                        self.level_passed = True

                elif event.type == pg.MOUSEBUTTONUP:
                    if self.selected_obj:
                        obj = self.objects[self.selected_obj]
                        obj["dragging"] = False

                        if self.selected_obj == "screwdriver":
                            for i in range(4):
                                if self.screws[i] and obj["rect"].colliderect(self.screw_rects[i]):
                                    if i not in self.screws_to_remove:
                                        self.unscrewing_playing = True
                                        self.unscrew_start_time = now
                                        self.screws_to_remove.append(i)
                                        self.unscrew_sound.play()
                        else:
                            obj["falling"] = True

                    self.selected_obj = None

                elif event.type == pg.MOUSEMOTION and self.selected_obj:
                    obj = self.objects[self.selected_obj]
                    if obj["dragging"] and not (self.selected_obj == "screwdriver" and self.unscrewing_playing):
                        obj["rect"].x = event.pos[0] + self.offset_x
                        obj["rect"].y = event.pos[1] + self.offset_y

            # Screw removal after sound finishes
            if self.unscrewing_playing and now - self.unscrew_start_time >= self.unscrew_duration:
                self.unscrewing_playing = False
                for i in self.screws_to_remove:
                    self.screws[i] = False
                self.screws_to_remove.clear()

            # Handle object falling
            for key, obj in self.objects.items():
                if key == "screwdriver" and self.unscrewing_playing:
                    continue
                if obj["falling"]:
                    if obj["rect"].y < obj["original_y"]:
                        obj["rect"].y += 10
                        if obj["rect"].y > obj["original_y"]:
                            obj["rect"].y = obj["original_y"]
                    else:
                        obj["falling"] = False

            if not self.wall_falling and all(not screw for screw in self.screws):
                self.wall_falling = True

            if self.wall_falling:
                self.wall_rect.y += self.wall_speed
                for rect in self.screw_rects:
                    rect.y += self.wall_speed
                if self.wall_rect.top > self.height:
                    if not self.metal_fall_played:
                        self.metal_fall_sound.play()
                        self.metal_fall_played = True
                    self.wall_falling = False
                    self.wall_fallen = True
                    self.button_enabled = True

            if self.clicked_time and now - self.clicked_time > 100:
                self.button_current = self.idle
                self.clicked_time = None

            # Draw UI
            self.screen.blit(self.button_current, self.button_rect.topleft)

            if not self.wall_fallen:
                pg.draw.rect(self.screen, (100, 100, 100), self.wall_rect)
                for i in range(4):
                    if self.screws[i]:
                        center = self.screw_rects[i].center
                        pg.draw.circle(self.screen, (30, 30, 30), center, 10)

            for obj in self.objects.values():
                self.screen.blit(obj["surf"], obj["rect"].topleft)

            if self.level_passed:
                self.unscrew_sound.stop()
                self.metal_fall_sound.stop()
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.textl, self.text_rectl)
                self.level_passed_sound.play()
                pg.display.flip()
                pg.time.delay(1000)
                Six().run()

            self.screen.blit(self.text, self.text_rect)
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

if __name__ == "__main__":
    Five().run()
