import pygame
from LVLDAT import Level
from PlatformOBJ import Platform
from PlayerCharacter import Player

# Colors
BLACK = (0, 0, 0)

class GMOVER(Level):
    """Prevents excessive player deaths by creating a safe level."""

    def __init__(self, player):
        """Initialize the level."""
        super().__init__(player)

        self.level_limit = -250000

        # Platforms: width, height, x, y, type
        platforms = [
            (10, 1000, 0, 1000, ""),
            (100, 100, 0, 380, ""),
            (100, 100, 100, 380, "up"),
            (100, 100, 200, 380, "down"),
            (100, 100, 300, 380, ""),
        ]

        # Add platforms to the level
        for width, height, x, y, p_type in platforms:
            block = Platform(width, height)
            block.rect.x, block.rect.y = x, y
            block.type = p_type
            block.player = self.player
            self.platform_list.add(block)
