import pygame
import random
import statistics as st
from LoadDepends import *

# Global constants
level_count = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600

# Music list
Music = ["Silence", "Silence", "loop0", "loop2"]

def handle_keydown(event, player, current_level_no, level_list):
    """Handles keydown events to improve code readability."""
    if event.key == pygame.K_SPACE:
        player.text = "ON"
    elif event.key == pygame.K_LEFT:
        player.go_left()
    elif event.key == pygame.K_RIGHT:
        player.go_right()
    elif event.key == pygame.K_UP:
        if player.freeFly != 1:
            player.jump()
        else:
            player.go_up()
    elif event.key == pygame.K_DOWN:
        if player.freeFly == 1:
            player.go_down()
    elif event.key == pygame.K_KP0:
        player.debug = 1 - player.debug  # Toggle debug mode
    elif event.key == pygame.K_KP1:
        player.noParticles = 1 - player.noParticles  # Toggle particles
    elif event.key == pygame.K_KP2:
        player.noClip = 1 - player.noClip  # Toggle collision
    elif event.key == pygame.K_KP3:
        player.noPhysicsBlocks = 1 - player.noPhysicsBlocks  # Toggle block physics
    elif event.key == pygame.K_KP4:
        player.noSprites = 1 - player.noSprites
        player.justSet = 1
    elif event.key == pygame.K_KP5:
        player.toSpawn = 1  # Warp to spawn
    elif event.key == pygame.K_KP6:
        player.randomlyWarp = 1  # Random teleport
    elif event.key == pygame.K_KP8:
        player.noJumpCap = 1 - player.noJumpCap  # Toggle infinite jumps
    elif event.key == pygame.K_KP9:
        player.freeFly = 1 - player.freeFly  # Toggle free fly mode
    elif event.key == pygame.K_KP_PLUS:
        player.speedMultiplier += 1
    elif event.key == pygame.K_KP_MINUS:
        player.speedMultiplier -= 1
    elif event.key == pygame.K_END:
        return handle_level_change(current_level_no, level_list, player)

    return current_level_no

def handle_keyup(event, player):
    """Handles keyup events to ensure smooth player movement."""
    if event.key == pygame.K_LEFT and player.change_x < 0:
        player.stop()
    elif event.key == pygame.K_RIGHT and player.change_x > 0:
        player.stop()
    elif event.key == pygame.K_UP and player.change_y < 0 and player.freeFly == 1:
        player.stop()
    elif event.key == pygame.K_DOWN and player.change_y > 0 and player.freeFly == 1:
        player.stop()

def handle_level_change(current_level_no, level_list, player):
    """Handles level transitions while updating the music."""
    pygame.mixer_music.fadeout(300)
    
    if current_level_no < len(level_list) - 1:
        current_level_no += 1
    else:
        current_level_no = 0

    player.level = level_list[current_level_no]
    player.toSpawn = 1
    player.text = 0
    player.justSet = 1
    return current_level_no

def update_music(current_level_no):
    """Handles music playback efficiently."""
    if pygame.mixer_music.get_pos() == -1:
        pygame.mixer_music.fadeout(3000)
        pygame.mixer_music.load(f"music/{Music[current_level_no]}.wav")
        pygame.mixer_music.play(loops=0, start=0.0, fade_ms=0)

def render_debug_info(screen, font, player, current_level_no, current_position, current_height):
    """Renders debug information on the screen."""
    debug_texts = [
        f"POS_X {current_position}",
        f"POS_Y {current_height}",
        f"JUMPS {player.jumps}",
        f"FALL_SPEED_CHECK {player.snappedtofloor}",
        f"FACING {player.Direction}",
        f"BOUNCE_COUNT {player.bounces}",
        f"X_SPEED {player.change_x}",
        f"Y_SPEED {player.change_y}",
        f"NO_COLLISION {player.noClip}",
        f"FLY_MODE {player.freeFly}",
        f"INFINITE_JUMP {player.noJumpCap}",
        f"NO_SPRITES {player.noSprites} {player.noParticles}",
        f"NO_BLOCK_PROPERTIES {player.noPhysicsBlocks}",
        f"FLYING_PLATFORM_ACTIVE {player.fpEnabled}",
        f"STAGE {current_level_no}",
    ]

    for i, text in enumerate(debug_texts):
        debug_surface = font.render(text, True, (150, 95, 255))
        screen.blit(debug_surface, (50, 65 + i * 15))

def main():
    """Main Program"""
    pygame.init()
    font = pygame.font.SysFont("arial", 15)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Scriptopolis Game")

    player = Player()
    level_list = [Level_01(player)]
    current_level_no = 0
    current_level = level_list[current_level_no]
    
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x, player.rect.y = 340, SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    
    pygame.mixer_music.load(f"music/{Music[current_level_no]}.wav")
    pygame.mixer_music.play(loops=0, start=0.0, fade_ms=1999)
    
    clock = pygame.time.Clock()
    done = False

    while not done:
        size = pygame.display.get_window_size()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                current_level_no = handle_keydown(event, player, current_level_no, level_list)
            elif event.type == pygame.KEYUP:
                handle_keyup(event, player)

        update_music(current_level_no)

        active_sprite_list.update()
        current_level.update()

        # Camera movement
        scale_x = size[0] // 4
        scale_y = size[1] // 4

        if player.rect.right >= scale_x * 3:
            current_level.shift_world_x(scale_x * 3 - player.rect.right)
        elif player.rect.left <= scale_x:
            current_level.shift_world_x(scale_x - player.rect.left)
        if player.rect.top <= scale_y:
            current_level.shift_world_y(scale_y - player.rect.top)
        elif player.rect.bottom >= scale_y * 3:
            current_level.shift_world_y(scale_y * 3 - player.rect.bottom)

        # Level transition
        current_position = player.rect.x + current_level.world_shift
        current_height = player.rect.y + current_level.world_height
        
        if current_position < current_level.level_limit:
            player.rect.x = 120
            current_level_no = handle_level_change(current_level_no, level_list, player)

        screen.fill(BLACK)
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        if player.debug:
            render_debug_info(screen, font, player, current_level_no, current_position, current_height)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
