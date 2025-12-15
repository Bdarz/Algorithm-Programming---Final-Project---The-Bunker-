import pygame

from projectile import Bullet

pygame.mixer.init()

# Loads gunshot sounds
gunshot_sound = pygame.mixer.Sound("assets/gun_shot.mp3")
gunshot_sound.set_volume(0.05)

# Base gun class, meant for child classes with unique shoot patterns
class Gun:
    def __init__(self, name, cooldown):
        self.name = name
        
        self.base_cooldown = cooldown
        self.current_cooldown = 0

    # For shooting, I ensure that cooldown is down before I actually return a bullet projectile
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

# Simple revolver class
class Revolver(Gun):
    def __init__(self):
        super().__init__("Revolver", 120)

# Gun inventory
class Gun_Inventory:
    def __init__(self):
        self.gun_inventory = [Revolver()] # Owned Gun

        # Possible guns
        self.guns_list = {
            "Revolver": Revolver,
        }
    
    # Pickup feature (Currently useless)
    def pickup(self, gun_name):
        if gun_name in self.guns_list:
            self.gun_inventory.append(self.guns_list[gun_name]())
