import pygame
import math
import random

from enemy import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, position, dimensions):
        super().__init__()

        self.type = "wall"

        self.image = pygame.Surface(dimensions)
        self.image.fill((40, 40, 40))
        self.rect = self.image.get_rect(topleft = position)

class Stairs(pygame.sprite.Sprite):
    def __init__(self, position, dimensions = [30, 30], type = ""):
        super().__init__()

        self.image = pygame.Surface(dimensions)

        self.type = type
        if type == "ascend":
            self.image.fill((255, 0, 0))
        elif type == "descend":
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect(topleft = position)

class Room(pygame.sprite.Sprite):
    def __init__(self, player, position, relative_position, dimensions, door = "blank", variation = "blank", level = ""):
        super().__init__()

        self.type = "room"

        self.image = pygame.Surface(dimensions)
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft = position)

        self.player = player
        self.position = position
        self.relative_position = relative_position
        self.dimensions = dimensions
        if door == "blank":
            self.door = []
        else:
            self.door = door
        self.variation = variation
        self.level = level

        self.distance = abs(relative_position[0]) + abs(relative_position[1])

        self.tiles = [
            Wall(self.position, (self.dimensions[0], 30)),
            Wall(self.position, (30, self.dimensions[1])),
            Wall((self.position[0], self.position[1] + self.dimensions[1] - 29), (self.dimensions[0], 30)),
            Wall((self.position[0] + self.dimensions[0] - 29, self.position[1]), (30, self.dimensions[1]))
        ]
        self.enemies = []

        self.room_variation()

    def doorgen(self):
        if self.variation == "hallway":
            redux, count, cardinals = 0, 0, ["north", "west", "south", "east"]
            for i in cardinals:
                if i in self.door:
                    self.tiles.pop(count - redux)
                    redux += 1
                count +=1
        else:
            if "north" in self.door:
                self.tiles[0] = Wall(self.position, (self.dimensions[0]//3, 30))
                self.tiles.append(Wall((self.position[0] + self.dimensions[0] * 2 // 3, self.position[1]), (self.dimensions[0]//3, 30)))
            if "west" in self.door:
                self.tiles[1] = Wall(self.position, (30, self.dimensions[1]//3))
                self.tiles.append(Wall((self.position[0], self.position[1] + self.dimensions[1] * 2 // 3), (30, self.dimensions[1]//3)))
            if "south" in self.door:
                self.tiles[2] = Wall((self.position[0], self.position[1] + self.dimensions[1] - 29), (self.dimensions[0]//3, 30))
                self.tiles.append(Wall((self.position[0] + self.dimensions[0] * 2 // 3, self.position[1] + self.dimensions[1] - 29), (self.dimensions[0]//3, 30)))
            if "east" in self.door:
                self.tiles[3] = Wall((self.position[0] + self.dimensions[0] - 29, self.position[1]), (30, self.dimensions[1] // 3))
                self.tiles.append(Wall((self.position[0] + self.dimensions[0] - 29, self.position[1] + self.dimensions[1] * 2 // 3), (30, self.dimensions[1] // 3)))
    
    def room_variation(self):
        extra_tiles = []
        enemies = []

        if self.variation == "spawn" and self.level != 1:
            extra_tiles = [
                Stairs((self.position[0] + self.dimensions[0] // 2 - self.dimensions[0] // 8, self.position[1] + self.dimensions[1] // 2 - self.dimensions[1] // 8), (self.dimensions[0] // 4, self.dimensions[1] // 4), "descend")
            ]

        if self.variation == "furthest":
            extra_tiles = [
                Stairs((self.position[0] + self.dimensions[0] // 2 - self.dimensions[0] // 8, self.position[1] + self.dimensions[1] // 2 - self.dimensions[1] // 8), (self.dimensions[0] // 4, self.dimensions[1] // 4), "ascend")
            ]

        if self.variation == "four pillars" or self.variation == 1:
            extra_tiles = [
                Wall((self.position[0] + self.dimensions[0] // 4.8, self.position[1] + self.dimensions[1] // 4.8), (self.dimensions[0] // 8, self.dimensions[1] // 8)),
                Wall((self.position[0] + self.dimensions[0] // 1.5, self.position[1] + self.dimensions[1] // 4.8), (self.dimensions[0] // 8, self.dimensions[1] // 8)),
                Wall((self.position[0] + self.dimensions[0] // 4.8, self.position[1] + self.dimensions[1] // 1.5), (self.dimensions[0] // 8, self.dimensions[1] // 8)),
                Wall((self.position[0] + self.dimensions[0] // 1.5, self.position[1] + self.dimensions[1] // 1.5), (self.dimensions[0] // 8, self.dimensions[1] // 8))
            ]

            enemies = [
                PlusShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] // 2, self.position[1] + self.dimensions[1] // 2))
            ]

            extra_enemies = [
                PlusShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] // 4, self.position[1] + self.dimensions[1] // 4)),
                PlusShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] // 4, self.position[1] + self.dimensions[1] * 3 // 4)),
                PlusShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] * 3 // 4, self.position[1] + self.dimensions[1] // 4)),
                PlusShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] * 3 // 4, self.position[1] + self.dimensions[1] * 3 // 4))
            ]
        
        if self.variation == "central pillar" or self.variation == 2:
            extra_tiles = [
                Wall((self.position[0] + self.dimensions[0] // 2 - self.dimensions[0] // 16, self.position[1] + self.dimensions[1] // 2 - self.dimensions[1] // 16), (self.dimensions[0] // 8, self.dimensions[1] // 8))
            ]

            extra_enemies = [
                SingleShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] // 4, self.position[1] + self.dimensions[1] // 4)),
                SingleShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] // 4, self.position[1] + self.dimensions[1] * 3 // 4)),
                SingleShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] * 3 // 4, self.position[1] + self.dimensions[1] // 4)),
                SingleShooter(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] * 3 // 4, self.position[1] + self.dimensions[1] * 3 // 4))
            ]
            max = 3
            for i in range(2):
                rand = random.randint(0, max)
                enemies.append(extra_enemies[rand])
                extra_enemies.pop(rand)
                max -= 1

        if self.variation == "boss":
            extra_tiles = [
                Wall((self.position[0] + self.dimensions[0] // 4.8, self.position[1] + self.dimensions[1] // 4.8), (self.dimensions[0] // 8, self.dimensions[1] // 8)),
                Wall((self.position[0] + self.dimensions[0] // 1.5, self.position[1] + self.dimensions[1] // 4.8), (self.dimensions[0] // 8, self.dimensions[1] // 8)),
                Wall((self.position[0] + self.dimensions[0] // 4.8, self.position[1] + self.dimensions[1] // 1.5), (self.dimensions[0] // 8, self.dimensions[1] // 8)),
                Wall((self.position[0] + self.dimensions[0] // 1.5, self.position[1] + self.dimensions[1] // 1.5), (self.dimensions[0] // 8, self.dimensions[1] // 8))
            ]

            enemies = [
                BossShooter1(self.player, pygame.math.Vector2(self.position[0] + self.dimensions[0] // 2, self.position[1] + self.dimensions[1] // 2))
            ]

            enemies[0].room_position = self.position
            enemies[0].room_dimensions = self.dimensions

        for extra_tile in extra_tiles:
            self.tiles.append(extra_tile)
        for enemy in enemies:
            self.enemies.append(enemy)
        
class Worldgen:
    def __init__(self, player, room_amount, base_room_hwidth, level):
        self.player = player
        self.room_amount = room_amount
        self.base_room_hwidth = base_room_hwidth
        self.level = level

        self.rg = [Room(self.player, [self.player.spawnpoint[0] - self.base_room_hwidth[0] // 2, self.player.spawnpoint[1] - self.base_room_hwidth[1] // 2], [0, 0], self.base_room_hwidth, "blank", "spawn", level)]
        self.rc = [[0, 0]]

        self.furthest = self.rg[0]
        self.furthest_distance = 0
            
    def neon_genesis(self):
        cardinals = ["north", "west", "south", "east"]
        i = 0
        while i < self.room_amount:
            current = random.randint(0, len(self.rg) - 1)
            cardinal = random.randint(0, 3)

            north_rc = [self.rg[current].relative_position[0], self.rg[current].relative_position[1] + 1]
            if cardinals[cardinal] == "north" and north_rc not in self.rc:
                self.rg[current].door.append(cardinals[cardinal])
                self.rc.append(north_rc)
                self.rg.append(Room(self.player, (self.rg[current].position[0], self.rg[current].position[1] - self.base_room_hwidth[1]), north_rc, self.base_room_hwidth, door = ["south"]))
                i += 1
            
            west_rc = [self.rg[current].relative_position[0] - 1, self.rg[current].relative_position[1]]
            if cardinals[cardinal] == "west" and west_rc not in self.rc:
                self.rg[current].door.append(cardinals[cardinal])
                self.rc.append(west_rc)
                self.rg.append(Room(self.player, (self.rg[current].position[0] - self.base_room_hwidth[0], self.rg[current].position[1]), west_rc, self.base_room_hwidth, door = ["east"]))
                i += 1

            south_rc = [self.rg[current].relative_position[0], self.rg[current].relative_position[1] -1]
            if cardinals[cardinal] == "south" and south_rc not in self.rc:
                self.rg[current].door.append(cardinals[cardinal])
                self.rc.append(south_rc)
                self.rg.append(Room(self.player, (self.rg[current].position[0], self.rg[current].position[1] + self.base_room_hwidth[1]), south_rc, self.base_room_hwidth, door = ["north"]))
                i += 1

            east_rc = [self.rg[current].relative_position[0] + 1, self.rg[current].relative_position[1]]
            if cardinals[cardinal] == "east" and east_rc not in self.rc:
                self.rg[current].door.append(cardinals[cardinal])
                self.rc.append(east_rc)
                self.rg.append(Room(self.player, (self.rg[current].position[0] + self.base_room_hwidth[0], self.rg[current].position[1]), east_rc, self.base_room_hwidth, door = ["west"]))
                i += 1
            
        for i in self.rg:
            if i.distance > self.furthest_distance:
                self.furthest = i
                self.furthest_distance = i.distance

        for i in self.rg:
            i.doorgen()

            if i == self.furthest:
                i.variation = "furthest"
                i.room_variation()
            elif i.relative_position == [0, 0]:
                pass
            else:
                i.variation = random.randint(0, 2)
                i.room_variation()

        return self.rg