import pygame
import toolbox
import random
import image_util
from score_manager import Background

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen, center):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.containers = None
        self.screen = screen
        self.x = center[0]
        self.y = center[1]

        self.type = random.choice(['health_point', 'reload', 'speed'])


        self.powerup_images = {'health_point': pygame.image.load(image_util.getImage("pill_red.png")).convert(),
                               'reload': pygame.image.load(image_util.getImage("reload.png")).convert(),
                               'speed': pygame.image.load(image_util.getImage('bolt_gold.png')).convert()}

        self.image = self.powerup_images[self.type]
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.reload_cooldown = 0
        self.reload_cooldown_max = 600

        self.kill_timer = 300
        self.reload_timer = 240
        self.speed_timer = 240

        self.r_flag = False
        self.s_flag = False

    def update(self, player):

        if self.r_flag:
            if self.reload_timer >= 0:
                self.reload_timer -= 1
            else:
                self.up_reload(player, True)
                self.kill()

        elif self.s_flag:
            if self.speed_timer >= 0:
                self.speed_timer -= 1
            else:
                self.up_reload(player, False)
                self.kill()
        else:
            self.rect.center = [self.x - Background.display_scroll[0], self.y - Background.display_scroll[1]]
            if self.kill_timer >= 0:
                self.kill_timer -= 1
            else:
                self.kill()


        self.screen.blit(self.image, self.rect)

    def regen_hp(self, player):
        player.health += random.randrange(0.1*player.health_max, 0.2*player.health_max)
        if player.health >= player.health_max:
            player.health = player.health_max

        self.explode()

    def up_reload(self, player, flag):
        buffer = player.start_shoot_cd
        if not flag:
            player.shoot_cooldown_max -= int(0.2 * buffer)
        else:
            player.shoot_cooldown_max += int(0.2 * buffer)

    def up_speed(self, player, flag):
        buffer = player.start_speed
        if not flag:
            player.speed -= int(0.2 * buffer)
        else:
            player.speed += int(0.2 * buffer)

    def hide(self):
        self.rect.center = (100000 - Background.display_scroll[0], 100000 - Background.display_scroll[1])

    def explode(self):
        self.kill()