import pygame
import os
from LVLDAT import Level
from PlatformOBJ import Platform

# Colors
BLACK = (0, 0, 0)

class Level_04(Level):
    """Definition for Level 4."""

    def __init__(self, player):
        """Initialize Level 4."""
        super().__init__(player)
        player.text = "OFF"
        self.level_limit = -10500

        # Platform types mapping to image files
        platform_images = {
            "spawn": "spawnTile.PNG",
            "up": "moveUpTile.PNG",
            "down": "moveDownTile.PNG",
            "bouncy": "moveBounceTile.PNG",
            "normal": "floorTile.PNG",
            "": "floorTile.PNG",
            "pullup": "pullTile.PNG",
            "pulldown": "pullTile.PNG",
            "pullleft": "pullTile.PNG",
            "pullright": "pullTile.PNG",
            "message": "setMessageTile.PNG",
            "enablemessages": "setEnableTile.PNG",
            "disablemessages": "setDisableTile.PNG",
            "developer": "Dr RNG 3.PNG",
        }

        # Platform types list
        platform_types = [
            "spawn", "", "normal", "up", "down", "bouncy", "fall",
            "flyup", "pullup", "pulldown", "pullleft", "pullright",
            "vanish", "hazard", "fast", "slow", "reset", "goal",
            "pushable", "timed", "slideleft", "slideright",
            "message", "enablemessages", "disablemessages",
            "multimessage", "developer", "lowerlimit"
        ]

        # Level platform list (Format: width, height, x, y, type, optional message)
        level_data = [
            (5, 1, 0, 0, 0),  # Spawn object
            (1, 1, 5, 0, 23), 
            (10, 1, 6, 0, 22, "Hey, can you hear me?"),
            (9, 1, 16, 0, 22, "Hello?"),
            (9, 1, 25, 0, 22, "Please listen!"),
            (9, 1, 34, 0, 22, "I need your help."),
            (8, 1, 42, 0, 22, "Our program is in danger."),
            (30, 1, 50, 0, 22, "You need to go get our only developer back!"),
            (20, 1, 80, 0, 22, "He's been ignoring us for far too long."),
            (15, 1, 100, 0, 22, "You should be able to find him in the next room."),
            (1, 1, 115, 0, 24),
            (9, 1, 116, 0, 1),
            (10, 1, 125, 0, 1),
            (10, 1, 135, 0, 2),
            (10, 1, 145, 0, 3),
            (10, 1, 155, 0, 4),
            (1, 1, 999, 25, 27),  # Lower limit object
        ]

        # Process level data
        for platform in level_data:
            width, height, x, y, type_index, *optional_msg = platform
            platform_type = self.get_platform_type(platform_types, type_index)
            self.create_platform(width, height, x, y, platform_type, platform_images, optional_msg, player)

    def get_platform_type(self, platform_types, index):
        """Returns the platform type based on its index."""
        return platform_types[index] if index < len(platform_types) else ""

    def create_platform(self, width, height, x, y, platform_type, platform_images, optional_msg, player):
        """Creates and adds platforms based on type."""
        img_file = platform_images.get(platform_type, "floorTile.PNG")

        for row in range(height):
            for col in range(width):
                block = Platform(64, 64)
                block.rect.x = (x + col) * 64
                block.rect.y = (y + row) * 64
                block.type = platform_type
                block.image = pygame.image.load(os.path.join('blockimages/Tiles', img_file)).convert()

                if platform_type == "spawn":
                    player.rect.bottom = block.rect.top  # Set spawn position

                if platform_type == "message" and optional_msg:
                    block.message = optional_msg[0]

                self.platform_list.add(block)
