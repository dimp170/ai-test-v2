import pygame
from LVLDAT import Level
from PlatformOBJ import Platform
from PlatformImageOBJ import PlatformImage
from PlayerCharacter import Player
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 100, 100)
PURPLE = (255, 0, 255)
GRAY = (100, 100, 100)


class Level_02(Level):


    def __init__(self, player):
        """Initialize level 1."""
        super().__init__(player)
        self.level_limit = -2500

        # Platform types mapping to image files
        platform_images = {
            "spawn": "spawnTile.PNG",
            "up": "moveUpTile.PNG",
            "down": "moveDownTile.PNG",
            "bouncy": "moveBounceTile.PNG",
            "normal": "floorTile.PNG",
            "": "floorTile.PNG",
            "push": "moveDownTile.PNG",
            "message": "setMessageTile.PNG",
            "enablemessages": "setEnableTile.PNG",
            "disablemessages": "setDisableTile.PNG",
            "suffer": "sufferTile.PNG",
            "developer": "Dr RNG 3.PNG",
            "flyingplatform": "FlyingPlatform.PNG",
            "pullup": "pullTile.PNG",
            "pulldown": "pullTile.PNG",
            "pullleft": "pullTile.PNG",
            "pullright": "pullTile.PNG"
        }

        # Level platform list (Format: width, height, x, y, type, [optional message])
        level_data = [
            [1, 11, -1, -22, 1], [1, 11, 4, -24, 1],
            [1, 1, -5, 0, 8],  # Pull block (up)
            [10, 1, 5, -24, 1], [1, 1, 0, -15, 5],  # Bouncy block
            [9, 1, -1, -11, 1], [9, 1, -10, -4, 1],
            [1, 8, -1, -11, 1], [1, 1, 0, -1, 5],  # Bouncy block
            [1, 1, 1, -6, 3],  # Up elevator block
            [1, 5, 2, -5, 1], [1, 1, 3, -8, 4],  # Down elevator block
            [1, 1, 4, -4, 5],  # Bouncy block
            [1, 1, 8, -8, 1], [2, 1, -4, 0, 1], [1, 5, 1, -5, 1],
            [1, 5, 3, -5, 1], [6, 3, 4, -3, 1], [20, 1, 1, 0, 1],
            [2, 1, -1, 0, 1], [2, 1, -1, 0, 1],
            [1, 1, -2, 25000, 22, "This is where you respawn if you fall off."],
            [1, 1, -2, 55, 27],  # Lower limit (respawn zone)
            [1, 2, 8, -5, 18],  # Pushable block
            [1, 1, 6, 25000, 22, "Pushable blocks! Fun, right?"],
            [1, 1, 16, -5, 26],  # Flying block
            [1, 1, 16, 25000, 22, "Floating blocks can fly. They have movement limits."],
            [1, 1, 8 + 16, 25, 29],  # Flying block disabled zone
            [15, 1, 9, 25, 28],  # Flying block enabled zone
            [1, 1, 8, 25, 29],  # Flying block disabled zone
            [1, 10, -25, -9, 30],  # Suffer!
            [2, 3, 8, -8, 1],
            [1, 1, -2, 0, 0],  # Spawn block
        ]

        # Process level data
        for platform in level_data:
            width, height, x, y, type_index, *optional_msg = platform
            platform_type = self.get_platform_type(type_index)

            self.create_platform(width, height, x, y, platform_type, platform_images, optional_msg)

    def get_platform_type(self, index):
        """Returns the platform type based on its index."""
        platform_types = [
            "spawn", "", "normal", "up", "down", "bouncy", "fall",
            "flyup", "pullup", "pulldown", "pullleft", "pullright",
            "vanish", "hazard", "fast", "slow", "reset", "goal",
            "push", "timed", "slideleft", "slideright", "message",
            "enablemessages", "disablemessages", "multimessage",
            "flyingplatform", "lowerlimit", "fpenable", "fpdisable",
            "suffer"
        ]
        return platform_types[index] if index < len(platform_types) else ""

    def create_platform(self, width, height, x, y, platform_type, platform_images, optional_msg):
        """Creates and adds platforms based on type."""
        img_file = platform_images.get(platform_type, "floorTile.PNG")

        for row in range(height):
            for col in range(width):
                block = Platform(64, 64)
                block.rect.x = (x + col) * 64
                block.rect.y = (y + row) * 64
                block.type = platform_type
                block.image = pygame.image.load(os.path.join('blockimages/Tiles', img_file)).convert()

                if platform_type == "message" and optional_msg:
                    block.message = optional_msg[0]

                self.platform_list.add(block)