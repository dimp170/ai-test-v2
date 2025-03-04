import pygame
import os
from LVLDAT import Level
from PlatformOBJ import Platform

# Colors
BLACK = (0, 0, 0)

class Level_03(Level):
    """Definition for Level 3."""

    def __init__(self, player):
        """Initialize Level 3."""
        super().__init__(player)
        self.level_limit = -5500

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
            "suffer": "sufferTile.PNG",
            "developer": "Dr RNG 3.PNG"
        }

        # Platform types list
        platform_types = [
            "spawn", "", "normal", "up", "down", "bouncy", "fall",
            "flyup", "pullup", "pulldown", "pullleft", "pullright",
            "vanish", "hazard", "fast", "slow", "reset", "goal",
            "pushable", "timed", "slideleft", "slideright",
            "message", "enablemessages", "disablemessages",
            "multimessage", "developer", "lowerlimit", "suffer"
        ]

        # Level platform list (Format: width, height, x, y, type)
        level_data = [
            (1, 1, 0, 0, 0),
            (8, 10, 1, 0, 1),
            (1, 10, 9, 0, 1),
            (25, 6, 5, 5, 1),
            (25, 1, 30, 5, 5),
            (4, 8, 55, 5, 4),
            (11, 8, 59, 3, 3),
            (1, 1, 255, 255, 27),
            (22, 2, 255, 255, 28),
        ]

        # Process level data
        for width, height, x, y, type_index in level_data:
            platform_type = self.get_platform_type(platform_types, type_index)
            self.create_platform(width, height, x, y, platform_type, platform_images, player)

    def get_platform_type(self, platform_types, index):
        """Returns the platform type based on its index."""
        return platform_types[index] if index < len(platform_types) else ""

    def create_platform(self, width, height, x, y, platform_type, platform_images, player):
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

                self.platform_list.add(block)
