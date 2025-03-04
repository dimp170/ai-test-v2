import pygame
import os
from LVLDAT import Level
from PlatformOBJ import Platform

# Colors
BLACK = (0, 0, 0)

class Level_05(Level):
    """Definition for Level 5."""

    def __init__(self, player):
        """Initialize Level 5."""
        super().__init__(player)
        player.text = "OFF"
        self.level_limit = -250000

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
            "flyingplatform": "FlyingPlatform.PNG",
        }

        # Platform types list
        platform_types = [
            "spawn", "", "normal", "up", "down", "bouncy", "fall",
            "flyup", "pullup", "pulldown", "pullleft", "pullright",
            "vanish", "hazard", "fast", "slow", "reset", "goal",
            "pushable", "timed", "slideleft", "slideright",
            "message", "enablemessages", "disablemessages",
            "multimessage", "flyingplatform", "lowerlimit",
            "fpenable", "fpdisable"
        ]

        # Level platform list (Format: width, height, x, y, type, optional message)
        level_data = [
            (6, 26, -6, -25, 1),
            (5, 1, 1, 0, 23),
            (5, 1, 1, 0, 22, "This game is an absolute mess."),
            (6, 23, 6, -25, 1),
            (5, 1, 6, -4, 8),
            (5, 1, 11, 6, 22, "There's no point in continuing work on it."),
            (1, 5, 16, 2, 11),
            (1, 1, 15, 0, 8),
            (1, 1, 16, 0, 22, "Please stop trying to make me develop this trash."),
            (10, 1, 16, 2, 1),
            (1, 1, 26, 1, 11),
            (1, 1, 26, -1, 8),
            (1, 1, 0, 0, 27),
            (1, 1, 5, -5, 26),
            (1, 1, 0, 0, 0),
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
