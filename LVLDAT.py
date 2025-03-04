import pygame

# Colors
BLACK = (0, 0, 0)

class Level:
    def __init__(self, player):
        """Initialize level properties and sprite groups."""
        self.player = player
        self.world_shift = 0
        self.world_height = 0

        # Sprite Groups
        self.sprite_groups = {
            "platforms": pygame.sprite.Group(),
            "image_platforms": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(),
            "end_objects": pygame.sprite.Group(),
            "push_blocks": pygame.sprite.Group()
        }

    def update(self):
        """Update all objects in the level."""
        for group in self.sprite_groups.values():
            group.update()

    def draw(self, screen):
        """Draw the level background and all objects."""
        screen.fill(BLACK)  # Clear screen
        for group in self.sprite_groups.values():
            group.draw(screen)

    def shift_world_x(self, shift_x):
        """Shift all objects in the level horizontally."""
        self.world_shift += shift_x
        for group in self.sprite_groups.values():
            for sprite in group:
                sprite.rect.x += shift_x

    def shift_world_y(self, shift_y):
        """Shift all objects in the level vertically."""
        self.world_height += shift_y
        for group in self.sprite_groups.values():
            for sprite in group:
                sprite.rect.y += shift_y
