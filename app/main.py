import pygame
import sys
import numpy as np
from dataclasses import dataclass

W, H = 480, 720
BG_COLORS = [(40, 40, 60), (80, 80, 100)]  # Dark to medium gradient
FPS = 60
G = 0.8  # gravity magnitude
PLAT_W = 160
GAP_MIN = 180
GAP_MAX = 300
SCROLL = 4
SAMPLE_RATE = 44100

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    """Represents the player character with gravity manipulation capabilities."""

    def __init__(self) -> None:
        super().__init__()
        self.spritesheet = pygame.image.load(
            "app/assets/sprites/player.png"
        ).convert_alpha()
        self.frames = [
            self.spritesheet.subsurface(pygame.Rect(i * 40, 0, 40, 40))
            for i in range(3)
        ]
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(W // 3, H // 2))
        self.vy = 0
        self.g_dir = 1  # 1 = down, -1 = up

    def update(self, platforms: pygame.sprite.Group) -> None:
        """Update player state including animation and physics.

        Args:
            platforms: Group of platforms for collision detection
        """
        # Animate
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        # Physics
        self.vy += G * self.g_dir  # type: ignore
        self.rect.y += int(self.vy)

        # gravity flip
        if (self.g_dir == 1 and self.rect.bottom > H) or (
            self.g_dir == -1 and self.rect.top < 0
        ):
            self.kill()  # fell off-screen

        # collision check
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            # only legit contact if touching face aligned with gravity
            plat = hits[0]
            if self.g_dir == 1 and self.rect.bottom <= plat.rect.top + 10:
                self.rect.bottom = plat.rect.top
                self.vy = 0
            elif self.g_dir == -1 and self.rect.top >= plat.rect.bottom - 10:
                self.rect.top = plat.rect.bottom
                self.vy = 0
            else:
                self.kill()


class SoundGenerator:
    """Handles generation and management of game sound effects using numpy-based waveform synthesis."""

    def __init__(self) -> None:
        """Initialize sound generator with empty sound dictionary."""
        self.sounds = {}

    def generate_jump_sound(self):
        """Generate 8-bit style jump sound using square waves"""
        duration = 0.15
        freq = 440
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
        wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))
        stereo_wave = np.repeat(
            wave[:, None],  # Convert 1D array to 2D column vector
            2,  # Duplicate for stereo channels
            axis=1,
        )
        sound = pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))
        self.sounds["jump"] = sound

    def generate_death_sound(self):
        """Generate 8-bit style death sound using noise"""
        duration = 0.5
        samples = np.random.randint(
            -32767, 32767, (int(SAMPLE_RATE * duration), 2)
        )  # Stereo samples
        sound = pygame.sndarray.make_sound(samples.astype(np.int16))
        self.sounds["death"] = sound


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int) -> None:
        super().__init__()
        # Generate random platform gap
        # Generate platform with random dimensions
        self.image = pygame.Surface((PLAT_W, H), pygame.SRCALPHA)
        # Removed unused random call


@dataclass
class ParallaxLayer:
    """Dataclass representing a single parallax background layer.

    Attributes:
        surf: Surface containing the layer's visual
        offset: Current horizontal offset for scrolling effect
        speed: Scroll speed multiplier relative to foreground
    """

    surf: pygame.Surface
    offset: float
    speed: float


class ParallaxBackground:
    def __init__(self) -> None:
        self.layers = []
        for i in range(2):
            surf = pygame.Surface((W, H))
            start = BG_COLORS[i]
            end = tuple(c + 40 for c in start)
            for y in range(H):
                color = tuple(
                    int(start[c] + (end[c] - start[c]) * (y / H)) for c in range(3)
                )
                pygame.draw.line(surf, color, (0, y), (W, y))
            self.layers.append(ParallaxLayer(surf, 0, 0.2 * (i + 1)))

    def update(self) -> None:
        """Update parallax background layers."""
        for layer in self.layers:
            layer.offset -= SCROLL * layer.speed
            if layer.offset <= -W:
                layer.offset = 0

    def draw(self, screen: pygame.Surface) -> None:
        for layer in self.layers:
            screen.blit(layer.surf, (layer.offset, 0))
            screen.blit(layer.surf, (layer.offset + W, 0))


def show_game_over(screen: pygame.Surface, font: pygame.font.Font, score: int) -> bool:
    """Display game over screen with restart prompt.
    Args:
        screen: Pygame display surface
        font: Font for rendering text
        score: Final score to display
    Returns:
        bool: True if player wants to restart
    """
    screen.fill((40, 40, 60))
    text = font.render("GAME OVER", True, (255, 100, 100))
    text_rect = text.get_rect(center=(W // 2, H // 2 - 40))
    screen.blit(text, text_rect)

    score_text = font.render(f"Score: {score//10}", True, (200, 200, 200))
    score_rect = score_text.get_rect(center=(W // 2, H // 2 + 40))
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True


def main() -> None:
    """Main game loop."""
    sound_gen = SoundGenerator()
    sound_gen.generate_jump_sound()
    sound_gen.generate_death_sound()
    player = Player()
    platforms = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    background = ParallaxBackground()
    spawn_x = W

    score = 0
    font = pygame.font.SysFont(None, 48)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                player.g_dir *= -1  # flip

        # Spawn new platforms
        spawn_x -= SCROLL
        if spawn_x <= W - PLAT_W:
            platform = Platform(W)
            platforms.add(platform)
            all_sprites.add(platform)
            spawn_x = W

        all_sprites.update(platforms)
        if not player.alive():
            sound_gen.sounds["death"].play()
            pygame.display.flip()
            if show_game_over(screen, font, score):
                main()  # Restart game
            return

        score += 1
        screen.fill((30, 30, 40))
        all_sprites.draw(screen)
        score_surf = font.render(str(score // 10), True, (240, 240, 240))
        screen.blit(score_surf, (20, 20))
        # Speed indicator
        speed_surf = font.render(f"SPD: {SCROLL:.1f}", True, (200, 200, 200))
        screen.blit(speed_surf, (20, 60))
        background.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
