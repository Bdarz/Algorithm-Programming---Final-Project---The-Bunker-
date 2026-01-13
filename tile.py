# Pygame for surfaces and rect, random for procedural generation
import pygame
import random

# Importing enemy for entity generation
from enemy import SingleShooter, PlusShooter, BossShooter1

# Base wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, position, dimensions):
        super().__init__()

        # Identifier
        self.type = "wall"

        # Properties such as texture and position
        self.image = pygame.Surface(dimensions)
        self.image.fill((40, 40, 40))
        self.rect = self.image.get_rect(topleft = position)

# Stair object as the only method for players to travel between levels
class Stairs(pygame.sprite.Sprite):
    def __init__(self, position, dimensions = [30, 30], type = ""):
        super().__init__()

        self.type = type

        # Properties such as texture and position
        self.image = pygame.Surface(dimensions)

        if type == "ascend":
            self.image.fill((255, 0, 0))
        elif type == "descend":
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect(topleft = position)

class Room(pygame.sprite.Sprite):
    def __init__(self, player, position, relative_position, dimensions, door = "blank", variation = "blank", level = ""):
        super().__init__()

        # Room is room
        self.type = "room"

        # Floor texture
        self.image = pygame.Surface(dimensions)
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft = position)

        # Inherits player object for enemies to track
        self.player = player

        # Current position and position relative to other rooms, a.k.a the custom coordinates
        self.position = position
        self.relative_position = relative_position

        # Room size
        self.dimensions = dimensions

        # Creates a list of doors
        if door == "blank":
            self.door = []
        else:
            self.door = door

        # Stores current variation and elvel it is on
        self.variation = variation
        self.level = level

        # Stores distance of self from other rooms, obtained from the coords of parent room
        self.distance = abs(relative_position[0]) + abs(relative_position[1])

        # Base thickness of walls
        self.base_wall_thickness = 30

        # Generates 4 walls to each side
        self.tiles = [
            Wall(self.position, (self.dimensions[0], self.base_wall_thickness)),
            Wall(self.position, (self.base_wall_thickness, self.dimensions[1])),
            Wall((self.position[0], self.position[1] + self.dimensions[1] - self.base_wall_thickness + 1), (self.dimensions[0], self.base_wall_thickness)),
            Wall((self.position[0] + self.dimensions[0] - self.base_wall_thickness + 1, self.position[1]), (self.base_wall_thickness, self.dimensions[1]))
        ]

        # Creates a list of possible enemies
        self.enemies = []

        # Calls for variation if the room is created with a variation automatically in mind
        self.room_variation()
    
    def room_variation(self):
        # Creates a list of possible extra enemies/walls
        extra_tiles = []
        enemies = []

        # Spawn room, which has a stair, unless its level 1, which has no stairs to level 0
        if self.variation == "spawn" and self.level != 1:
            extra_tiles = [
                Stairs((self.position[0] + self.dimensions[0] // 2 - self.dimensions[0] // 8, self.position[1] + self.dimensions[1] // 2 - self.dimensions[1] // 8), (self.dimensions[0] // 4, self.dimensions[1] // 4), "descend")
            ]

        # Furthest room, which has a stair to the next level
        if self.variation == "furthest":
            extra_tiles = [
                Stairs((self.position[0] + self.dimensions[0] // 2 - self.dimensions[0] // 8, self.position[1] + self.dimensions[1] // 2 - self.dimensions[1] // 8), (self.dimensions[0] // 4, self.dimensions[1] // 4), "ascend")
            ]

        # Room has four pillars at pre-determined, fine-tuned spots, with hard-coded numbers because it is not meant to be modified
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
        
        # Same as top variation in logic, just different walls and enemies
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

        # A special boss room, which grants the room's dimensions to the boss for movement
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

        # Inputs all extra tiles into the list of tiles/walls in a room
        for extra_tile in extra_tiles:
            self.tiles.append(extra_tile)

        # Same as above but for enemies
        for enemy in enemies:
            self.enemies.append(enemy)

# Procedural Generation code
class Worldgen:
    def __init__(self, player, room_amount, base_room_hwidth, level):
        # First, inherit player object for enemy generation later
        self.player = player

        # Determine how many rooms and their dimensions
        self.room_amount = room_amount
        self.base_room_hwidth = base_room_hwidth

        # Keep track of which level it is
        self.level = level

        # Create a list for all rooms, and create a base spawn room
        self.all_rooms = [Room(self.player, [self.player.spawnpoint[0] - self.base_room_hwidth[0] // 2, self.player.spawnpoint[1] - self.base_room_hwidth[1] // 2], [0, 0], self.base_room_hwidth, "blank", "spawn", level)]
        
        # Create a custom coordinate system and store the coordinates of existing rooms here 
        self.relative_coords = [[0, 0]]

        # To later find the furthest room geometrically, which is what the stairoom will be
        self.furthest = self.all_rooms[0]
        self.furthest_distance = 0

        # Wall thickness
        self.wall_thickness = 30

    # Step 2
    def doorgen(self, room):
        # Basically, when it wants a door in a certain direction, it deletes that wall and creates two walls
        # It leaves a gap of 1/3rd as the size of the door, this is what the game uses as its door size
        if "north" in room.door:
            room.tiles[0] = Wall(room.position, (room.dimensions[0]//3, self.wall_thickness))
            room.tiles.append(Wall((room.position[0] + room.dimensions[0] * 2 // 3, room.position[1]), (room.dimensions[0]//3, self.wall_thickness)))
        if "west" in room.door:
            room.tiles[1] = Wall(room.position, (self.wall_thickness, room.dimensions[1]//3))
            room.tiles.append(Wall((room.position[0], room.position[1] + room.dimensions[1] * 2 // 3), (self.wall_thickness, room.dimensions[1]//3)))
        if "south" in room.door:
            room.tiles[2] = Wall((room.position[0], room.position[1] + room.dimensions[1] - self.wall_thickness + 1), (room.dimensions[0]//3, 30))
            room.tiles.append(Wall((room.position[0] + room.dimensions[0] * 2 // 3, room.position[1] + room.dimensions[1] - self.wall_thickness +  1), (room.dimensions[0]//3, self.wall_thickness + 1)))
        if "east" in room.door:
            room.tiles[3] = Wall((room.position[0] + room.dimensions[0] - self.wall_thickness + 1, room.position[1]), (self.wall_thickness, room.dimensions[1] // 3))
            room.tiles.append(Wall((room.position[0] + room.dimensions[0] - self.wall_thickness + 1, room.position[1] + room.dimensions[1] * 2 // 3), (self.wall_thickness, room.dimensions[1] // 3)))

    # Step 1
    def neon_genesis(self):
        # Create a list containing all possible directions a room can be in
        cardinals = ["north", "west", "south", "east"]

        # Keep track of how many rooms have been generated
        i = 0

        # Generate rooms based on how many rooms is desired
        while i < self.room_amount:
            # Chooses a random room from the list of existing rooms to use as the room from which a new room will be generated
            # Call it the parent room
            current = random.randint(0, len(self.all_rooms) - 1)

            # Chooses a random direction 
            cardinal = random.randint(0, 3)

            # Creates the coordinates for a room north of the current room
            north_rc = [self.all_rooms[current].relative_position[0], self.all_rooms[current].relative_position[1] + 1]

            # Confirms direction and checks if there is a pre-existing room in this direction
            if cardinals[cardinal] == "north" and north_rc not in self.relative_coords:
                # Creates a door to chosen direction in the current room
                self.all_rooms[current].door.append(cardinals[cardinal])

                # Adds coordinates of new room to the list of coordinates
                self.relative_coords.append(north_rc)
                
                # Adds a new room with a door on the direction opposite of chosen direction, to connect current and new room
                self.all_rooms.append(Room(self.player, (self.all_rooms[current].position[0], self.all_rooms[current].position[1] - self.base_room_hwidth[1]), north_rc, self.base_room_hwidth, door = ["south"]))
                
                # Notifies that a new room has been generated
                i += 1
            
            # These all follow the same pattern, just different directions
            west_rc = [self.all_rooms[current].relative_position[0] - 1, self.all_rooms[current].relative_position[1]]
            if cardinals[cardinal] == "west" and west_rc not in self.relative_coords:
                self.all_rooms[current].door.append(cardinals[cardinal])
                self.relative_coords.append(west_rc)
                self.all_rooms.append(Room(self.player, (self.all_rooms[current].position[0] - self.base_room_hwidth[0], self.all_rooms[current].position[1]), west_rc, self.base_room_hwidth, door = ["east"]))
                i += 1

            south_rc = [self.all_rooms[current].relative_position[0], self.all_rooms[current].relative_position[1] -1]
            if cardinals[cardinal] == "south" and south_rc not in self.relative_coords:
                self.all_rooms[current].door.append(cardinals[cardinal])
                self.relative_coords.append(south_rc)
                self.all_rooms.append(Room(self.player, (self.all_rooms[current].position[0], self.all_rooms[current].position[1] + self.base_room_hwidth[1]), south_rc, self.base_room_hwidth, door = ["north"]))
                i += 1

            east_rc = [self.all_rooms[current].relative_position[0] + 1, self.all_rooms[current].relative_position[1]]
            if cardinals[cardinal] == "east" and east_rc not in self.relative_coords:
                self.all_rooms[current].door.append(cardinals[cardinal])
                self.relative_coords.append(east_rc)
                self.all_rooms.append(Room(self.player, (self.all_rooms[current].position[0] + self.base_room_hwidth[0], self.all_rooms[current].position[1]), east_rc, self.base_room_hwidth, door = ["west"]))
                i += 1
            
        # Finds the furthest room
        for i in self.all_rooms:
            if i.distance > self.furthest_distance:
                self.furthest = i
                self.furthest_distance = i.distance

        # Generate doors and variations for all rooms
        for i in self.all_rooms:
            # Generates door
            self.doorgen(i)

            # Checks if room is furthest to see if it should turn it into a stairoom
            if i == self.furthest:
                i.variation = "furthest"
                i.room_variation()
            
            # Ensures it is not the original room, since that is meant to be empty
            elif i.relative_position != [0, 0]:
                # Designate a random variation out of two variations
                i.variation = random.randint(0, 2)

                # Generate variation
                i.room_variation()

        # Returns a list containing all room objects, which are lists containing wall objects and enemies
        return self.all_rooms