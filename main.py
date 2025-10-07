import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid 
from asteroidfield import AsteroidField
from shot import Shot

PLAYING = "playing"
GAME_OVER = "game_over"
PAUSED = "paused"

def reset_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    return updatable, drawable, asteroids, shots, player, asteroid_field

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    updatable, drawable, asteroids, shots, player, asteroid_field = reset_game()
    state = PLAYING
    start_time = pygame.time.get_ticks()
    game_over_render = None

    while True:

        dt = game_clock.tick(60) / 1000
        pygame.display.set_caption(f"Asteroids — {game_clock.get_fps():.0f} FPS")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if state == PLAYING:
                    state = PAUSED
                elif state == PAUSED:
                    state = PLAYING
            if state == GAME_OVER and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                updatable, drawable, asteroids, shots, player, asteroid_field = reset_game()
                state = PLAYING
                start_time = pygame.time.get_ticks()
                game_over_render = None
        if state == PLAYING:
            updatable.update(dt)


            for asteroid in list(asteroids):
                if player.collides_with(asteroid):
                    state = GAME_OVER
                    survived = int((pygame.time.get_ticks() - start_time) / 1000)
                    msg = f"Game Over! Survived: {survived}s  (Press R to Restart)"
                    surf = font.render(msg, True, (255, 255, 255))
                    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    game_over_render = (surf, rect)
                    break


            for shot in list(shots):
                hit = False
                for asteroid in list(asteroids):
                    if shot.collides_with(asteroid):
                        shot.kill()
                        new_ones = asteroid.split()
                        if new_ones:
                            for a in new_ones:
                                asteroids.add(a)
                                updatable.add(a)
                                drawable.add(a)
                        hit = True
                        break

                if hit:
                    break

        screen.fill((0, 0, 0))
        for thing in drawable:
            thing.draw(screen)

        if state == GAME_OVER and game_over_render:
            s, r = game_over_render
            screen.blit(s, r)

        if state == PAUSED:
            pause_surf = font.render("Paused (P to resume)", True, (255, 255, 255))
            pause_rect = pause_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(pause_surf, pause_rect)

        pygame.display.flip()
            
      






        


if __name__ == "__main__":
   
    main()
