import pygame
from LVLDAT import Level
from PlatformOBJ import Platform
from PlayerCharacter import Player

# Colors
COLORS = {
    "up": (0, 255, 0),  # GREEN
    "down": (255, 0, 0),  # RED
    "bouncy": (0, 0, 255),  # BLUE
    "normal": (255, 255, 255),  # WHITE
    "": (255, 255, 255),  # WHITE (default)
    "spawn": (255, 0, 255),  # PURPLE
    "pull": (100, 100, 100),  # GRAY
}

class Level_02(Level):
    """Definition for Level 2."""

    def __init__(self, player):
        """Initialize Level 2."""
        super().__init__(player)
        self.level_limit = -2500

        # Platform types mapping
        platform_types = [
            "spawn", "", "normal", "up", "down", "bouncy", "fall",
            "flyup", "pullup", "pulldown", "pullleft", "pullright",
            "vanish", "hazard", "fast", "slow", "reset", "goal",
            "pushable", "timed", "slideleft", "slideright"
        ]

        # Level platform list (Format: width, height, x, y, type)
        level_data = [
            (1, 1, 0, 0, 0),
            (8, 1, 1, 0, 1),
            (1, 10, 9, 0, 1),
            (25, 1, 5, 5, 1),
            (25, 1, 30, 5, 5),
            (4, 8, 55, 5, 4),
            (11, 8, 59, 3, 3),
        ]

        # Process level data
        for width, height, x, y, type_index in level_data:
            platform_type = self.get_platform_type(platform_types, type_index)
            self.create_platform(width, height, x, y, platform_type, player)

    def get_platform_type(self, platform_types, index):
        """Returns the platform type based on its index."""
        return platform_types[index] if index < len(platform_types) else ""

    def create_platform(self, width, height, x, y, platform_type, player):
        """Creates and adds platforms based on type."""
        block = Platform(width * 100, height * 100)
        block.rect.x = x * 100
        block.rect.y = y * 100
        block.type = platform_type

        # Set block color using dictionary lookup (efficient)
        block.image.fill(COLORS.get(platform_type, (255, 255, 255)))  # Default WHITE

        if platform_type == "spawn":
            player.rect.bottom = block.rect.top  # Set spawn position

        self.platform_list.add(block)
