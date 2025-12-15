import pygame

from projectile import Bullet

gunshot_sound = pygame.mixer.Sound("assets/gun_shot.mp3")
gunshot_sound.set_volume(0.05)

class Gun:
    def __init__(self, name, cooldown):
        self.name = name
        
        self.base_cooldown = cooldown
        self.current_cooldown = 0

    def shoot(self, player_position, angle):
        if self.current_cooldown == 0:
            self.current_cooldown = self.base_cooldown
            gunshot_sound.play()
            return Bullet(player_position, angle)
        else:
            return None

    def update(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

class Revolver(Gun):
    def __init__(self):
        super().__init__("Revolver", 120)

class Guns:
    def __init__(self):
        self.gun_inventory = [Revolver()]
        self.guns_list = {
            "Revolver": Revolver,
        }
    
    def pickup(self, gun_name):
        if gun_name in self.guns_list:
            self.gun_inventory.append(self.guns_list[gun_name]())
