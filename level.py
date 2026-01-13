import pygame

from tile import Worldgen, Room

class Level():
    def __init__(self, screen, player, room_amount = 10, worldgen = True):
        # Inherits screen and player
        self.screen = screen
        self.player = player

        # Offset for drawing
        self.current_offset = pygame.math.Vector2(0, 0)

        # Creates map/level unless stated otherwise
        if worldgen:
            self.tile_list = Worldgen(player, room_amount, (600, 600), self.level).neon_genesis()

        # A dictionary for all the sprite groups
        self.sprites = {
            "floor": pygame.sprite.Group(),
            "wall": pygame.sprite.Group(),
            "stairup": pygame.sprite.Group(),
            "stairdown": pygame.sprite.Group(),
            "enemy": pygame.sprite.Group(),
            "enemyproj": pygame.sprite.Group(),
            "playerproj": pygame.sprite.Group()
        }

        # A list to store all enemies
        self.enemy_list = []

        # Basically inputs all things map related into their respective sprite groups
        for tile in self.tile_list:
            # Ensures that it is a room
            if tile.type == "room":
                # Every room has a list of tiles, either walls, or stairs
                for subtile in tile.tiles:
                    if subtile.type == "wall":
                        self.sprites["wall"].add(subtile)
                    elif subtile.type == "ascend":
                        self.sprites["stairup"].add(subtile)
                    elif subtile.type == "descend":
                        self.sprites["stairdown"].add(subtile)
                
                # Adds enemies to sprite group as well
                for enemy in tile.enemies:
                    self.sprites["enemy"].add(enemy)

                # Floor texture
                self.sprites["floor"].add(tile)
        
        # This is specifically for the boss level, to check if boss is dead or not
        self.boss_killed = False

    def camera(self):
        # Camera offset, basically to draw everything relative to player position to create tracking camera feel
        self.current_offset[0] = int(self.player.position[0] - 640)
        self.current_offset[1] = int(self.player.position[1] - 360)

    def collision(self):
        # Checks if player is on a stair or not
        player_descend = pygame.sprite.spritecollide(self.player, self.sprites["stairdown"], dokill = False)
        player_ascend = pygame.sprite.spritecollide(self.player, self.sprites["stairup"], dokill = False)

        # For descending, it has some spawn invuln to prevent constant rubber banding between levels
        if player_descend:
            if self.player.spawninvuln == False:
                # Returns player to last position on last level
                self.player.position = self.player.last_position[self.level - 1]
                self.player.spawninvuln = True

                return self.level - 1
        
        # Same as above
        elif player_ascend or self.boss_killed:
            if self.player.spawninvuln == False:

                # Ensures that player does not exceed level count
                if len(self.player.last_position) < self.level + 1: 
                    self.player.last_position.append(self.player.position)
                else:
                    self.player.last_position[self.level] = self.player.position

                self.player.position = self.player.spawnpoint
                self.player.spawninvuln = True

                return self.level + 1
        else:
            self.player.spawninvuln = False

        # Wall collision, which undoes movement
        player_wall = pygame.sprite.spritecollide(self.player, self.sprites["wall"], dokill = False)
        if player_wall:
            self.player.undo_movement()
            self.player.rect.center = self.player.position

        # For when player is hit by projectiles, takes damage based on how many projectiles hit
        player_hit = pygame.sprite.spritecollide(self.player, self.sprites["enemyproj"], dokill = True)
        if player_hit:
            for p in player_hit:
                self.player.hitpoints -= 1

        # For when player hits an enemy with a projectile, same logic, just for different parties
        enemy_hit = pygame.sprite.groupcollide(self.sprites["enemy"], self.sprites["playerproj"], dokilla = False, dokillb = True)
        if enemy_hit:
            for enemy, playerproj in enemy_hit.items():
                for p in playerproj:
                    enemy.health()
        
        # Projectiles gets deleted when it collides with a wall
        pygame.sprite.groupcollide(self.sprites["enemyproj"], self.sprites["wall"], dokilla = True, dokillb = False)
        pygame.sprite.groupcollide(self.sprites["playerproj"], self.sprites["wall"], dokilla = True, dokillb = False)

    def enemy_activity(self):
        # Constantly keep the enemies attacking if in range
        for enemy in self.sprites["enemy"]:
            projectiles = enemy.update()
            for projectile in projectiles:
                if projectile != None:
                    # Adds whatever projectiles is returned by the update(attack) behavior into the sprite group
                    self.sprites["enemyproj"].add(projectile)

    def run(self):
        # Passes offset to keep a track of mouse location according to offset
        self.player.update(self.current_offset)

        # Basic calls per frame
        self.enemy_activity()
        returnal = self.collision()
        self.camera()

        # Updates projectile movement per frame
        self.sprites["enemyproj"].update()
        self.sprites["playerproj"].update()

        # Returnal is the value returned by stair collision, a.k.a what level to send to
        return returnal

# Level classes, this allows them to contain special properties, like for boss
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

# Custom boss level, no worldgen here, instead a handcrafted one
class Boss_1(Level):
    def __init__(self, screen, player):
        self.level = 3
        self.base_room_hwidth = [800, 800]
        self.player = player

        # Specialized boss room
        self.tile_list = [
            Room(player, [player.spawnpoint[0] - self.base_room_hwidth[0] // 2, player.spawnpoint[1] - self.base_room_hwidth[1] // 2], [0, 0], self.base_room_hwidth, "blank", "boss", self.level)
        ]

        # Doesn't call worldgen
        super().__init__(screen, player, 25, False)

        self.spawn_offset = False

    def run(self):
        self.player.update(self.current_offset)
        self.enemy_activity()

        # Just to place the player a bit far away from the boss
        if self.spawn_offset == False:
            self.spawn_offset = True
            self.player.position[1] += 200

        # Kill everything to win
        if len(self.sprites["enemy"]) == 0:
            self.boss_killed = True

        returnal = self.collision()
        self.camera()

        self.sprites["enemyproj"].update()
        self.sprites["playerproj"].update()
        
        return returnal