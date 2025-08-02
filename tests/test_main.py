"""Test suite for main game functionality."""
import pytest
from app.main import Player
import pygame

@pytest.fixture
def mock_platform_group():
    return pygame.sprite.Group()

def test_player_initialization():
    """Test player sprite initializes with correct properties."""
    player = Player()
    assert player.rect.center == (160, 360)
    assert len(player.frames) == 3

def test_player_physics(mock_platform_group):
    """Test gravity and movement calculations."""
    player = Player()
    initial_y = player.rect.y
    player.update(mock_platform_group)
    assert player.rect.y > initial_y