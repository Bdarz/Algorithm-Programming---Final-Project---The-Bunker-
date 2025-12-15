import pygame
import sys

from tile import Worldgen, Room

class Level():
    def __init__(self, screen, player, room_amount = 10, worldgen = True):
        self.screen = screen
        self.player = player

        self.current_offset = pygame.math.Vector2(0, 0)

        if worldgen:
            self.tile_list = Worldgen(player, room_amount, (600, 600), self.level).neon_genesis()

        self.enemy_list = []
        self.sprites = {
            "floor": pygame.sprite.Group(),
            "wall": pygame.sprite.Group(),
            "stairup": pygame.sprite.Group(),
            "stairdown": pygame.sprite.Group(),
            "enemy": pygame.sprite.Group(),
            "enemyproj": pygame.sprite.Group(),
            "playerproj": pygame.sprite.Group()
        }

        for tile in self.tile_list:
            if tile.type == "room":
                for subtile in tile.tiles:
                    if subtile.type == "wall":
                        self.sprites["wall"].add(subtile)
                    elif subtile.type == "ascend":
                        self.sprites["stairup"].add(subtile)
                    elif subtile.type == "descend":
                        self.sprites["stairdown"].add(subtile)
                for enemy in tile.enemies:
                    self.enemy_list.append(enemy)
                self.sprites["floor"].add(tile)
        for enemy in self.enemy_list:
            self.sprites["enemy"].add(enemy)
        
        self.boss_killed = False

    def camera(self):
        self.current_offset[0] = int(self.player.position[0] - 640)
        self.current_offset[1] = int(self.player.position[1] - 360)

    def collision(self):
        player_descend = pygame.sprite.spritecollide(self.player, self.sprites["stairdown"], dokill = False)
        player_ascend = pygame.sprite.spritecollide(self.player, self.sprites["stairup"], dokill = False)

        if player_descend:
            if self.player.spawninvuln == False:
                self.player.position = self.player.lasvoss[self.level - 1]
                self.player.spawninvuln = True

                return self.level - 1
        elif player_ascend or self.boss_killed:
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

        player_wall = pygame.sprite.spritecollide(self.player, self.sprites["wall"], dokill = False)
        if player_wall:
            self.player.undo_movement()
            self.player.rect.center = self.player.position

        player_hit = pygame.sprite.spritecollide(self.player, self.sprites["enemyproj"], dokill = True)
        if player_hit:
            for p in player_hit:
                self.player.hitpoints -= 1

        enemy_hit = pygame.sprite.groupcollide(self.sprites["enemy"], self.sprites["playerproj"], dokilla = False, dokillb = True)
        if enemy_hit:
            for enemy, playerproj in enemy_hit.items():
                for p in playerproj:
                    enemy.hp -= 1
                    if enemy.hp <= 0:
                        enemy.kill()
        
        pygame.sprite.groupcollide(self.sprites["enemyproj"], self.sprites["wall"], dokilla = True, dokillb = False)
        pygame.sprite.groupcollide(self.sprites["playerproj"], self.sprites["wall"], dokilla = True, dokillb = False)

    def enemy_activity(self):
        for enemy in self.sprites["enemy"]:
            projectiles = enemy.update()
            for projectile in projectiles:
                if projectile != None:
                    self.sprites["enemyproj"].add(projectile)

    def run(self):
        self.player.update(self.current_offset)
        self.enemy_activity()
        returnal = self.collision()
        self.camera()

        self.sprites["enemyproj"].update()
        self.sprites["playerproj"].update()

        return returnal

class Level_0(Level):
    def __init__(self, screen, player):
        self.level = 0
        super().__init__(screen, player, 1, True)

class Level_1(Level):
    def __init__(self, screen, player):
        self.level = 1
        super().__init__(screen, player, 10, True)

class Level_2(Level):
    def __init__(self, screen, player):
        self.level = 2
        super().__init__(screen, player, 16, True)

class Boss_1(Level):
    def __init__(self, screen, player):
        self.level = 3
        self.base_room_hwidth = [800, 800]
        self.player = player
        self.tile_list = [
            Room(player, [player.spawnpoint[0] - self.base_room_hwidth[0] // 2, player.spawnpoint[1] - self.base_room_hwidth[1] // 2], [0, 0], self.base_room_hwidth, "blank", "boss", self.level)
        ]
        super().__init__(screen, player, 25, False)

        self.spawn_offset = False

    def run(self):
        self.player.update(self.current_offset)
        self.enemy_activity()

        if self.spawn_offset == False:
            self.spawn_offset = True
            self.player.position[1] += 200

        if len(self.sprites["enemy"]) == 0:
            self.boss_killed = True

        returnal = self.collision()
        self.camera()

        self.sprites["enemyproj"].update()
        self.sprites["playerproj"].update()
        
        return returnal