import pygame
import sys

from enemy import *
from projectile import *
from tile import *

class Level():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.current_offset = pygame.math.Vector2(0, 0)

    def camera(self):
        self.current_offset[0] = self.player.position[0] - 640
        self.current_offset[1] = self.player.position[1] - 360
    
    def draw_sprite(self):
        self.screen.fill((0, 0, 0))
        
        for i in self.floor_sprite:
            resulting_offset = i.rect.topleft - self.current_offset
            self.screen.blit(i.image, resulting_offset)

        for i in self.stairup_sprite:
            resulting_offset = i.rect.topleft - self.current_offset
            self.screen.blit(i.image, resulting_offset)

        for i in self.stairdown_sprite:
            resulting_offset = i.rect.topleft - self.current_offset
            self.screen.blit(i.image, resulting_offset)

        for i in self.wall_sprite:
            resulting_offset = i.rect.topleft - self.current_offset
            self.screen.blit(i.image, resulting_offset)

        for i in self.enemy_sprite:
            resulting_offset = i.rect.topleft - self.current_offset
            self.screen.blit(i.image, resulting_offset)

        for i in self.enemy_projectile_sprite:
            resulting_offset = i.rect.topleft - self.current_offset
            self.screen.blit(i.image, resulting_offset)

        for i in self.player_projectile_sprite:
            resulting_offset = i.rect.topleft - self.current_offset
            self.screen.blit(i.image, resulting_offset)

        ensures_that_i_draw_this_at_topleft_not_center_of_position = pygame.math.Vector2(self.player.rectwo.width//2, self.player.rectwo.height//2)
        resulting_offset = self.player.position - ensures_that_i_draw_this_at_topleft_not_center_of_position - self.current_offset
        self.screen.blit(self.player.image, resulting_offset)

        health_bar = self.player.healthbar()
        heart_position = pygame.math.Vector2(10, 10)
        if health_bar:
            for i in health_bar:
                self.screen.blit(i, heart_position)
                heart_position[0] += 50
    
    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if len(self.player.guns.gun_inventory) > 1:
                        self.player.equipped_slot = 1
                
                if event.key == pygame.K_2:
                    if len(self.player.guns.gun_inventory) > 2:
                        self.player.equipped_slot = 2

                if event.key == pygame.K_n:
                    bullet = self.player.guns.gun_inventory[self.player.equipped_slot].shoot(self.player.position, self.player.angle)
                    if bullet:
                        self.player_projectile_sprite.add(bullet)
            
            heldkey = pygame.key.get_pressed()
            if heldkey[pygame.K_n]:
                bullet = self.player.guns.gun_inventory[self.player.equipped_slot].shoot(self.player.position, self.player.angle)
                if bullet:
                    self.player_projectile_sprite.add(bullet)

    def collision(self):
        player_descend = pygame.sprite.spritecollide(self.player, self.stairdown_sprite, dokill = False)
        player_ascend = pygame.sprite.spritecollide(self.player, self.stairup_sprite, dokill = False)

        if player_descend:
            if self.player.spawninvuln == False:
                self.player.position = self.player.lasvoss[self.level - 1]
                self.player.spawninvuln = True

                return self.level - 1
        elif player_ascend:
            if self.player.spawninvuln == False:
                if len(self.player.lasvoss) < self.level + 1: 
                    self.player.lasvoss.append(self.player.position)
                else:
                    self.player.lasvoss[self.level] = self.player.position
                self.player.position = self.player.spawnpoint
                self.player.spawninvuln = True

                return self.level + 1
        else:
            self.player.spawninvuln = False

        player_wall = pygame.sprite.spritecollide(self.player, self.wall_sprite, dokill = False)
        if player_wall:
            self.player.undo_movement()
            self.player.rect.center = self.player.position

        player_hit = pygame.sprite.spritecollide(self.player, self.enemy_projectile_sprite, dokill = True)
        if player_hit:
            for p in player_hit:
                self.player.hitpoints -= 1

        enemy_hit = pygame.sprite.groupcollide(self.enemy_sprite, self.player_projectile_sprite, dokilla = False, dokillb = True)
        if enemy_hit:
            for e, pp in enemy_hit.items():
                for p in pp:
                    e.hp -= 1
                    if e.hp <= 0:
                        e.kill()
        
        pygame.sprite.groupcollide(self.enemy_projectile_sprite, self.wall_sprite, dokilla = True, dokillb = False)
        pygame.sprite.groupcollide(self.player_projectile_sprite, self.wall_sprite, dokilla = True, dokillb = False)

    def enemy_activity(self):
        for e in self.enemy_sprite:
            projectiles = e.update()
            for p in projectiles:
                if p != None:
                    self.enemy_projectile_sprite.add(p)

    def run(self):
        self.player.update(self.current_offset)
        self.control()
        self.enemy_activity()
        returnal = self.collision()
        self.camera()

        self.enemy_projectile_sprite.update()
        self.player_projectile_sprite.update()

        self.draw_sprite()
        
        return returnal

class Level_1(Level):
    def __init__(self, screen, player):
        self.level = 1
        super().__init__(screen, player)

        self.tile_list = Worldgen(player, 13, (200, 200), 1).neon_genesis()
        self.enemy_list = []
        self.wall_sprite = pygame.sprite.Group()
        self.floor_sprite = pygame.sprite.Group()
        self.stairup_sprite = pygame.sprite.Group()
        self.stairdown_sprite = pygame.sprite.Group()

        for tile in self.tile_list:
            if tile.type == "room":
                tiles = tile.tiles
                for subtile in tiles:
                    if subtile.type == "wall":
                        self.wall_sprite.add(subtile)
                    elif subtile.type == "ascend":
                        self.stairup_sprite.add(subtile)
                    elif subtile.type == "descend":
                        self.stairdown_sprite.add(subtile)
                for enemy in tile.enemies:
                    self.enemy_list.append(enemy)
                self.floor_sprite.add(tile)

        self.enemy_sprite = pygame.sprite.Group()
        for enemy in self.enemy_list:
            self.enemy_sprite.add(enemy)

        self.enemy_projectile_sprite = pygame.sprite.Group()
        self.player_projectile_sprite = pygame.sprite.Group()

class Level_2(Level):
    def __init__(self, screen, player):
        self.level = 2
        super().__init__(screen, player)

        self.tile_list = Worldgen(player, 13, (200, 200), 2).neon_genesis()
        self.enemy_list = []
        self.wall_sprite = pygame.sprite.Group()
        self.floor_sprite = pygame.sprite.Group()
        self.stairup_sprite = pygame.sprite.Group()
        self.stairdown_sprite = pygame.sprite.Group()

        for tile in self.tile_list:
            if tile.type == "room":
                tiles = tile.tiles
                for subtile in tiles:
                    if subtile.type == "wall":
                        self.wall_sprite.add(subtile)
                    elif subtile.type == "ascend":
                        self.stairup_sprite.add(subtile)
                    elif subtile.type == "descend":
                        self.stairdown_sprite.add(subtile)
                for enemy in tile.enemies:
                    self.enemy_list.append(enemy)
                self.floor_sprite.add(tile)

        self.enemy_sprite = pygame.sprite.Group()
        for enemy in self.enemy_list:
            self.enemy_sprite.add(enemy)

        self.enemy_projectile_sprite = pygame.sprite.Group()
        self.player_projectile_sprite = pygame.sprite.Group()
