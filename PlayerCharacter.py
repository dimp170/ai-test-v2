import math
import os
import pygame
import random
import statistics as st
from pygame.locals import *

# Colors
BLACK, WHITE, RED, GREEN, BLUE, ORANGE, PURPLE, GRAY = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 100, 100), (255, 0, 255), (100, 100, 100)

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# Character sprite sets
SPRITES = {
    "idle": ["PL1"],
    "left": ["PL0", "PL1", "PL3", "PL4", "PL3", "PL1", "PL0"],
    "right": ["PR0", "PR1", "PR3", "PR4", "PR3", "PR1", "PR0"],
    "idle_side": ["PIL", "PIR"],
    "slide": ["PLSL", "PLSR"],
    "falling": ["PFALL", "PFALR", "PFALL2", "PFALR2", "PFALL3", "PFALR3", "PFALL4", "PFALR4"],
    "push": ["PSHL", "PSH"],
    "head": ["Head1"]
}

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Movement & Physics
        self.change_x, self.change_y = 0, 0
        self.speedCap, self.speedGain = 15, 0.25
        self.fallCap = 40
        self.jumps, self.bounces, self.fails = 0, 0, 0
        self.timer, self.totalseconds = 0, 0
        self.pushing, self.Direction = 0, 1
        self.state, self.frame = "Idle", 0

        # Debug and Game Settings
        self.debug, self.noSprites, self.noJumpCap = 0, 0, 0
        self.freeFly, self.speedMultiplier = 0, 1
        self.noClip, self.noPhysicsBlocks, self.noParticles, self.noText = 0, 0, 0, 0
        self.toSpawn, self.randomlyWarp = 0, 0

        # Graphics & Sprites
        self.image = pygame.image.load(os.path.join('images', "PIR.gif")).convert()
        self.rect = self.image.get_rect()
        self.justSet = 0

        # Level & Text
        self.level, self.message, self.text = None, "", "OFF"

    def update(self):
        """ Update player movement and handle physics. """
        self.apply_gravity()
        self.check_spawn()
        self.handle_warp()
        self.handle_movement()
        self.handle_collisions()
        self.update_sprite()

    def apply_gravity(self):
        """ Apply gravity effect. """
        if self.freeFly == 1:
            return
        
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1.1
            for block in self.level.platform_list:
                if self.rect.x in range(block.rect.left, block.rect.right) and block.rect.top - self.rect.bottom in range(0, 12):
                    self.change_y, self.rect.bottom = 0, block.rect.top

    def check_spawn(self):
        """ Check if player should respawn at spawn block. """
        if self.toSpawn == 1:
            for block in self.level.platform_list:
                if block.type.lower() == "spawn":
                    self.rect.x, self.rect.y = block.rect.x, block.rect.y - 128
                    self.toSpawn = 0

    def handle_warp(self):
        """ Warp player to a random platform if enabled. """
        if self.randomlyWarp:
            block = random.choice(self.level.platform_list)
            self.rect.x, self.rect.y = block.rect.x, block.rect.y - 128
            self.randomlyWarp = 0

    def handle_movement(self):
        """ Handle player movement based on state. """
        if self.state == "WLeft":
            self.move_left()
        elif self.state == "WRight":
            self.move_right()
        elif self.state == "WUp":
            self.move_up()
        elif self.state == "WDown":
            self.move_down()
        elif self.state == "Idle":
            self.stop()

    def move_left(self):
        """ Move player left. """
        self.change_x = max(self.change_x - self.speedGain, -self.speedCap)
        self.Direction = 0

    def move_right(self):
        """ Move player right. """
        self.change_x = min(self.change_x + self.speedGain, self.speedCap)
        self.Direction = 1

    def move_up(self):
        """ Move player up (Free Fly Mode). """
        if self.freeFly:
            self.change_y = max(self.change_y - self.speedGain, -self.speedCap)

    def move_down(self):
        """ Move player down (Free Fly Mode). """
        if self.freeFly:
            self.change_y = min(self.change_y + self.speedGain, self.speedCap)

    def stop(self):
        """ Stop player movement. """
        self.change_x, self.change_y = 0, 0

    def handle_collisions(self):
        """ Handle player collisions with platforms. """
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:
            if self.noClip:
                continue
            
            if block.rect.left < self.rect.centerx < block.rect.right:
                if self.change_y > 0 and self.rect.bottom >= block.rect.top:
                    self.rect.bottom, self.jumps = block.rect.top, 0
                    self.change_y = 0

            if self.rect.right >= block.rect.left and self.Direction == 1:
                self.rect.right, self.change_x = block.rect.left, 0
            elif self.rect.left <= block.rect.right and self.Direction == 0:
                self.rect.left, self.change_x = block.rect.right, 0

    def update_sprite(self):
        """ Update player sprite based on movement state. """
        if self.noSprites:
            return

        sprite_set = SPRITES["idle"] if self.state == "Idle" else SPRITES["right"] if self.Direction else SPRITES["left"]
        frame_index = (self.frame // 2) % len(sprite_set)
        self.image = pygame.image.load(os.path.join('images', f"{sprite_set[frame_index]}.gif")).convert()

    def jump(self):
        """ Perform jump action. """
        if self.jumps < 2 or self.noJumpCap:
            self.change_y = -25 if self.jumps == 0 else -20
            self.jumps += 1

    def go_left(self):
        self.state = "WLeft"

    def go_right(self):
        self.state = "WRight"

    def go_up(self):
        self.state = "WUp"

    def go_down(self):
        self.state = "WDown"

    def stop_movement(self):
        self.state = "Idle"
