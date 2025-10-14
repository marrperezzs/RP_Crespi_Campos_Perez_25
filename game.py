"""
Geometry Dash-style Side-scrolling Game

How to run:
1. pip install pygame
2. python game.py

Controls:
- SPACE or UP: Jump
- DOWN: Fast fall (optional)
- R: Retry (on game over)
- ESC: Quit
"""

import pygame
import random
import sys
import math
from enum import Enum
from typing import List, Optional
import os

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (135, 206, 235)
DARK_BLUE = (25, 25, 112)
PLATFORM_COLOR = (139, 69, 19)  # Brown for platforms

# Game parameters
GRAVITY = 800  # pixels/second²
JUMP_STRENGTH = -400  # pixels/second (negative for upward)
FAST_FALL_MULTIPLIER = 2.0
BASE_SPEED = 200  # pixels/second
SPEED_INCREMENT = 5  # speed increase per second
MAX_SPEED = 500  # maximum scroll speed
BASE_SPAWN_INTERVAL = 2.0  # seconds between obstacles
MIN_SPAWN_INTERVAL = 0.8  # minimum spawn interval
SPAWN_INTERVAL_DECREASE = 0.05  # decrease per second
PLAYER_SIZE = 30
OBSTACLE_MIN_WIDTH = 20
OBSTACLE_MAX_WIDTH = 60
OBSTACLE_MIN_HEIGHT = 40
OBSTACLE_MAX_HEIGHT = 120
MIN_GAP_SIZE = 100
MAX_GAP_SIZE = 200

class GameState(Enum):
    """Game state enumeration"""
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class Player:
    """Player class representing the purple square character"""
    
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.velocity_y = 0
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = 2  # Double jump enabled
        
    def update(self, dt: float, fast_fall: bool = False, platforms: List['Obstacle'] = None):
        """Update player physics"""
        if platforms is None:
            platforms = []
            
        # Apply gravity
        gravity_force = GRAVITY * dt
        if fast_fall and not self.on_ground:
            gravity_force *= FAST_FALL_MULTIPLIER
            
        self.velocity_y += gravity_force
        
        # Update position
        self.rect.y += self.velocity_y * dt
        
        # Check platform collisions (only for block-type obstacles)
        self.on_ground = False
        for platform in platforms:
            if platform.type == "block" and self.rect.colliderect(platform.rect):
                # Check if player is landing on top of the platform
                is_landing_on_top = (
                    self.velocity_y >= 0 and  # Falling or at rest
                    self.rect.bottom > platform.rect.top and  # Player is overlapping platform
                    self.rect.bottom <= platform.rect.top + 10 and  # Close to platform top (within 10 pixels)
                    self.rect.centerx >= platform.rect.left and  # Player center is within platform width
                    self.rect.centerx <= platform.rect.right
                )
                
                if is_landing_on_top:
                    # Landing on top - safe, can stand on platform
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jump_count = 0
                    break
                else:
                    # Check which side the player is hitting from
                    # Only end game if hitting from the LEFT side of the platform
                    
                    # Check if hitting from the left (player's right side hits platform's left side)
                    is_hitting_from_left = (
                        self.rect.right > platform.rect.left and  # Player's right side is overlapping platform's left
                        self.rect.right <= platform.rect.left + 10 and  # Close to platform's left edge
                        self.rect.centerx < platform.rect.centerx  # Player is to the left of platform center
                    )
                    
                    if is_hitting_from_left:
                        # Hitting from left - push player back and trigger game over
                        self.rect.x = platform.rect.left - self.rect.width - 1
                        return "deadly_collision"
                    else:
                        # Hitting from top, bottom, or right - just push player away but continue game
                        if self.rect.bottom <= platform.rect.top + 10:
                            # Hitting from top - push player up
                            self.rect.bottom = platform.rect.top
                            self.velocity_y = 0
                        elif self.rect.top >= platform.rect.bottom - 10:
                            # Hitting from bottom - push player down
                            self.rect.top = platform.rect.bottom
                            self.velocity_y = 0
                        elif self.rect.left >= platform.rect.right - 10:
                            # Hitting from right - push player to the right
                            self.rect.x = platform.rect.right + 1
        
        # Ground collision
        if self.rect.bottom >= SCREEN_HEIGHT - 50:  # Ground level
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.on_ground = True
            self.jump_count = 0
            
        # Ceiling collision
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity_y = 0
            
    def jump(self):
        """Make the player jump"""
        if self.jump_count < self.max_jumps:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            self.jump_count += 1
            
    def draw(self, surface: pygame.Surface):
        """Draw the player"""
        pygame.draw.rect(surface, PURPLE, self.rect)
        # Add a small highlight for visual appeal
        highlight = pygame.Rect(self.rect.x + 2, self.rect.y + 2, 
                               self.rect.width - 4, self.rect.height - 4)
        pygame.draw.rect(surface, (200, 100, 255), highlight)

class Obstacle:
    """Obstacle class for enemies and barriers"""
    
    def __init__(self, x: int, y: int, width: int, height: int, obstacle_type: str = "block", is_horizontal: bool = False):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = obstacle_type
        self.is_horizontal = is_horizontal  # True for horizontal platforms
        self.scored = False  # Track if player has passed this obstacle
        
    def update(self, dt: float, scroll_speed: float):
        """Update obstacle position"""
        self.rect.x -= scroll_speed * dt
        
    def draw(self, surface: pygame.Surface):
        """Draw the obstacle"""
        if self.type == "block":
            # Draw as a platform (brown color)
            color = PLATFORM_COLOR if not self.is_horizontal else (101, 67, 33)  # Darker for horizontal
            pygame.draw.rect(surface, color, self.rect)
            # Add some visual detail
            inner_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2,
                                   self.rect.width - 4, self.rect.height - 4)
            inner_color = (160, 82, 45) if not self.is_horizontal else (139, 69, 19)
            pygame.draw.rect(surface, inner_color, inner_rect)
            # Add platform texture lines
            if self.is_horizontal:
                # Horizontal lines for horizontal platforms
                for i in range(0, self.rect.height, 4):
                    pygame.draw.line(surface, (101, 67, 33), 
                                   (self.rect.x, self.rect.y + i), 
                                   (self.rect.right, self.rect.y + i), 1)
            else:
                # Vertical lines for vertical platforms
                for i in range(0, self.rect.width, 8):
                    pygame.draw.line(surface, (101, 67, 33), 
                                   (self.rect.x + i, self.rect.y), 
                                   (self.rect.x + i, self.rect.bottom), 1)
        elif self.type == "spike":
            # Draw as a triangle (still dangerous)
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.left, self.rect.bottom),
                (self.rect.right, self.rect.bottom)
            ]
            pygame.draw.polygon(surface, RED, points)
            
    def is_off_screen(self) -> bool:
        """Check if obstacle is off the left side of screen"""
        return self.rect.right < 0

class Background:
    """Background with scrolling elements"""
    
    def __init__(self):
        self.clouds = []
        self.stars = []
        self.cloud_speed = 50  # Slower than main scroll speed
        self.star_speed = 30
        
        # Generate initial clouds
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'size': random.randint(20, 40)
            })
            
        # Generate initial stars
        for _ in range(20):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - 100),
                'size': random.randint(1, 3)
            })
    
    def update(self, dt: float, scroll_speed: float):
        """Update background elements"""
        # Update clouds
        for cloud in self.clouds[:]:
            cloud['x'] -= self.cloud_speed * dt
            if cloud['x'] + cloud['size'] < 0:
                cloud['x'] = SCREEN_WIDTH + cloud['size']
                cloud['y'] = random.randint(50, 200)
                cloud['size'] = random.randint(20, 40)
                
        # Update stars
        for star in self.stars[:]:
            star['x'] -= self.star_speed * dt
            if star['x'] < 0:
                star['x'] = SCREEN_WIDTH
                star['y'] = random.randint(0, SCREEN_HEIGHT - 100)
                star['size'] = random.randint(1, 3)
    
    def draw(self, surface: pygame.Surface):
        """Draw the background"""
        # Sky gradient
        for y in range(SCREEN_HEIGHT - 50):
            color_ratio = y / (SCREEN_HEIGHT - 50)
            r = int(LIGHT_BLUE[0] * (1 - color_ratio) + DARK_BLUE[0] * color_ratio)
            g = int(LIGHT_BLUE[1] * (1 - color_ratio) + DARK_BLUE[1] * color_ratio)
            b = int(LIGHT_BLUE[2] * (1 - color_ratio) + DARK_BLUE[2] * color_ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw stars
        for star in self.stars:
            pygame.draw.circle(surface, WHITE, (int(star['x']), int(star['y'])), star['size'])
            
        # Draw clouds
        for cloud in self.clouds:
            # Simple cloud shape
            pygame.draw.circle(surface, WHITE, (int(cloud['x']), int(cloud['y'])), cloud['size'])
            pygame.draw.circle(surface, WHITE, (int(cloud['x'] + cloud['size']//2), int(cloud['y'])), cloud['size']//2)
            pygame.draw.circle(surface, WHITE, (int(cloud['x'] - cloud['size']//2), int(cloud['y'])), cloud['size']//2)

class Spawner:
    """Handles obstacle spawning and difficulty progression"""
    
    def __init__(self):
        self.last_spawn_time = 0
        self.current_spawn_interval = BASE_SPAWN_INTERVAL
        
    def update(self, current_time: float, game_time: float) -> bool:
        """Update spawner and return True if should spawn"""
        # Calculate current spawn interval based on game time
        self.current_spawn_interval = max(
            MIN_SPAWN_INTERVAL,
            BASE_SPAWN_INTERVAL - (game_time * SPAWN_INTERVAL_DECREASE)
        )
        
        if current_time - self.last_spawn_time >= self.current_spawn_interval:
            self.last_spawn_time = current_time
            return True
        return False
        
    def spawn_obstacle(self) -> List[Obstacle]:
        """Spawn obstacles - can return multiple obstacles for combinations"""
        obstacles = []
        
        # Choose spawn pattern
        pattern = random.choice([
            "single_vertical", "single_horizontal", "spike_wall", 
            "platform_combo", "floating_platform", "gap_jump"
        ])
        
        if pattern == "single_vertical":
            # Single vertical platform
            width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
            height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
            x = SCREEN_WIDTH
            y = SCREEN_HEIGHT - 50 - height
            obstacles.append(Obstacle(x, y, width, height, "block", False))
            
        elif pattern == "single_horizontal":
            # Single horizontal platform
            width = random.randint(80, 150)
            height = random.randint(15, 25)
            x = SCREEN_WIDTH
            y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 100)
            obstacles.append(Obstacle(x, y, width, height, "block", True))
            
        elif pattern == "spike_wall":
            # Wall of spikes
            for i in range(random.randint(2, 4)):
                width = random.randint(20, 40)
                height = random.randint(40, 80)
                x = SCREEN_WIDTH + (i * 30)
                y = SCREEN_HEIGHT - 50 - height
                obstacles.append(Obstacle(x, y, width, height, "spike"))
                
        elif pattern == "platform_combo":
            # Vertical platform with horizontal platform above
            # Vertical platform
            v_width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
            v_height = random.randint(60, 100)
            v_x = SCREEN_WIDTH
            v_y = SCREEN_HEIGHT - 50 - v_height
            obstacles.append(Obstacle(v_x, v_y, v_width, v_height, "block", False))
            
            # Horizontal platform above
            h_width = random.randint(60, 120)
            h_height = 20
            h_x = SCREEN_WIDTH + v_width + 20
            h_y = v_y - random.randint(80, 120)
            obstacles.append(Obstacle(h_x, h_y, h_width, h_height, "block", True))
            
        elif pattern == "floating_platform":
            # Multiple floating horizontal platforms
            for i in range(random.randint(2, 3)):
                width = random.randint(60, 100)
                height = 20
                x = SCREEN_WIDTH + (i * 120)
                y = random.randint(200, SCREEN_HEIGHT - 150)
                obstacles.append(Obstacle(x, y, width, height, "block", True))
                
        elif pattern == "gap_jump":
            # Two vertical platforms with gap
            width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
            height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
            
            # First platform
            x1 = SCREEN_WIDTH
            y1 = SCREEN_HEIGHT - 50 - height
            obstacles.append(Obstacle(x1, y1, width, height, "block", False))
            
            # Second platform with gap
            gap = random.randint(80, 150)
            x2 = SCREEN_WIDTH + width + gap
            y2 = SCREEN_HEIGHT - 50 - height
            obstacles.append(Obstacle(x2, y2, width, height, "block", False))
            
        return obstacles

class Game:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Dash Clone")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.state = GameState.MENU
        self.reset_game()
        
        # Background
        self.background = Background()
        
        # Music
        self.music_playing = False
        self.setup_music()
        
        # High score
        self.high_score = self.load_high_score()
        
    def setup_music(self):
        """Setup background music"""
        try:
            # Create a simple beep pattern as background music
            # Since we don't have external music files, we'll create a simple pattern
            self.music_playing = False
        except:
            self.music_playing = False
            
    def start_music(self):
        """Start background music"""
        if not self.music_playing:
            try:
                # For now, we'll just set a flag - in a real game you'd load music files
                self.music_playing = True
            except:
                pass
                
    def stop_music(self):
        """Stop background music"""
        if self.music_playing:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
            except:
                self.music_playing = False
        
    def reset_game(self):
        """Reset game to initial state"""
        self.player = Player(100, SCREEN_HEIGHT - 50 - PLAYER_SIZE)
        self.obstacles: List[Obstacle] = []
        self.spawner = Spawner()
        self.score = 0
        self.game_start_time = 0
        self.scroll_speed = BASE_SPEED
        
    def load_high_score(self) -> int:
        """Load high score from file"""
        try:
            if os.path.exists("highscore.dat"):
                with open("highscore.dat", "r") as f:
                    return int(f.read().strip())
        except (ValueError, IOError):
            pass
        return 0
        
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open("highscore.dat", "w") as f:
                f.write(str(self.high_score))
        except IOError:
            pass
            
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.MENU:
                        return False
                    elif self.state == GameState.GAME_OVER:
                        return False
                    else:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.MENU:
                    if event.key != pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks() / 1000.0
                        self.start_music()
                        
                elif self.state == GameState.PLAYING:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.player.jump()
                        
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks() / 1000.0
                        self.start_music()
                        
        return True
        
    def update(self, dt: float):
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return
            
        current_time = pygame.time.get_ticks() / 1000.0
        game_time = current_time - self.game_start_time
        
        # Update difficulty
        self.scroll_speed = min(MAX_SPEED, BASE_SPEED + (game_time * SPEED_INCREMENT))
        
        # Handle fast fall
        keys = pygame.key.get_pressed()
        fast_fall = keys[pygame.K_DOWN]
        
        # Update background
        self.background.update(dt, self.scroll_speed)
        
        # Update player
        collision_result = self.player.update(dt, fast_fall, self.obstacles)
        if collision_result == "deadly_collision":
            self.state = GameState.GAME_OVER
            self.stop_music()
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            return
        
        # Spawn obstacles
        if self.spawner.update(current_time, game_time):
            new_obstacles = self.spawner.spawn_obstacle()
            self.obstacles.extend(new_obstacles)
            
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(dt, self.scroll_speed)
            
            # Check for scoring
            if not obstacle.scored and obstacle.rect.right < self.player.rect.left:
                obstacle.scored = True
                self.score += 1
                
            # Remove off-screen obstacles
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                
        # Check collisions - only spikes are deadly, platforms are solid barriers
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect) and obstacle.type == "spike":
                # Spikes are deadly
                self.state = GameState.GAME_OVER
                self.stop_music()
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                break
            # Block platforms are handled in player.update as solid barriers
                
    def draw_menu(self):
        """Draw the welcome/menu screen"""
        # Draw animated background
        self.background.draw(self.screen)
        self.background.update(0.016, 50)  # Slow animation
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title with shadow effect
        title_text = self.big_font.render("GEOMETRY DASH CLONE", True, WHITE)
        title_shadow = self.big_font.render("GEOMETRY DASH CLONE", True, PURPLE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 117))
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Controls with better formatting
        controls_title = self.font.render("CONTROLS:", True, WHITE)
        controls_title_rect = controls_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(controls_title, controls_title_rect)
        
        controls = [
            "SPACE or UP - Jump (Double Jump!)",
            "DOWN - Fast fall",
            "ESC - Quit"
        ]
        
        y_offset = SCREEN_HEIGHT // 2 - 10
        for i, control in enumerate(controls):
            text = self.font.render(control, True, LIGHT_BLUE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 35))
            self.screen.blit(text, text_rect)
            
        # Game features
        features_title = self.font.render("FEATURES:", True, WHITE)
        features_title_rect = features_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(features_title, features_title_rect)
        
        features = [
            "• Jump on brown platforms",
            "• Avoid red spikes",
            "• Use horizontal platforms",
            "• Survive as long as possible!"
        ]
        
        y_offset = SCREEN_HEIGHT // 2 + 110
        for i, feature in enumerate(features):
            text = self.font.render(feature, True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 30))
            self.screen.blit(text, text_rect)
            
        # Start instruction with pulsing effect
        pulse = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
        start_color = (pulse, 255, pulse)
        start_text = self.font.render("Press any key to start", True, start_color)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250))
        self.screen.blit(start_text, start_rect)
        
        # High score
        if self.high_score > 0:
            hs_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 290))
            self.screen.blit(hs_text, hs_rect)
            
    def draw_game_over(self):
        """Draw the game over screen"""
        self.screen.fill(BLACK)
        
        # Game Over text
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(score_text, score_rect)
        
        # High score
        if self.score == self.high_score and self.score > 0:
            new_high_text = self.font.render("NEW HIGH SCORE!", True, GREEN)
            new_high_rect = new_high_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(new_high_text, new_high_rect)
        else:
            hs_text = self.font.render(f"High Score: {self.high_score}", True, GRAY)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(hs_text, hs_rect)
            
        # Options
        options = [
            "[R] Retry",
            "[ESC] Quit"
        ]
        
        y_offset = SCREEN_HEIGHT // 2 + 60
        for i, option in enumerate(options):
            text = self.font.render(option, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 40))
            self.screen.blit(text, text_rect)
            
    def draw_hud(self):
        """Draw the heads-up display"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Speed indicator
        speed_text = self.font.render(f"Speed: {int(self.scroll_speed)}", True, WHITE)
        self.screen.blit(speed_text, (10, 50))
        
    def draw(self):
        """Draw the current game state"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        else:  # PLAYING
            # Draw background
            self.background.draw(self.screen)
            
            # Draw ground
            ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
            pygame.draw.rect(self.screen, DARK_GRAY, ground_rect)
            
            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            
            # Draw player
            self.player.draw(self.screen)
                
            # Draw HUD
            self.draw_hud()
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
            
        pygame.quit()
        sys.exit()

def main():
    """Main function"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
