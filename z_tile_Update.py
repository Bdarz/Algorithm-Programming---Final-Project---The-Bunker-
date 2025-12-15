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
    def __init__(self, position, dimensions, type):
        super().__init__()

        self.image = pygame.Surface(dimensions)

        self.type = type
        if type == "ascend":
            self.image.fill((255, 0, 0))
        elif type == "descend":
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect(topleft = position)

class Room(pygame.sprite.Sprite):
    def __init__(self, position, dimensions, door = "", rc = (0, 0), variation = "", distance = 0):
        super().__init__()

        self.position = position
        self.dimensions = dimensions
        if door == "":
            self.door = []
        else:
            self.door = door
        self.rc = rc
        self.variation = variation
        self.distance = distance

        self.type = "room"

        self.image = pygame.Surface(dimensions)
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft = position)

        self.tiles = [
            Wall(self.position, (self.dimensions[0], 30)),
            Wall(self.position, (30, self.dimensions[1])),
            Wall((self.position[0], self.position[1] + self.dimensions[1] - 29), (self.dimensions[0], 30)),
            Wall((self.position[0] + self.dimensions[0] - 29, self.position[1]), (30, self.dimensions[1]))
        ]

class Worldgen:
    def __init__(self, player, room_amount, hwidth, level):
        self.player = player
        self.room_amount = room_amount
        self.hwidth = hwidth
        self.level = level

        self.rg = [Room((self.player.spawnpoint[0] - self.hwidth[0] // 2, self.player.spawnpoint[1] - self.hwidth[1] // 2), self.hwidth, variation = "spawn")]
        self.entities = []
        self.rc = [[0, 0]]
        
        self.variations = ("empty", "four pillars", "center pillar")
    
    def variation(self, room):
        extra_tiles = []
        if room.variation != "spawn":
            variation = random.randint(0, 2)

            if variation == "boss":
                pass

            elif room.variation == "furthest": 
                extra_tiles = [ 
                    Stairs((room.position[0] + room.dimensions[0] // 2 - room.dimensions[0] // 8, room.position[1] + room.dimensions[1] // 2 - room.dimensions[1] // 8), (room.dimensions[0] // 4, room.dimensions[1] // 4), "ascend") 
                ]

            elif variation == 0:
                pass

            elif variation == 1:
                extra_tiles = [
                    Wall((room.position[0] + room.dimensions[0] // 4.8, room.position[1] + room.dimensions[1] // 4.8), (room.dimensions[0] // 8, room.dimensions[1] // 8)),
                    Wall((room.position[0] + room.dimensions[0] // 1.5, room.position[1] + room.dimensions[1] // 4.8), (room.dimensions[0] // 8, room.dimensions[1] // 8)),
                    Wall((room.position[0] + room.dimensions[0] // 4.8, room.position[1] + room.dimensions[1] // 1.5), (room.dimensions[0] // 8, room.dimensions[1] // 8)),
                    Wall((room.position[0] + room.dimensions[0] // 1.5, room.position[1] + room.dimensions[1] // 1.5), (room.dimensions[0] // 8, room.dimensions[1] // 8))
                ]
                self.entities.append(PlusShooter(self.player, pygame.math.Vector2(room.position[0] + room.dimensions[0] // 2, room.position[1] + room.dimensions[1] // 2)))

            elif variation == 2:
                extra_tiles = [
                    Wall((room.position[0] + room.dimensions[0] // 2 - room.dimensions[0] // 16, room.position[1] + room.dimensions[1] // 2 - room.dimensions[1] // 16), (room.dimensions[0] // 8, room.dimensions[1] // 8))
                ]

                enemy_position = [
                    pygame.math.Vector2(room.position[0] + room.dimensions[0] // 4, room.position[1] + room.dimensions[1] // 4),
                    pygame.math.Vector2(room.position[0] + room.dimensions[0] // 4, room.position[1] + room.dimensions[1] * 3 // 4),
                    pygame.math.Vector2(room.position[0] + room.dimensions[0] * 3 // 4, room.position[1] + room.dimensions[1] // 4),
                    pygame.math.Vector2(room.position[0] + room.dimensions[0] * 3 // 4, room.position[1] + room.dimensions[1] * 3 // 4)
                ]
                
                for i in range(2):
                    pos = random.randint(0, 2)
                    self.entities.append(SingleShooter(self.player, enemy_position[pos]))
                    enemy_position.pop(pos)
    
        else:
            extra_tiles = [ 
                Stairs((room.position[0] + room.dimensions[0] // 2 - room.dimensions[0] // 8, room.position[1] + room.dimensions[1] // 2 - room.dimensions[1] // 8), (room.dimensions[0] // 4, room.dimensions[1] // 4), "descent") 
            ] 
        
        for extra_tile in extra_tiles:
            room.tiles.append(extra_tile)
        
    def doorgen(self, room):
        if "north" in room.door:
            room.tiles[0] = Wall(room.position, (room.dimensions[0]//3, 30))
            room.tiles.append(Wall((room.position[0] + room.dimensions[0] * 2 // 3, room.position[1]), (room.dimensions[0]//3, 30)))
        if "west" in room.door:
            room.tiles[1] = Wall(room.position, (30, room.dimensions[1]//3))
            room.tiles.append(Wall((room.position[0], room.position[1] + room.dimensions[1] * 2 // 3), (30, room.dimensions[1]//3)))
        if "south" in room.door:
            room.tiles[2] = Wall((room.position[0], room.position[1] + room.dimensions[1] - 29), (room.dimensions[0]//3, 30))
            room.tiles.append(Wall((room.position[0] + room.dimensions[0] * 2 // 3, room.position[1] + room.dimensions[1] - 29), (room.dimensions[0]//3, 30)))
        if "east" in room.door:
            room.tiles[3] = Wall((room.position[0] + room.dimensions[0] - 29, room.position[1]), (30, room.dimensions[1] // 3))
            room.tiles.append(Wall((room.position[0] + room.dimensions[0] - 29, room.position[1] + room.dimensions[1] * 2 // 3), (30, room.dimensions[1] // 3)))
        
        self.variation(room)

    def neon_genesis(self):
        cardinals = ["north", "west", "south", "east"]
        i = 0
        while i < self.room_amount:
            current = random.randint(0, len(self.rg) - 1)
            cardinal = random.randint(0, 3)

            north_rc = [self.rg[current].rc[0], self.rg[current].rc[1] + 1]
            if cardinals[cardinal] == "north" and north_rc not in self.rc:
                self.rg.append(Room((self.rg[current].position[0], self.rg[current].position[1] - self.hwidth[1]), self.hwidth, ["south"], north_rc, self.rg[current].distance + 1))
                self.rc.append(north_rc)
                self.rg[current].door.append("north")
                i += 1

            west_rc = [self.rg[current].rc[0] - 1, self.rg[current].rc[1] ]
            if cardinals[cardinal] == "west" and west_rc not in self.rc:
                self.rg.append(Room((self.rg[current].position[0] - self.hwidth[0], self.rg[current].position[1]), self.hwidth, ["east"], west_rc, self.rg[current].distance + 1))
                self.rc.append(west_rc)
                self.rg[current].door.append("west")
                i += 1
            
            south_rc = [self.rg[current].rc[0], self.rg[current].rc[1] - 1]
            if cardinals[cardinal] == "south" and south_rc not in self.rc:
                self.rg.append(Room((self.rg[current].position[0], self.rg[current].position[1] + self.hwidth[1]), self.hwidth, ["north"], south_rc, self.rg[current].distance + 1))
                self.rc.append(south_rc)
                self.rg[current].door.append("south")
                i += 1

            east_rc = [self.rg[current].rc[0] + 1, self.rg[current].rc[1]]
            if cardinals[cardinal] == "east" and east_rc not in self.rc:
                self.rg.append(Room((self.rg[current].position[0] + self.hwidth[0], self.rg[current].position[1]), self.hwidth, ["west"], east_rc, self.rg[current].distance + 1))
                self.rc.append(east_rc)
                self.rg[current].door.append("east")
                i += 1

        furthest_room = self.rg[0]
        furthest_room_distance = self.rg[0].distance
        for room in self.rg:
            if room.distance > furthest_room_distance:
                furthest_room = room
                furthest_room_distance = room.distance
        furthest_room.variation = "furthest"
        
        for room in self.rg:
            self.doorgen(room)

        return self.rg, self.entities