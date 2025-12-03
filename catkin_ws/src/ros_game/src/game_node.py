#!/usr/bin/env python3

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
import rospy
from std_msgs.msg import String, Int64
from ros_game_msgs.msg import user_msg

from ros_game.srv import GetUserScore, GetUserScoreResponse
from ros_game.srv import SetGameDifficulty, SetGameDifficultyResponse



import pygame
import random
import sys
import math
from enum import Enum
from typing import List, Optional
import os
from array import array

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
YELLOW = (255, 255, 0)

# Background milestone colors
SUNSET_SKY = (255, 165, 0)  # Orange
SUNSET_GROUND = (255, 69, 0)  # Red-orange
NIGHT_SKY = (25, 25, 112)  # Midnight blue
NIGHT_GROUND = (0, 0, 0)  # Black
RAINBOW_SKY = (255, 20, 147)  # Deep pink
RAINBOW_GROUND = (0, 191, 255)  # Deep sky blue

# Retro arcade colors
NEON_GREEN = (0, 255, 0)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_CYAN = (0, 255, 255)
ARCADE_PURPLE = (128, 0, 128)
ARCADE_RED = (255, 0, 0)
ARCADE_CYAN = (0, 255, 255)

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
        
        # Draw smiley face
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        # Eyes
        eye_size = 3
        left_eye_x = center_x - 8
        right_eye_x = center_x + 8
        eye_y = center_y - 5
        pygame.draw.circle(surface, WHITE, (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(surface, WHITE, (right_eye_x, eye_y), eye_size)
        
        # Eye pupils
        pygame.draw.circle(surface, BLACK, (left_eye_x, eye_y), 1)
        pygame.draw.circle(surface, BLACK, (right_eye_x, eye_y), 1)
        
        # Smile (arc)
        smile_rect = pygame.Rect(center_x - 10, center_y - 2, 20, 12)
        pygame.draw.arc(surface, WHITE, smile_rect, 0, 3.14, 2)

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
        self.current_sky_color = LIGHT_BLUE  # Default sky color
        self.current_ground_color = DARK_BLUE  # Default ground color
        
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
            r = int(self.current_sky_color[0] * (1 - color_ratio) + self.current_ground_color[0] * color_ratio)
            g = int(self.current_sky_color[1] * (1 - color_ratio) + self.current_ground_color[1] * color_ratio)
            b = int(self.current_sky_color[2] * (1 - color_ratio) + self.current_ground_color[2] * color_ratio)
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
    
    def change_colors(self, sky_color, ground_color):
        """Change the background colors"""
        self.current_sky_color = sky_color
        self.current_ground_color = ground_color

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

        rospy.init_node('game_node')

        self.user_name = ""
        self.user_username = ""
        self.user_age = 0

        self.last_command: Optional[str] = None

        self.user_sub = rospy.Subscriber('/user_information', user_msg, self.user_info_callback)
        self.key_sub = rospy.Subscriber('/keyboard_control', String, self.key_callback) 
        self.result_pub = rospy.Publisher('/result_information', Int64, queue_size=10)

        rospy.loginfo("Game initialized, waiting for user info...")

        self.user_scores = {}
        self.current_difficulty = "medium"
        self.speed_multiplier = 1.0  # Default speed multiplier

        self.user_score_srv = rospy.Service('/user_score', GetUserScore, self.handle_user_score)
        self.set_difficulty_srv = rospy.Service('/difficulty', SetGameDifficulty, self.handle_set_difficulty)

        rospy.loginfo("Services ready.")

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Dash Clone")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.retro_font = pygame.font.Font(None, 48)
        self.retro_big_font = pygame.font.Font(None, 96)
        
        # Background
        self.background = Background()
        
        # Background milestone tracking
        self.last_milestone = 0
        
        self.state = GameState.MENU
        self.reset_game()
        
        # Music
        self.music_playing = False
        self.setup_music()
        
        # High score
        self.high_score = self.load_high_score()
        
    def setup_music(self):
        """Setup procedural background music and separate menu/over loops."""
        self.music_sound = None
        self.menu_music_sound = None
        self.over_music_sound = None
        self.explosion_sound = None
        try:
            # Ensure mixer is initialized with predictable format
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

            def generate_music_sound(sample_rate: int = 44100) -> pygame.mixer.Sound:
                # Simple 2-bar arpeggiated loop using sine waves
                pattern = [
                    (261.63, 0.20), (329.63, 0.20), (392.00, 0.20), (523.25, 0.40),  # C E G C5
                    (392.00, 0.20), (329.63, 0.20), (261.63, 0.20), (196.00, 0.40),  # G E C G3
                    (220.00, 0.20), (277.18, 0.20), (349.23, 0.20), (440.00, 0.40),  # A C# F A
                    (349.23, 0.20), (277.18, 0.20), (220.00, 0.20), (174.61, 0.40),  # F C# A F3
                ]

                # ADSR-like simple envelope per note to avoid clicks
                attack = 0.01
                release = 0.04
                volume = 0.18  # master volume (0..1)

                samples = array('h')
                two_pi = 2.0 * math.pi
                phase = 0.0

                for freq, dur in pattern:
                    num = int(dur * sample_rate)
                    step = two_pi * freq / sample_rate
                    for i in range(num):
                        t = i / sample_rate
                        # Envelope
                        env = 1.0
                        if t < attack:
                            env = t / attack
                        elif t > (dur - release):
                            env = max(0.0, (dur - t) / release)

                        # Add a quiet second harmonic for richness
                        s = math.sin(phase) * 0.8 + math.sin(phase * 2.0) * 0.2
                        val = int(max(-1.0, min(1.0, s)) * env * volume * 32767)
                        samples.append(val)
                        phase += step

                # Create Sound from raw samples; loop will repeat seamlessly
                return pygame.mixer.Sound(buffer=samples)

            self.music_sound = generate_music_sound()

            def generate_relaxed_music_sound(sample_rate: int = 44100) -> pygame.mixer.Sound:
                # Calm pad-like loop: slow chords with soft envelope
                chords = [
                    # (root, major third, fifth) as frequencies
                    (261.63, 329.63, 392.00),  # C major
                    (220.00, 277.18, 329.63),  # A minor/C#dim flavor (soft)
                    (246.94, 311.13, 369.99),  # B♭ (relaxed)
                    (233.08, 293.66, 349.23),  # B♭->A# style to F
                ]

                note_dur = 0.8
                gap = 0.05
                attack = 0.05
                release = 0.2
                volume = 0.12

                samples = array('h')
                two_pi = 2.0 * math.pi
                t_global = 0.0

                for (f1, f2, f3) in chords:
                    total = int(note_dur * sample_rate)
                    for i in range(total):
                        t = i / sample_rate
                        # Gentle LFO for movement
                        lfo = 0.02 * math.sin(two_pi * 0.5 * (t_global + t))
                        # Envelope
                        env = 1.0
                        if t < attack:
                            env = t / attack
                        elif t > (note_dur - release):
                            env = max(0.0, (note_dur - t) / release)
                        # Sum three sines, include quiet harmonics
                        s = (
                            math.sin(two_pi * (f1 + lfo) * (t_global + t)) * 0.6 +
                            math.sin(two_pi * (f2 + lfo) * (t_global + t)) * 0.6 +
                            math.sin(two_pi * (f3 + lfo) * (t_global + t)) * 0.6 +
                            math.sin(two_pi * 2.0 * (f1 + lfo) * (t_global + t)) * 0.1
                        ) / 3.0
                        val = int(max(-1.0, min(1.0, s)) * env * volume * 32767)
                        samples.append(val)

                    # Small gap between chords
                    gap_n = int(gap * sample_rate)
                    for _ in range(gap_n):
                        samples.append(0)
                    t_global += note_dur + gap

                return pygame.mixer.Sound(buffer=samples)

            # Over/game-over relaxed track
            self.over_music_sound = generate_relaxed_music_sound()

            def generate_happy_menu_music(sample_rate: int = 44100) -> pygame.mixer.Sound:
                # Bright, simple, happy arpeggio with light bell-like harmonics
                scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major up to C5
                pattern = []
                # Build a short cheerful pattern
                for f in [0, 2, 4, 7, 4, 2, 0, 7]:  # C E G B♭(approx via A: keep G)
                    pattern.append((scale[f], 0.16))
                for f in [4, 5, 7, 9 - 2, 7, 5, 4, 0]:  # G A C5 (approx) then back
                    idx = max(0, min(len(scale) - 1, f))
                    pattern.append((scale[idx], 0.16))

                attack = 0.005
                release = 0.06
                volume = 0.14
                two_pi = 2.0 * math.pi
                samples = array('h')

                for freq, dur in pattern:
                    n = int(dur * sample_rate)
                    step = two_pi * freq / sample_rate
                    phase = 0.0
                    for i in range(n):
                        t = i / sample_rate
                        env = 1.0
                        if t < attack:
                            env = t / attack
                        elif t > (dur - release):
                            env = max(0.0, (dur - t) / release)
                        # Sine + a bit of triangle-like second harmonic via abs(sin)
                        s = math.sin(phase) * 0.8 + (2.0 * abs(math.sin(phase)) - 1.0) * 0.2
                        val = int(max(-1.0, min(1.0, s)) * env * volume * 32767)
                        samples.append(val)
                        phase += step

                    # tiny gap between notes
                    for _ in range(int(0.01 * sample_rate)):
                        samples.append(0)

                return pygame.mixer.Sound(buffer=samples)

            # Menu happy loop
            self.menu_music_sound = generate_happy_menu_music()

            def generate_explosion_sound(sample_rate: int = 44100, duration: float = 0.6) -> pygame.mixer.Sound:
                # Simple explosion: white noise burst + descending sine boom with exponential decay
                total = int(duration * sample_rate)
                samples = array('h')
                rng = random.Random(1337)
                two_pi = 2.0 * math.pi

                # Parameters
                start_freq = 220.0
                end_freq = 55.0
                boom_mix = 0.6  # boom vs noise
                noise_mix = 0.7
                max_amp = 0.9

                for i in range(total):
                    t = i / sample_rate
                    # Exponential decay envelope
                    env = math.exp(-4.0 * t)
                    # Frequency sweep for boom
                    f = end_freq + (start_freq - end_freq) * max(0.0, 1.0 - t / duration)
                    phase = two_pi * f * t
                    boom = math.sin(phase)
                    noise = (rng.random() * 2.0 - 1.0)
                    s = boom * boom_mix + noise * noise_mix
                    val = int(max(-1.0, min(1.0, s)) * env * max_amp * 32767)
                    samples.append(val)

                return pygame.mixer.Sound(buffer=samples)

            self.explosion_sound = generate_explosion_sound()
        except Exception:
            self.music_sound = None
            self.menu_music_sound = None
            self.over_music_sound = None
            self.explosion_sound = None
        finally:
            self.music_playing = False
            
    def start_music(self):
        """Start background music"""
        if self.music_sound and not self.music_playing:
            try:
                self.music_sound.set_volume(0.35)
                self.music_sound.play(loops=-1)
                self.music_playing = True
            except Exception:
                self.music_playing = False

    def start_menu_music(self):
        """Start happy relaxed loop for MENU."""
        try:
            if self.menu_music_sound:
                self.menu_music_sound.set_volume(0.26)
                self.menu_music_sound.play(loops=-1)
        except Exception:
            pass

    def start_over_music(self):
        """Start calm relaxed loop for GAME OVER."""
        try:
            if self.over_music_sound:
                self.over_music_sound.set_volume(0.24)
                self.over_music_sound.play(loops=-1)
        except Exception:
            pass
                
    def stop_music(self):
        """Stop all background music loops (gameplay and relaxed)."""
        try:
            if self.music_sound:
                self.music_sound.stop()
        finally:
            self.music_playing = False
        try:
            if self.menu_music_sound:
                self.menu_music_sound.stop()
        except Exception:
            pass
        try:
            if self.over_music_sound:
                self.over_music_sound.stop()
        except Exception:
            pass

    def play_game_over_sfx(self):
        """Play explosion SFX once on game over."""
        try:
            if self.explosion_sound:
                self.explosion_sound.set_volume(0.6)
                self.explosion_sound.play()
        except Exception:
            pass
        
    def reset_game(self):
        """Reset game to initial state"""
        self.player = Player(100, SCREEN_HEIGHT - 50 - PLAYER_SIZE)
        self.obstacles: List[Obstacle] = []
        self.spawner = Spawner()
        self.score = 0
        self.game_start_time = 0
        self.scroll_speed = BASE_SPEED
        self.last_milestone = 0
        # Reset background to default colors
        self.background.change_colors(LIGHT_BLUE, DARK_BLUE)
        
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
    
    def check_background_milestones(self):
        """Check if score has reached a milestone and change background colors"""
        milestones = [10, 25, 50, 100, 200]
        
        for milestone in milestones:
            if self.score >= milestone and self.last_milestone < milestone:
                self.last_milestone = milestone
                
                if milestone == 10:
                    # Sunset theme
                    self.background.change_colors(SUNSET_SKY, SUNSET_GROUND)
                elif milestone == 25:
                    # Night theme
                    self.background.change_colors(NIGHT_SKY, NIGHT_GROUND)
                elif milestone == 50:
                    # Rainbow theme
                    self.background.change_colors(RAINBOW_SKY, RAINBOW_GROUND)
                elif milestone == 100:
                    # Back to sunset
                    self.background.change_colors(SUNSET_SKY, SUNSET_GROUND)
                elif milestone == 200:
                    # Back to night
                    self.background.change_colors(NIGHT_SKY, NIGHT_GROUND)
                break
    
    def get_funny_phrase(self):
        """Get a funny phrase based on the score"""
        if self.score == 0:
            return "Did you even try? "
        elif self.score < 5:
            return "Better luck next time! "
        elif self.score < 10:
            return "Getting there! Keep practicing! "
        elif self.score < 15:
            return "Not bad! You're improving! "
        elif self.score < 25:
            return "Good job! You're getting the hang of it! "
        elif self.score < 35:
            return "Nice! You're becoming a pro! "
        elif self.score < 50:
            return "Excellent! You're really good at this! "
        elif self.score < 75:
            return "Amazing! You're a geometry master! "
        elif self.score < 100:
            return "Incredible! You're unstoppable! "
        elif self.score < 150:
            return "Legendary! You're a gaming god! "
        elif self.score < 200:
            return "Mind-blowing! You're beyond human! "
        else:
            return "IMPOSSIBLE! You must be cheating! "
            
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
                        # Exit to menu: stop gameplay music, start menu music
                        self.state = GameState.MENU
                        self.stop_music()
                        self.start_menu_music()
                        
                elif self.state == GameState.MENU:
                    if event.key != pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks() / 1000.0
                        self.stop_music()
                        self.start_music()
                        
                elif self.state == GameState.PLAYING:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.player.jump()
                        
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks() / 1000.0
                        self.stop_music()
                        self.start_music()
                        
        return True

    def apply_ros_command(self):
        """Aplica el último comando recibido por ROS al jugador."""
        if self.state != GameState.PLAYING:
            # Solo actuamos en la fase de juego
            return

        if self.last_command is None:
            return

        cmd = self.last_command
        self.last_command = None  # consumimos el comando

        if cmd == "JUMP" or cmd == "UP":
            self.player.jump()
        elif cmd == "DOWN":
            # Podrías activar una caída rápida extra si quieres
            # Por ejemplo, aumentar momentáneamente la velocidad hacia abajo:
            self.player.velocity_y += 200
        elif cmd == "LEFT":
            # Pequeño movimiento horizontal a la izquierda
            self.player.rect.x -= 15
        elif cmd == "RIGHT":
            # Pequeño movimiento horizontal a la derecha
            self.player.rect.x += 15


    def update(self, dt: float):
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return
            
        current_time = pygame.time.get_ticks() / 1000.0
        game_time = current_time - self.game_start_time
        
        # Update difficulty
        base_speed = BASE_SPEED + (game_time * SPEED_INCREMENT)
        self.scroll_speed = min(MAX_SPEED, base_speed * self.speed_multiplier)
        #self.scroll_speed = min(MAX_SPEED, BASE_SPEED + (game_time * SPEED_INCREMENT))
        
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
            self.play_game_over_sfx()
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()


            if self.user_name:
                self.user_scores[self.user_name] = self.score

            self.result_pub.publish(Int64(self.score))
            rospy.loginfo(f"Game Over! Final Score: {self.score}")
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
                
                # Check for background color milestones
                self.check_background_milestones()
                
            # Remove off-screen obstacles
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                
        # Check collisions - only spikes are deadly, platforms are solid barriers
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect) and obstacle.type == "spike":
                # Spikes are deadly
                self.state = GameState.GAME_OVER
                self.stop_music()
                self.play_game_over_sfx()
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()


                if self.user_name:
                    self.user_scores[self.user_name] = self.score

                self.result_pub.publish(Int64(self.score))
                rospy.loginfo(f"Game Over! Final Score: {self.score}")
                break
            # Block platforms are handled in player.update as solid barriers
                
    def draw_menu(self):
        """Draw the welcome/menu screen"""
        # Ensure happy music is playing on menu
        self.start_menu_music()
        # Retro arcade background to match game over style
        self.screen.fill(BLACK)
        
        # Scanlines
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Grid
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(self.screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Pulsing border like game over
        pulse = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.008))
        border_color = (pulse, 0, pulse)
        pygame.draw.rect(self.screen, border_color, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 5)
        
        # Main title with retro big font and shadow
        title_main = self.retro_big_font.render("GEOMETRY DASH", True, NEON_PINK)
        title_shadow = self.retro_big_font.render("GEOMETRY DASH", True, ARCADE_PURPLE)
        shadow_rect = title_main.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 120))
        main_rect = title_main.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_main, main_rect)
        
        # Decorative lines
        pygame.draw.line(self.screen, NEON_CYAN, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 80),
                         (SCREEN_WIDTH // 2 + 220, SCREEN_HEIGHT // 2 - 80), 3)
        pygame.draw.line(self.screen, NEON_CYAN, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 60),
                         (SCREEN_WIDTH // 2 + 220, SCREEN_HEIGHT // 2 - 60), 3)
        
        # Controls block using retro font
        controls_title = self.retro_font.render("CONTROLS", True, NEON_YELLOW)
        self.screen.blit(controls_title, controls_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
        controls = [
            "SPACE/UP: JUMP",
            "DOWN: FAST FALL",
            "ESC: QUIT",
        ]
        for i, text_val in enumerate(controls):
            c_text = self.font.render(text_val, True, NEON_BLUE)
            self.screen.blit(c_text, c_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10 + i * 32)))
        
        if self.user_name:
            name_text = self.font.render(f"PLAYER: {self.user_name}", True, NEON_GREEN)
            self.screen.blit(name_text, name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))

        # Start prompt with pulsing neon
        pulse2 = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
        start_color = (pulse2, pulse2, 255)
        start_text = self.retro_font.render("PRESS ANY KEY TO START", True, start_color)
        self.screen.blit(start_text, start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120)))
        
        # High score (if any)
        if self.high_score > 0:
            hs_text = self.retro_font.render(f"HIGH SCORE: {self.high_score:04d}", True, ARCADE_CYAN)
            self.screen.blit(hs_text, hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160)))
        
        # Retro corner decorations
        corner_size = 30
        pygame.draw.line(self.screen, NEON_GREEN, (50, 50), (50 + corner_size, 50), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (50, 50), (50, 50 + corner_size), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (SCREEN_WIDTH - 50, 50), (SCREEN_WIDTH - 50 - corner_size, 50), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (SCREEN_WIDTH - 50, 50), (SCREEN_WIDTH - 50, 50 + corner_size), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (50, SCREEN_HEIGHT - 50), (50 + corner_size, SCREEN_HEIGHT - 50), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (50, SCREEN_HEIGHT - 50), (50, SCREEN_HEIGHT - 50 - corner_size), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), (SCREEN_WIDTH - 50 - corner_size, SCREEN_HEIGHT - 50), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50 - corner_size), 3)
            
    def draw_game_over(self):
        """Draw the retro arcade style game over screen"""
        # Ensure calm relaxed music is playing on game over
        self.start_over_music()
        # Retro arcade background with scanlines effect
        self.screen.fill(BLACK)
        
        # Add scanlines effect
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Add some retro grid pattern
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(self.screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Pulsing border effect
        pulse = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.008))
        border_color = (pulse, 0, pulse)
        pygame.draw.rect(self.screen, border_color, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 5)
        
        # Main "GAME OVER" text with retro styling
        game_over_text = self.retro_big_font.render("GAME OVER", True, ARCADE_RED)
        game_over_shadow = self.retro_big_font.render("GAME OVER", True, NEON_PINK)
        
        # Add shadow effect
        shadow_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 120))
        main_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        
        self.screen.blit(game_over_shadow, shadow_rect)
        self.screen.blit(game_over_text, main_rect)
        
        # Add decorative lines
        pygame.draw.line(self.screen, NEON_CYAN, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 80), 
                        (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 80), 3)
        pygame.draw.line(self.screen, NEON_CYAN, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 60), 
                        (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 60), 3)
        
        # Final score with retro styling
        score_text = self.retro_font.render(f"FINAL SCORE: {self.score:04d}", True, NEON_GREEN)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        # Funny phrase with retro colors
        funny_phrase = self.get_funny_phrase()
        phrase_color = NEON_YELLOW if self.score >= 50 else NEON_ORANGE if self.score >= 25 else NEON_BLUE
        phrase_text = self.font.render(funny_phrase, True, phrase_color)
        phrase_rect = phrase_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(phrase_text, phrase_rect)
        
        # High score section with retro styling
        if self.score == self.high_score and self.score > 0:
            # Blinking effect for new high score
            blink = int(255 * abs(math.sin(pygame.time.get_ticks() * 0.01)))
            new_high_text = self.retro_font.render("*** NEW HIGH SCORE! ***", True, (blink, 255, blink))
            new_high_rect = new_high_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(new_high_text, new_high_rect)
        else:
            hs_text = self.retro_font.render(f"HIGH SCORE: {self.high_score:04d}", True, ARCADE_PURPLE)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(hs_text, hs_rect)
        
        # Add more decorative lines
        pygame.draw.line(self.screen, NEON_CYAN, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100), 
                        (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 100), 3)
        pygame.draw.line(self.screen, NEON_CYAN, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 120), 
                        (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 120), 3)
            
        # Retro arcade style options
        options = [
            "PRESS [R] TO RETRY",
            "PRESS [ESC] TO QUIT"
        ]
        
        y_offset = SCREEN_HEIGHT // 2 + 150
        for i, option in enumerate(options):
            # Pulsing effect for options
            pulse = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.005 + i))
            option_color = (pulse, pulse, 255)
            text = self.retro_font.render(option, True, option_color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 50))
            self.screen.blit(text, text_rect)
        
        # Add some retro corner decorations
        corner_size = 30
        # Top-left corner
        pygame.draw.line(self.screen, NEON_GREEN, (50, 50), (50 + corner_size, 50), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (50, 50), (50, 50 + corner_size), 3)
        # Top-right corner
        pygame.draw.line(self.screen, NEON_GREEN, (SCREEN_WIDTH - 50, 50), (SCREEN_WIDTH - 50 - corner_size, 50), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (SCREEN_WIDTH - 50, 50), (SCREEN_WIDTH - 50, 50 + corner_size), 3)
        # Bottom-left corner
        pygame.draw.line(self.screen, NEON_GREEN, (50, SCREEN_HEIGHT - 50), (50 + corner_size, SCREEN_HEIGHT - 50), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (50, SCREEN_HEIGHT - 50), (50, SCREEN_HEIGHT - 50 - corner_size), 3)
        # Bottom-right corner
        pygame.draw.line(self.screen, NEON_GREEN, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), (SCREEN_WIDTH - 50 - corner_size, SCREEN_HEIGHT - 50), 3)
        pygame.draw.line(self.screen, NEON_GREEN, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50 - corner_size), 3)
            
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
        
    def welcome_phase(self) -> bool:
        """Fase 1: Welcome - mostrar pantalla de menú y esperar a empezar el juego."""
        rospy.loginfo("[GAME_NODE] Welcome phase started.")
        # Aquí más adelante leerás el user_msg de ROS y mostrarás el nombre

        self.state = GameState.MENU
        running = True

        while running and self.state == GameState.MENU:
            dt = self.clock.tick(FPS) / 1000.0

            # Eventos (ESC para salir, cualquier tecla para empezar)
            running = self.handle_events()
            if not running:
                break

            # En MENU, update() realmente no hace nada (sale tempranamente)
            self.update(dt)
            self.draw()

            # Cuando en handle_events se pulse una tecla, pasas a PLAYING
            # y este while terminará porque self.state ya no será MENU

        return running

    def game_phase(self) -> bool:
        """Fase 2: Game - juego en marcha, controlado por las teclas (luego ROS)."""
        rospy.loginfo("[GAME_NODE] Game phase started.")

        # Aseguramos que el estado es PLAYING
        self.state = GameState.PLAYING
        running = True

        while running and self.state == GameState.PLAYING and not rospy.is_shutdown():
            dt = self.clock.tick(FPS) / 1000.0

            running = self.handle_events()
            if not running:
                break

            self.apply_ros_command()  # Aplica comandos recibidos por ROS


            self.update(dt)   # Física, colisiones, score, etc.
            self.draw()       # Fondo, jugador, obstáculos, HUD...

            # Cuando el jugador muere, en update() pasas a GAME_OVER,
            # así que el while terminará porque self.state != PLAYING

        return running

    def final_phase(self) -> bool:
        """Fase 3: Final - mostrar pantalla de GAME OVER y calcular/publicar score."""
        rospy.loginfo("[GAME_NODE] Final phase reached, calculating score.")
        # Aquí más adelante publicarás el score por ROS en 'result_information'

        # Aseguramos que estamos en GAME_OVER
        self.state = GameState.GAME_OVER
        running = True

        while running and self.state == GameState.GAME_OVER:
            dt = self.clock.tick(FPS) / 1000.0

            running = self.handle_events()
            if not running:
                break

            # En GAME_OVER no actualizas la lógica del juego, solo dibujas la pantalla final
            self.draw()

            # Si en GAME_OVER el jugador pulsa R, tu handle_events ya pone:
            #   reset_game()
            #   self.state = GameState.PLAYING
            # Esto hará que el while termine porque el estado deja de ser GAME_OVER.

        # Aquí es un buen sitio para hacer algo con self.score si lo necesitas
        return running

    def user_info_callback(self, msg: user_msg):
        """Recibe name, username y age desde INFO_USER."""
        self.user_name = msg.name
        self.user_username = msg.username
        self.user_age = msg.age
        rospy.loginfo(
            "GAME_NODE: Received user info: name=%s, username=%s, age=%d",
            self.user_name, self.user_username, self.user_age
        )

    def key_callback(self, msg: String):
        """Recibe comandos de movimiento desde CONTROL_NODE."""
        self.last_command = msg.data.upper()
        rospy.loginfo("GAME_NODE: Received keyboard command: %s", self.last_command)

    def handle_user_score(self, req: GetUserScore) -> GetUserScoreResponse:
        """
        Servicio 'user_score':
        - req.name: nombre del usuario
        - devuelve: porcentaje de su score respecto al máximo registrado.
        """
        name = req.username

        # Score del usuario (0 si nunca ha jugado o nunca ha muerto)
        score = self.user_scores.get(name, 0)

        # Máximo score de todos los usuarios registrados
        if self.user_scores:
            max_score = max(self.user_scores.values())
        else:
            max_score = 0

        if max_score <= 0:
            percentage = 0.0
        else:
            percentage = 100.0 * float(score) / float(max_score)

        rospy.loginfo(
            "SERVICE user_score: name=%s, score=%d, percentage=%.2f",
            name, score, percentage
        )

        return GetUserScoreResponse(score=int(percentage))

    def handle_set_difficulty(self, req: SetGameDifficulty) -> SetGameDifficultyResponse:
        """
        Servicio 'difficulty':
        - req.level: 'easy', 'medium' o 'hard'
        - Solo permite cambiar si estamos en fase de menú (por ejemplo GameState.MENU)
        """
        level = req.change_difficulty.lower()

        # Aquí puedes comprobar tu estado de juego; por ejemplo:
        if self.state != GameState.MENU:
            rospy.loginfo("SERVICE difficulty: no estamos en fase 1, rechazado.")
            return SetGameDifficultyResponse(success=False)

        if level not in ("easy", "medium", "hard"):
            rospy.logwarn("SERVICE difficulty: invalid level '%s'", level)
            return SetGameDifficultyResponse(success=False)

        self.current_difficulty = level
        self.apply_difficulty_settings()

        rospy.loginfo("SERVICE difficulty: difficulty changed to '%s'", level)

        return SetGameDifficultyResponse(success=True)


    def apply_difficulty_settings(self):
        """Ajusta parámetros del juego según la dificultad actual."""
        if self.current_difficulty == "easy":
            self.speed_multiplier = 0.8
        elif self.current_difficulty == "medium":
            self.speed_multiplier = 1.0
        elif self.current_difficulty == "hard":
            self.speed_multiplier = 1.2
        else:
            # Por si acaso llega algo raro
            self.speed_multiplier = 1.0


    def run(self):
        """Bucle principal del nodo GAME_NODE organizado en 3 fases."""
        running = True

        while running:
            # ----- Fase 1: Welcome -----
            running = self.welcome_phase()
            if not running:
                break  # salir del juego

            # ----- Fase 2: Game -----
            running = self.game_phase()
            if not running:
                break

            # ----- Fase 3: Final -----
            running = self.final_phase()
            if not running:
                break

            # Cuando salimos de la fase final, reseteamos el juego
            # y volvemos a empezar desde la fase de Welcome
            self.reset_game()

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