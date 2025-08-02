import pygame


def create_sprite_sheet():
    pygame.init()
    surf = pygame.Surface((120, 40), pygame.SRCALPHA)
    colors = [(255, 100, 100), (255, 180, 100), (255, 100, 180)]
    for i in range(3):
        rect = pygame.Rect(i * 40, 0, 40, 40)
        pygame.draw.rect(surf, colors[i], rect, border_radius=6)
    pygame.image.save(surf, "assets/sprites/player.png")


if __name__ == "__main__":
    create_sprite_sheet()
