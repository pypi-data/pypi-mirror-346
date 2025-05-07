from typing import Any, Callable, Optional
import pygame
import pygame.freetype as ft
import websockets
import sys
import asyncio
import json
import random
import logging
import os

class Entity:
    def __init__(self, width: int, height: int, screen_width: int, screen_height: int, id: int=-1):
        """Set up Entity variables and set up a Pygame Surface for the entity.

    
        Args:
            width (int): The width of the player surface.
            height (int): The height of the player surface.
            screen_width (int): The width of the Pygame screen.
            screen_height (int): The height of them Pygame screen.
            state (dict): The state of the player containing fields and values.
            id (int, optional): The server id of the player. Defaults to -1.
        """

        self.width = width
        self.height = height
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height // 2 - self.height // 2
        self._assets = "./client/assets/"
        self._logger = logging.getLogger(f"cotb_client[{id}]")
        self._id = id

        self.is_transitioning = False
        self._transition_progress = 0
        self._last_move_time = 0

        self._surface = pygame.Surface((self.width, self.height))

    def _create_surface(self, path: str):
        """Creates a Pygame Surface with the entity's dimensions and sprite if any.
       
        Arguments:
            path (str): The path to the sprite of the entity.

        Returns:
            pygame.Surface: The created surface for the entity.
        """
        surface = pygame.Surface((self.width, self.height))
        try:
            img = pygame.image.load(path)
            resized_img = pygame.transform.scale(img, (self.width, self.height))
            surface.blit(resized_img, (0,0))
            surface.set_colorkey((0, 0, 0))
        except FileNotFoundError:
            surface.fill((random.randint(0,256), random.randint(0,256), random.randint(0,256)))
        
        return surface

    def _get_sprite(self, name):
        """Gets the path of the sprite for the entity.
       
        Arguments:
            name (str): The name of the sprite.

        Returns:
            str: The path to the image. Empty str if no path is found.
        """
        file_path = f"{self._assets}{name}.png"
        if (os.path.exists(file_path)):
            return file_path
        else:
            self._logger.error(f"File path not found: {file_path}")
            return ""

    def render(self, screen: pygame.Surface):
        """Renders the entity's surface on the given screen.
        
        Args:
            screen (pygame.Surface): The screen to render the entity on.
        """
        screen.blit(self._surface, (int(self.x), int(self.y)))

    def update_position(self, x: float, y: float):
        """Updates the entity's position coordinates.
        
        Args:
            x (float): The new x-coordinate.
            y (float): The new y-coordinate.
        """
        self.x = x
        self.y = y

    def get_id(self):
        """Gets the entity's ID.
        
        Returns:
            int: The entity's ID.
        """
        return self._id

    def start_transition(self, target_x, target_y, other_entites=None, screen_width=None, screen_height=None):
        """
        Starts a transition to a new position with collision prevention.
        
        Args:
            target_x (float): The target x-coordinate.
            target_y (float): The target y-coordinate.
            other_entites (dict, optional): Dictionary of other entites of this type in the game.
            screen_width (int, optional): Width of the game screen.
            screen_height (int, optional): Height of the game screen.
        """

        if screen_width is not None and screen_height is not None:
            margin_x = screen_width * 0.05
            margin_y = screen_height * 0.05
        
            target_x = max(margin_x, min(screen_width - margin_x - self.width, target_x))
            target_y = max(margin_y, min(screen_height - margin_y - self.height, target_y))

        target_x, target_y = self._check_collision(target_x, target_y, other_entites, screen_width, screen_height)

        # Check if the target position is different from the current position
        if (abs(target_x - self.x) < 1e-6 and abs(target_y - self.y) < 1e-6):
            return 

        current_time = pygame.time.get_ticks()
        
        # Check if we can start a new transition
        if not self.is_transitioning:
            # Reset transition start point
            self._start_x = self.x
            self._start_y = self.y
            
            # Set transition parameters
            self.is_transitioning = True
            self._transition_progress = 0
            self._target_x = target_x
            self._target_y = target_y
            self._last_move_time = current_time

    def _check_collision(self, target_x, target_y, other_entites, screen_width=None, screen_height=None) -> tuple:
        """
        Checks if target position collides with other entites and finds alternative position.
    
        Args:
            target_x (float): The target x-coordinate.
            target_y (float): The target y-coordinate.
            other_entites (dict): Dictionary of other entites of this type in the game.
            screen_width (int, optional): Width of the game screen.
            screen_height (int, optional): Height of the game screen.
        
        Returns:
            tuple: Modified (x, y) position that avoids collisions
        """
        # Skip collision check if no other players
        if not other_entites:
            return target_x, target_y
        
        # Calculate margins if screen dimensions provided
        if screen_width is not None and screen_height is not None:
            margin_x = screen_width * 0.05
            margin_y = screen_height * 0.05
            min_x = margin_x
            max_x = screen_width - margin_x - self.width
            min_y = margin_y
            max_y = screen_height - margin_y - self.height
        else:
            # Default values if screen dimensions not provided
            min_x = float('-inf')
            max_x = float('inf')
            min_y = float('-inf')
            max_y = float('inf')

        # If n == -1, this is the main player, so we will not change their position,
        # Else, this is another entity, so we mod by 4 because we can have 4 players
        # Or 4 enemies. This ensure no entity overlaping.
        # If there is more than 4 entites, then overlap will exists.
        n = self.get_id()
        if not (n == -1): n %= 4

        match (n):
            case 0:
                tmp = target_x
                target_x = min(max_x, target_x + self.width)
                if (target_x == max_x):
                    target_x = tmp - self.width
                    target_y -= self.height
            case 1:
                tmp = target_x
                target_x = max(min_x, target_x - self.width)
                if (target_x == min_x):
                    target_x = tmp + self.width
                    target_y += self.height
            case 2:
                tmp = target_y
                target_y = min(max_y, target_y + self.height)
                if (target_y == max_y):
                    target_y = tmp - self.height
                    target_x -= self.width
            case 3:
                tmp = target_y
                target_y = max(min_y, target_y - self.height)
                if (target_y == min_y):
                    target_y = tmp + self.height
                    target_x += self.width
            case _:
                # The main player will always be in the spot they choose
                pass

        return target_x, target_y

    def _ease_in_out_quad(self, t: float):
        """Easing function for smooth transitions.
        
        Args:
            t (float): The transition progress from 0.0 to 1.0.

        Returns:
            float: The eased value.
        """
        return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2

    def update_transition(self):
        """Updates the position during a transition animation.
        
        Increments transition progress and calculates new position using easing function.
        Sets final position when transition completes.
        """
        if self.is_transitioning:
            self._transition_progress += 1 / 14
            if self._transition_progress >= 1:
                self.update_position(self._target_x, self._target_y)
                self.is_transitioning = False
            else:
                t = self._ease_in_out_quad(self._transition_progress)
                new_x = self._start_x + (self._target_x - self._start_x) * t
                new_y = self._start_y + (self._target_y - self._start_y) * t
                self.update_position(new_x, new_y)

    def update(self):
        """Updates transition states of the entity.
        
        This method should be called once per frame in the game loop.
        """
        self.update_transition()

    def get_surface_copy(self) -> pygame.Surface:
        """Gets a copy of the entity's surface

        Returns:
            pygame.Surface: A copy of the current suface
        """
        return self._surface.copy()

class Player(Entity):
    def __init__(self, width: int, height: int, screen_width: int, screen_height: int, state: dict[Any, Any], id: int=-1):
        """Set up Player class variables and set up a Pygame Surface for the player.

    
        Args:
            width (int): The width of the player surface.
            height (int): The height of the player surface.
            screen_width (int): The width of the Pygame screen.
            screen_height (int): The height of them Pygame screen.
            state (dict): The state of the player containing fields and values.
            id (int, optional): The server id of the player. Defaults to -1.
        """

        super().__init__(width, height, screen_width, screen_height, id)

        classes = [
            "mage",
            "cleric",
            "tank",
            "range"
        ]

        self._state = state
        self._target = -1
        if not ("health" in state):
            self.starting_health = -1
        else:
            self.starting_health = state["health"]

        # If a class doesn't exists, then pick one at random
        if not ("class" in state) or (self._state["class"] in classes):
            self._state["class"] = classes[random.randint(0, len(classes) - 1)]

        self._surface = self._create_surface(self._get_sprite(self._state["class"]))

    def get_target(self) -> int:
        return self._target

    def _convert_keys(self, state: dict[Any, Any]):
        """Converts string keys to appropriate types in the state dictionary.
        
        Args:
            state (dict): The state dictionary with string keys.
            
        Returns:
            dict: A new dictionary with converted keys (int for digits, bool for "true"/"false").
        """
        new_dict = {}
        for key, value in state.items():
            if key.isdigit():
                new_dict[int(key)] = value
            elif key in ("true", "false"):  
                new_dict[key == "true"] = value
            else:
                new_dict[key] = value
        return new_dict

    def get_state(self):
        """Gets the player's current state.
        
        Returns:
            dict: The player's state dictionary.
        """
        return self._state

    def update_state(self, state: dict[Any, Any], isServerUpdate: bool=False):
        """Updates the player's state with new values.
        
        Args:
            state (dict): The new state to update with.
            other_players (dict, optional): Dictionary of other players. Defaults to {}.
            isServerUpdate (bool, optional): If this update is a server update, ensure keys are the same.
        """

        # Add sprite if one does not exists yet
        if ("class" in state) and ("class" in self._state) and (state["class"] != self._state["class"]):

            self._surface = self._create_surface(self._get_sprite(state["class"]))

        # Add starting health if starting health is unknow
        if ("health" in state) and (self.starting_health == -1):

            self.starting_health = state["health"]

        self._state.update(self._convert_keys(state))

        if isServerUpdate:
            set_of_states = set(self._state.keys())
            for key in set_of_states:
                if not (key in state.keys()):
                    del self._state[key]

    def find_target(self, enemies: dict, mouse_pos: tuple):
        """Checks if an enemy collides with the mouse and if one does,
        Set the current target of this player to the id of the enemy.

        Args:
            enemies (dict): A dictonary of the enemies in the game.
            mouse_pos (tuple(int, int)): The current position of the mouse.
        """
        if (len(enemies) == 0):
            self._target = -1
        elif (len(enemies) == 1) or (mouse_pos == (0,0)):
            self._target = next(iter(enemies.keys())) 
        else:
            for e in enemies:
                enemy_rect = enemies[e].get_surface().get_rect()
        
                # Move the rect to where the enemy is actually positioned on screen
                enemy_rect.topleft = (enemies[e].x, enemies[e].y)
        
                if enemy_rect.collidepoint(mouse_pos):
                    self._target = e
                    return

    def render_name(self, screen: pygame.Surface, font_size: int=14, opacity: int=64, y_offset: int=10):
        """Renders a username with white text on a semi-transparent black background
        positioned above a the player.
        
        Args:
            screen (pygame.Surface): The main pygame surface to render on
            font_size (int): Size of the font
            opacity (int): Opacity of the background (0-255, where 0 is invisible)
            y_offset (int): Distance above the surface to place the username
        """
        # Initialize font if not already done
        if not ft.was_init():
            ft.init()
        
        # Create font object
        font = ft.SysFont('Arial', font_size)
        
        # Get text
        if ("username" in self._state):
            name = self._state["username"]
        else:
            name = "Player"

        if (self._id == -1):
            name = "You"

        text_surface, text_rect = font.render(name, (255, 255, 255))
        
        # Create semi-transparent background
        background = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
        background.set_alpha(opacity)  # Set transparency (0-255)
        background.fill((0, 0, 0))     # Black color
        
        # Calculate position for the username
        # Center horizontally above the surface
        x_pos = self.x + (self._surface.get_width() - background.get_width()) // 2
        # Position above the surface with the specified offset
        y_pos = self.y - background.get_height() - y_offset
        
        # Position the elements
        background_pos = (x_pos, y_pos)
        text_pos = (x_pos + 10, y_pos + 5)
        
        # Blit the background and then the text
        screen.blit(background, background_pos)
        screen.blit(text_surface, text_pos)

    def __str__(self):
        """Returns a string representation of the player.
        
        Returns:
            str: A string showing the player's ID and state.
        """
        return f"{self._id}: {self._state}"


class Enemy(Entity):
    def __init__(self, id: int, room_id: int, screen_width: int, screen_height: int, type_of_enemy: str, health: int, attack: int, defense: int, abilities: list[str], is_boss: bool):
        """Initialize an Enemy instance.
        
        Args:
            id: A unique identifier for the enemy.
            room_id: The identifier of the room where the enemy is located.
            type_of_enemy: The category or type of the enemy.
            health: The initial health points of the enemy.
            attack: The attack power of the enemy.
            defense: The defense power of the enemy.
            abilities: A list of abilities the enemy can use.
            is_boss: Boolean indicating if the enemy is a boss.
        """


        super().__init__(100, 100, screen_width, screen_height, id)

        enemy_types = [
            "mechape",
            "goblin"
        ]

        self.room_id = room_id
        self.type_of_enemy = type_of_enemy
        self._start_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.abilities = abilities
        self.is_boss = is_boss

        # If an enemy type doesn't exists, then pick one at random
        if not (self.type_of_enemy in enemy_types):
            self.type_of_enemy = enemy_types[random.randint(0, len(enemy_types) - 1)]

        self._surface = self._create_surface(self._get_sprite(self.type_of_enemy))

    def get_surface(self):
        """Gets the enemy's surface

        Returns:
            pygame.Surface: The enemy's surface
        """
        return self._surface

    def render_target(self, screen: pygame.Surface, icon_size: int=20, y_offset: int=10, color: tuple=(255, 0, 0)):
        """Renders a red target icon above the enemy.
        
        Args:
            screen (pygame.Surface): The pygame surface to render on
            icon_size: Size of the target icon (width and height)
            y_offset: Distance above the enemy to place the icon
            color: RGB color tuple for the icon (default: red)
        """
        
        # Calculate position for target icon (centered above the enemy)
        icon_x = self.x + (self._surface.get_width() - icon_size) // 2
        icon_y = self.y - icon_size - y_offset
        
        # Draw the target icon (a simple red circle with a crosshair)
        # Outer circle
        pygame.draw.circle(screen, color, (icon_x + icon_size//2, icon_y + icon_size//2), 
                          icon_size//2, 2)
        
        # Horizontal line
        pygame.draw.line(screen, color, 
                        (icon_x + icon_size//4, icon_y + icon_size//2), 
                        (icon_x + 3*icon_size//4, icon_y + icon_size//2), 2)
        
        # Vertical line
        pygame.draw.line(screen, color, 
                        (icon_x + icon_size//2, icon_y + icon_size//4), 
                        (icon_x + icon_size//2, icon_y + 3*icon_size//4), 2)

    def _render_health(self, screen: pygame.Surface):
        """Renders the enemy's health to a given surface.

        Args:
            screen (pygame.Surface): The surface to render the health to.
        """

        bar = pygame.Surface((self.width, self.height * 0.10))
        bar_x = self.x
        bar_y = int(self.y + self.height)
        health_on_bar = int((self.health / self._start_health) * bar.get_width())

        bar.fill((255,0,0)) # Fill red
        bar.fill((0,255,0), rect=(0, 0, health_on_bar, bar.get_height())) # Add green

        screen.blit(bar, (bar_x, bar_y))


    def render(self, screen: pygame.Surface):
        """Renders the enemy's surface on the given screen, and health bar.
        
        Args:
            screen (pygame.Surface): The screen to render the enemy on.
        """
        super().render(screen)
        self._render_health(screen)
    
class ActionBar:
    """A bar with clickable buttons displayed at the bottom of the screen.
    
    This class handles rendering and interaction with a set of buttons
    displayed in a bar at the bottom of the game screen. The bar can be
    enabled or disabled to control its visibility.
    """
    
    def __init__(self, screen_width: int, screen_height: int, button_count: int = 4, enabled: bool = True):
        """Initialize the action bar with buttons.
        
        Args:
            screen_width (int): Width of the game screen.
            screen_height (int): Height of the game screen.
            button_count (int, optional): Number of buttons to display. Defaults to 4.
            enabled (bool, optional): Whether the bar is initially enabled. Defaults to True.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.button_count = button_count
        self.enabled = enabled
        
        # Bar dimensions and position
        self.bar_height = 80
        self.bar_width = screen_width
        self.bar_y = screen_height - self.bar_height
        
        # Button dimensions
        self.button_width = 200 
        self.button_height = self.bar_height - 15 
        self.button_padding = 20
        self.buttons: list[dict] = []
        
        # Calculate positions to evenly space buttons
        total_buttons_width = button_count * self.button_width + (button_count - 1) * self.button_padding
        start_x = (screen_width - total_buttons_width) // 2
        
        # Create button objects
        for i in range(button_count):
            x = start_x + i * (self.button_width + self.button_padding)
            y = self.bar_y + (self.bar_height - self.button_height) // 2
            self.buttons.append({
                'rect': pygame.Rect(x, y, self.button_width, self.button_height),
                'color': (180, 180, 180),
                'hover_color': (220, 220, 220),
                'pressed_color': (150, 150, 150),
                'text': f"BTN {i+1}",
                'action': None,
                'state': 'normal',  # normal, hover, pressed
                'icon': None
            })
        
        # Font for button text
        self.font = pygame.font.SysFont('Arial', 18)
        
        # Sounds (can be set later)
        self.click_sound = None
        self.hover_sound = None
        
        self._logger = logging.getLogger("action_bar")
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the action bar.
        
        When disabled, the bar will not be rendered and will not process events.
        
        Args:
            enabled (bool): Whether the action bar should be enabled.
        """
        self.enabled = enabled
        
        # Reset button states when disabling
        if not enabled:
            for button in self.buttons:
                button['state'] = 'normal'
    
    def is_enabled(self) -> bool:
        """Check if the action bar is currently enabled.
        
        Returns:
            bool: True if enabled, False otherwise.
        """
        return self.enabled
    
    def set_button_properties(self, button_index: int, **properties):
        """Set properties for a specific button.
        
        Args:
            button_index (int): Index of the button to modify (0-based).
            **properties: Keyword arguments for properties to set.
                Possible properties:
                - text (str): Text to display on the button
                - color (tuple): RGB color for normal state
                - hover_color (tuple): RGB color for hover state
                - pressed_color (tuple): RGB color for pressed state
                - action (callable): Function to call when button is clicked
                - icon (pygame.Surface): Icon to display on the button
        
        Raises:
            IndexError: If button_index is out of range.
        """
        if not 0 <= button_index < self.button_count:
            raise IndexError(f"Button index {button_index} out of range (0-{self.button_count-1})")
        
        button = self.buttons[button_index]
        for key, value in properties.items():
            if key in button:
                button[key] = value
            else:
                self._logger.warning(f"Unknown button property: {key}")
    
    def set_button_action(self, button_index: int, action: Callable[[], None]) -> None:
        """Set the action callback for a button.
        
        Args:
            button_index (int): Index of the button (0-based).
            action (callable): Function to call when button is clicked.
        
        Raises:
            IndexError: If button_index is out of range.
        """
        if not 0 <= button_index < self.button_count:
            raise IndexError(f"Button index {button_index} out of range (0-{self.button_count-1})")
            
        self.buttons[button_index]['action'] = action
    
    def set_sounds(self, click_sound_path: Optional[str] = None, hover_sound_path: Optional[str] = None) -> None:
        """Set sound effects for button interactions.
        
        Args:
            click_sound_path (str, optional): Path to sound file for click events.
            hover_sound_path (str, optional): Path to sound file for hover events.
        """
        if click_sound_path:
            try:
                self.click_sound = pygame.mixer.Sound(click_sound_path)
            except:
                self._logger.error(f"Failed to load click sound: {click_sound_path}")
        
        if hover_sound_path:
            try:
                self.hover_sound = pygame.mixer.Sound(hover_sound_path)
            except:
                self._logger.error(f"Failed to load hover sound: {hover_sound_path}")
    
    def handle_event(self, event) -> bool:
        """Handle mouse events for button interaction.
        
        Args:
            event: Pygame event to process.
            
        Returns:
            bool: True if the event was handled by a button, False otherwise.
        """
        # Skip event handling if disabled
        if not self.enabled:
            return False
            
        mouse_pos = pygame.mouse.get_pos()
        
        # Track which button is being hovered
        for button in self.buttons:
            was_hovering = button['state'] == 'hover'
            is_hovering = button['rect'].collidepoint(mouse_pos)
            
            # Handle mouse movements (for hover effects)
            if event.type == pygame.MOUSEMOTION:
                if is_hovering and button['state'] != 'pressed':
                    button['state'] = 'hover'
                    # Play hover sound when first hovering
                    if not was_hovering and self.hover_sound:
                        self.hover_sound.play()
                elif not is_hovering and button['state'] != 'pressed':
                    button['state'] = 'normal'
            
            # Handle mouse button down
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if is_hovering:
                    button['state'] = 'pressed'
                    if self.click_sound:
                        self.click_sound.play()
                    return True
            
            # Handle mouse button up
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if button['state'] == 'pressed':
                    button['state'] = 'hover' if is_hovering else 'normal'
                    if is_hovering and button['action']:
                        button['action']()
                    return True
                    
        return False
    
    def update(self) -> None:
        """Update button states based on mouse position.
        
        This should be called each frame to update hover effects without events.
        Skip updating if the action bar is disabled.
        """
        if not self.enabled:
            return
            
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            if button['state'] != 'pressed':
                if button['rect'].collidepoint(mouse_pos):
                    button['state'] = 'hover'
                else:
                    button['state'] = 'normal'
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the action bar and its buttons to the screen if enabled.
        
        Args:
            screen (pygame.Surface): The screen surface to render on.
        """
        # Skip rendering if disabled
        if not self.enabled:
            return
            
        # Draw the bar background
        pygame.draw.rect(screen, (50, 50, 60), (0, self.bar_y, self.bar_width, self.bar_height))
        pygame.draw.line(screen, (80, 80, 90), (0, self.bar_y), (self.bar_width, self.bar_y), 2)
        
        # Draw each button
        for button in self.buttons:
            # Determine color based on state
            if button['state'] == 'normal':
                color = button['color']
            elif button['state'] == 'hover':
                color = button['hover_color']
            else:  # pressed
                color = button['pressed_color']
            
            # Draw button background
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, (30, 30, 40), button['rect'], 2)  # border
            
            # Draw button content (icon or text)
            if button['icon']:
                # Center the icon in the button
                icon_rect = button['icon'].get_rect(center=button['rect'].center)
                screen.blit(button['icon'], icon_rect)
            elif button['text']:
                # Render and center the text
                text_surf = self.font.render(button['text'], True, (30, 30, 40))
                text_rect = text_surf.get_rect(center=button['rect'].center)
                screen.blit(text_surf, text_rect)

class PlayerList:

    def __init__(self, main_player: Player, other_players: dict[int, Player]):
        """Setup the player list

        Args:
            main_player (Player): The main player of the game.
            other_players (dict): All other players connected.

        """
        self._player = main_player
        self._other_players = other_players
        self._player_margin = 15
        self._player_bar_margin = 5

    def _get_health_bar(self, player: Player, screen: pygame.Surface) -> pygame.Surface:
        """Gets a surface for the player's health bar

        Args:
            player (Player): The current player's health bar to make.
            screen (pygame.Surface): The screen to size up the bar to.

        Returns:
            pygame.Surface: The health bar of the current player.
        """

        bar = pygame.Surface((screen.get_width() * .20, 14))
        health = player.get_state().get("health", 0)
        health_on_bar = int((health / player.starting_health) * bar.get_width())

        bar.fill((255,0,0)) # Fill red
        bar.fill((0,255,0), rect=(0, 0, health_on_bar, bar.get_height())) # Add green

        return bar


    def render(self, screen: pygame.Surface, font_size: int=14) -> tuple[int, int]:
        """Renders the list of players to a given screen.

        The list of players contains all the players followed by their health.

        Args:
            screen (pygame.Surface): The surface to render the list to
        """
        # Initialize font if not already done
        if not ft.was_init():
            ft.init()
        
        # Create font object
        font = ft.SysFont('Arial', font_size)

        # Get the names of the players
        main_player_name, main_player_name_rect = font.render("You", (255, 255, 255))
        other_names = []
        for p in self._other_players.values():
            other_names.append(font.render(p.get_state().get("username",f"Player {p.get_id}"), (255, 255, 255)))

        # Get the health bars of the players
        main_player_bar = self._get_health_bar(self._player, screen)
        other_health_bars = []
        for p in self._other_players.values():
            other_health_bars.append(self._get_health_bar(p, screen))

        # TODO: Ensure names do not overflow list width
        list_height = main_player_name.get_height() + main_player_bar.get_height()
        list_width = main_player_bar.get_width()

        # Add other players to height
        for i in range(len(self._other_players)):
            list_height += self._player_margin
            list_height += other_names[i][0].get_height()
            list_height += other_health_bars[i].get_height()

        player_list_bg = pygame.Surface((list_width, list_height))
        player_list_bg.set_alpha(64)  # Set transparency (0-255)
        player_list_bg.fill((0, 0, 0))     # Black color

        screen_x = screen.get_width() - list_width
        screen_y = 0 
        screen.blit(player_list_bg, (screen_x, screen_y))

        # Add main player to list
        screen.blit(main_player_name, (screen_x, screen_y))
        screen_y += main_player_name.get_height() + self._player_bar_margin
        screen.blit(main_player_bar, (screen_x, screen_y))
        screen_y += main_player_bar.get_height()

        # Add other players if any
        for i in range(len(self._other_players)):
            screen_y += self._player_margin

            screen.blit(other_names[i][0], (screen_x, screen_y))
            screen_y += other_names[i][0].get_height() + self._player_bar_margin
            screen.blit(other_health_bars[i], (screen_x, screen_y))
            screen_y += other_health_bars[i].get_height()

        return screen_x, screen_y

class TurnBar:
    def __init__(self, main_player: Player, other_players: dict[int, Player], enemies: dict[int, Enemy]):
        """Sets up the Turn Bar by adding needed references.

        Aegs:
            main_player (Player): The main player of the game.
            other_players (dict): A dictonary of other players in the game.
            enemies (dict): A dictonary of enemies in the current room.
        """
        self._player = main_player
        self._other_players = other_players
        self._enemies = enemies
        self._turns = []
        self._num_of_turns = -1
        self._turns_str = []

    def _scale_sprite(self, sprite: pygame.Surface, screen: pygame.Surface, start_x: int) -> pygame.Surface:
        """Scales a sprite based on the screen size and the starting point of the turn bar.

        Args:
            sprite (pygame.Surface): The surface to scale.
            screen (pygame.Surface): The screen to use to do the scaling.
            start_x (int): The starting point of the turn bar.

        Returns:
            pygame.Surface: The newly scaled surface.
        """
        width = screen.get_width() - start_x
        width_per_entity = width // self._num_of_turns
        height_per_entity = width_per_entity
        return pygame.transform.scale(sprite, (width_per_entity, height_per_entity))

    def get_player_turn_sprite(self, t: str, screen: pygame.Surface, start_x: int) -> tuple[Player, pygame.Surface]:
        """Finds the current player based on the turn given. Creates the sprite for the player that
        will be used in the turn bar.

        Args:
            t (str): The current turn which appears are (N#N).
            screen (pygame.Surface): The screen to scale the player's sprite by.
            start_x (int): The starting point of the turn bar.

        Returns:
            tuple(Player, pygame.Surface): A reference to the player and their scaled sprite.
        """

        split_turn = t.split("#")
        for p in self._other_players.values():
            if (p.get_id() == int(split_turn[1])):
                s = p.get_surface_copy()
                return (p, self._scale_sprite(s, screen, start_x))

        return (self._player, self._scale_sprite(self._player.get_surface_copy(), screen, start_x))


    def _update(self, screen: pygame.Surface, start_x: int):
        """Updates the turn bar's state, adjust sprites if the game's turn has changed.

        Args:
            screen (pygame.Surface): The screen for the turn bar.
            start_x (int): The starting point of the turn bar.
        """
        turns = self._player.get_state().get("turns", None)
        current_state = self._player.get_state().get("current_state", None)

        val = current_state == "enemy"
        # Only update if the turns have changed
        if (val) and (turns != self._turns_str):
            tmp = []
            self._num_of_turns = len(turns)
            for t in turns:
                if (t[0] == "P"):
                    tmp.append(self.get_player_turn_sprite(t, screen, start_x))
                else:
                    id = t[2:]
                    e = self._enemies[id]
                    tmp.append((e, self._scale_sprite(e.get_surface_copy(), screen, start_x)))

            self._turns = tmp
            self._turns_str = turns

    def render_bar(self, screen: pygame.Surface, start_x, start_y, font_size=14):
        """Renders the turn bar to the screen.

        Args:
            screen (pygame.Surface): The screen to render the bar to.
            start_x (int): The starting point of the turn bar.
            start_y (int): The starting point of the turn bar.
            font_size (int): The size of the text in the turn bar. Defaults to 14.
        """

        # Update the bar if need be
        self._update(screen, start_x)

        # Only render the bar if we are in an enemy state
        current_state = self._player.get_state().get("current_state", None)
        val = (current_state == "enemy") and (self._enemies != {})
        if val:

            # Initialize font if not already done
            if not ft.was_init():
                ft.init()
        
            # Create font object
            font = ft.SysFont('Arial', font_size)

            # Create text of the bar
            turn_height = self._turns[0][1].get_height()  
            turn_width = self._turns[0][1].get_width() * self._num_of_turns
            text_surface, _ = font.render("Next Up", (255, 255, 255))
            turn_height += text_surface.get_height()

            # Create background of the bar
            turn_bg = pygame.Surface((turn_width, turn_height))
            turn_bg.set_alpha(150)  # Set transparency (0-255)
            turn_bg.fill((0, 0, 0)) # Black color
            screen.blit(turn_bg, (start_x, start_y))

            screen.blit(text_surface, (start_x, start_y))
            start_y += text_surface.get_height()

            # Add entity sprites to the turn bar
            for t in self._turns:
                screen.blit(t[1], (start_x, start_y))
                start_x += t[1].get_width()


class StateManager:
    """State management for game entities including the main player and others.
   
   This class manages the state updates for the main player and other players
   in the game. It handles the application of state-specific functions based
   on the current state of each player.
   """

    def __init__(self, screen: pygame.Surface, player: Player, other_players: dict[int, Player], map: dict[int, Any]):
        """Initialize the StateManager with screen and player references.
       
       Args:
           screen (pygame.Surface): The pygame screen surface for rendering.
           player (Player): The main player instance controlled by the user.
           other_players (dict): Dictionary of other player instances in the game.
       """

        self._mainPlayer = player
        self._other_players = other_players
        self._screen = screen
        self._logger = logging.getLogger("cotb_state_manager")
        self._map = map
        self._enemies = {}
        self._action_bar = ActionBar(0,0) 

        # render methods defined in the render_methods module
        from .render_methods import voting, move, enemy 
        self._stateUpdates = {
            "vote": voting,
            "move": move,
            "enemy": enemy
        }

    def updatePlayers(self, newOtherPlayers: dict[int, Player]):
        """Update the collection of other players.
       
       Args:
           newOtherPlayers: New dictionary of other player instances.
       """
        self._other_players = newOtherPlayers

    def updateMap(self, newMap: dict[int, Any]):
        """Update the map of the game in the state manager

        Args:
            newMap: New dictionary of the new map
        """
        
        self._map = newMap

    def updateActionBar(self, actionBar: ActionBar):
        """Update the action bar for the state manager.

        Arguments:
            actionBar (ActionBar): The reference to the new action bar.
        """

        self._action_bar = actionBar

    def updateEnemies(self, newEnemies: dict[Any, Any]):
        """Update the enemies for the state manager.

        Arguments:
            newEnemies (dict): The reference to the new enemies.
        """

        self._enemies = newEnemies

    def _updateState(self):
        """Update the state of the main player.
       
       Gets the current state of the main player and applies the appropriate
       state update function if a matching state is found in _stateUpdates.
       Clears the "key" parameter after updating to ensure the state update runs
       only once.
       """
        state = self._mainPlayer.get_state()
        if (state["current_state"] in self._stateUpdates.keys()):

            self._logger.info(f"State update called on {state['current_state']} on main player")
            
            match (state["current_state"]):
                case "enemy":
                    self._stateUpdates[state["current_state"]](state, self._screen, self._mainPlayer, 
                                                       self._other_players,  self._map, self._enemies, self._action_bar, state.get("key", "-1"))
                case _:
                    self._action_bar.set_enabled(False)
                    self._stateUpdates[state["current_state"]](state, self._screen, self._mainPlayer, 
                                                       self._other_players,  self._map, self._enemies, state.get("key", "-1"))

            self._mainPlayer.update_state({"key": "-1"})

    def _updateStateOthers(self):
        """Update the states of all other players.
       
       Iterates through all other players, gets their current state, and applies
       the appropriate state update function if a matching state is found in _stateUpdates.
       Includes the main player in the player collection passed to the update function.
       """
        for p in self._other_players:
            state = self._other_players[p].get_state()
            if (state["current_state"] in self._stateUpdates.keys()):
                self._logger.info(f"State update called on {state['current_state']} on player {p}")

                # Create a copy of other players and add the main player
                other_players = dict(self._other_players)
                other_players.update({ -1 : self._mainPlayer })
                del other_players[p]

                match (state["current_state"]):
                    case "enemy":
                       self._stateUpdates[state["current_state"]](state, self._screen, self._other_players[p], 
                                                           other_players, self._map, self._enemies, self._action_bar)
                    case _:
                        self._action_bar.set_enabled(False)
                        self._stateUpdates[state["current_state"]](state, self._screen, self._other_players[p], 
                                                           other_players, self._map, self._enemies)

    def run(self):
        """Run a complete state update cycle.
       
       Updates the state of the main player followed by all other players.
       """
        self._updateState()
        self._updateStateOthers()


class GameEngine:    
    def __init__(self, server: str, fps: int):
        """Initializes the game engine.
        
        Args:
            server (str): The WebSocket server URL to connect to.
            fps (int): Target frames per second for the game.
        """

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
            # logging.FileHandler("app.log"),
            logging.StreamHandler()
            ]
        )

        self._logger = logging.getLogger("cotb_client")
        self._logger.info("Initializes Game Engine . . .")

        self._server = server
        self._fps = fps
        self._message_queue = asyncio.Queue()

        pygame.init()
        self._screen, self.screen_height, self.screen_width = self._init_screen(600, 900)
        self._clock = pygame.time.Clock()
        
        self._assets = "./client/assets/" 
        self._bg = ""
        self._image_cache = {
        }

        # Mock player
        self.player = Player(50, 50, self.screen_width, self.screen_height, {}) 
                             
        self._other_players = {} 

        self.is_transitioning = False
        self._transition_progress = 0
        self._last_move_time = 0
        self._move_cooldown = 100

        # Game state variables
        self._map = {}
        self._enemies = {}

        self._logger.info("Initializing State Manager . . .")
        self._state_manager = StateManager(self._screen, self.player, {}, self._map)


    def _update_game_state_variables(self, state: dict[Any, Any]):
        """Updates game state variables given a new game state

        This function is usually called when the server sends an "init"
        messages in the player's payload

        Args:
            state (dict): Dictionary of new game state variables.
        """

        self._logger.info("Updating Game State . . .")
        if ("map" in state):
            self._map = {int(key): value for key, value in state["map"].items()}
            self._state_manager.updateMap(self._map)

    def _update_enemies(self, enemies: dict[Any, Any]):
        """Updates enemies in the current room of the game

        It updates the enemies in the game engine, then sends the new enemies
        to the state manager.

        Args:
            state (dict): Dictionary of new game state variables.
        """

        currEnemies = set(enemies.keys())
        for e in enemies:

            id = enemies[e]["enemy_id"]
            room_id = enemies[e]["room_id"]
            enemy_type = enemies[e]["enemy_type"]
            health = enemies[e]["health"]
            attack = enemies[e]["attack"]
            defense = enemies[e]["defense"]
            ablilities = enemies[e]["abilities"].split(",")
            is_boss = enemies[e]["is_boss"]

            if e in self._enemies.keys():

                # Update fields
                self._enemies[e].id = id
                self._enemies[e].room_id = room_id 
                self._enemies[e].type_of_enemy = enemy_type
                self._enemies[e].health = health
                self._enemies[e].attack = attack
                self._enemies[e].defense = defense
                self._enemies[e].abilities = ablilities
                self._enemies[e].is_boss = is_boss
            else:
                # Add enemy
                self._enemies[e] = Enemy(id, room_id, self._screen.get_width(), self._screen.get_height(), 
                                         enemy_type, health, attack, defense, ablilities, is_boss)

        for e in list(self._enemies.keys()):
            if not (e in currEnemies):
                del self._enemies[e]

        # Give the player a target if it does not have one 
        if (self.player.get_target() == -1) or (not self.player.get_target() in currEnemies):
            self.player.find_target(self._enemies, (0,0))

        self._state_manager.updateEnemies(self._enemies)

        print(self._enemies)

    async def _connect(self):
        """Establishes a websocket connection to the server.
        
        Returns:
            websockets.WebSocketClientProtocol: The connected websocket.
            
        Raises:
            SystemExit: If connection fails.
        """
        try:
            ws = await websockets.connect(self._server) 
            return ws
        except Exception as e:
            self._logger.error(f"Error: {str(e)}")
            sys.exit()

    def _init_screen(self, height, width) -> tuple[pygame.Surface, int, int]:
        """Initializes the Pygame display window.
        
        Args:
            height (int): The height of the window.
            width (int): The width of the window.
            
        Returns:
            tuple[pygame.Surface, int, int]: The display surface, height, and width.
        """
        screen = pygame.display.set_mode((width, height)) 
        pygame.display.set_caption('Crown of the Abyss')
        return screen, height, width 

    def _handle_movement(self, keys: pygame.key.ScancodeWrapper):
        """Handles player movement based on keyboard input.
        
        Args:
            keys (pygame.key.ScancodeWrapper): The current keyboard state.
        """

        if any(keys):
            pressed_keys = [pygame.key.name(k) for k in range(len(keys)) if keys[k]]
            if pressed_keys:
                self.player.update_state({"key": pressed_keys[0]})

    def _get_background(self, image: str):
        """Gets the background of the current room.

        If the background has already been found, we get it from a cache,
        else, we find the new background and load it.

        Arguments:
            image (str): The path to the image to get.

        Returns:
            pygame.Surface: The image requested. An empty surface is returned if no
                            image is found.
        """

        if (image in self._image_cache.keys()):
            return self._image_cache[image]
        else:
            file_path = f"{self._assets}room{image}.jpg"
            if (os.path.exists(file_path)):

                tmp = pygame.Surface((self.screen_width, self.screen_height))
                img = pygame.image.load(file_path)
                resized_img = pygame.transform.scale(img, (tmp.get_width(), tmp.get_height()))
                tmp.blit(resized_img, (0,0))
                self._image_cache[image] = tmp 

                return self._get_background(image)

            else:
                self._logger.error(f"File path {file_path} does not exists")
                tmp = pygame.Surface((self.screen_width, self.screen_height))
                tmp.fill((0, 0, 0))
                return tmp
 
    def _render(self):
        """Renders all game elements to the screen.
        
        Fills the background and renders the player and all other players.
        """

        if (self._bg != ""):
            self._screen.blit(self._get_background(self._bg), (0,0))
        else:
            self._screen.fill((0,0,0))

        self.player.render(self._screen)

        for p in self._other_players:
            self._other_players[p].render(self._screen)

        for e in self._enemies:
            self._enemies[e].render(self._screen)

        if (self.player.get_target() != -1):
            self._enemies[self.player.get_target()].render_target(self._screen)

        self.player.render_name(self._screen)
        
        for p in self._other_players:
            self._other_players[p].render_name(self._screen)

        self._action_bar.render(self._screen)

        next_x, next_y = self._player_list.render(self._screen)

        next_y += 10

        self._turn_bar.render_bar(self._screen, next_x, next_y) 

    def _add_new_player(self, state: dict[Any, Any], id: int):
        """Adds a new player to the game state.
        
        Args:
            state (dict): Initial state dictionary for the player.
            id (int): The unique identifier for the player.
        """
        self._other_players[id] = Player(50, 50, self.screen_width, self.screen_height, state, id)
        self._state_manager.updatePlayers(self._other_players)


    async def _update_state_from_server(self):
        """Processes all messages in the queue and updates game state accordingly.
        
        Handles adding/removing players and updating player states based on server messages.
        """
        # Process all queued messages
        while not self._message_queue.empty():
            try:
                # Get a message from the queue
                message = await self._message_queue.get()

                # Parse the JSON message
                # data = { 'id' : { ... }, 'id : {...} ... }
                data = json.loads(message)

                current_ids = set(data.keys())

                for id, state in data.items():
                    id = int(id) # Id is currently 'id' when we need it as a number

                    # Check if the state is for us
                    if (id == self.player.get_id()):

                        if ("init" in state):
                            self._update_game_state_variables(state["init"])
                            state.pop("init")
                        
                        if ("enemies" in state):
                            self._update_enemies(state["enemies"])
                            del state["enemies"]
                        else:
                            self._update_enemies({})

                        self.player.update_state(state, isServerUpdate=True)
                        self._bg = str(self.player.get_state()["current_room_id"])

                    else:
                        if id in self._other_players.keys():
                            self._other_players[id].update_state(state, isServerUpdate=True)

                        else:
                            self._add_new_player(state, id)

                for id in list(self._other_players.keys()):
                    if str(id) not in current_ids:
                        del self._other_players[id]
                        self._logger.info(f"Player {id} has left") 

                # Mark the task as done
                self._message_queue.task_done()

            except Exception as e:
                self._logger.error(f"Error processing message: {str(e)}")

    async def run(self):
        """Main game loop.
        
        Establishes connection, handles game events, updates states, and renders the game.
        Runs continuously until the game is exited.
        """
        self._logger.info("Running Game Engine . . .")
        self._logger.info("Connecting . . .")
        self._connection = await self._connect()
        await self._connection.send(json.dumps(self.player.get_state()))

        # Create the action bar
        self._action_bar = ActionBar(self._screen.get_width(), self._screen.get_height())

        self._action_bar.set_enabled(False)

        self._state_manager.updateActionBar(self._action_bar)

        # Create the list of players

        self._player_list = PlayerList(self.player, self._other_players)

        # Create turn bar

        self._turn_bar = TurnBar(self.player, self._other_players, self._enemies)

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self._action_bar.handle_event(event)

                # Check if the main player chose an enemy target
                if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
                    self.player.find_target(self._enemies, pygame.mouse.get_pos())

            try:
                # Wait half of a frame: ~0.008 seconds for 60 fps
                response = await asyncio.wait_for(self._connection.recv(), timeout=(1/self._fps) * 0.50)
                self._logger.info(f"Response from server: {response}")
                await self._message_queue.put(response)
            except TimeoutError: 
                pass

            # Since the queue will only have one message, this wont be long
            self._logger.info("Adding state from server")
            await self._update_state_from_server()

            self._logger.info("Listening for keys")
            keys = pygame.key.get_pressed()
            self._logger.info(f"Got keys {[pygame.key.name(k) for k in range(len(keys)) if keys[k]]}")
            self._handle_movement(keys)

            self._logger.info("Running State Manager")
            self._state_manager.run()

            self._logger.info(f"Current State: {self.player.get_state()}, Other Players State: {[str(v) for _, v in self._other_players.items()]}")

            self._logger.info("Updating entites using update()")
            self.player.update()
            for p in self._other_players:
                self._other_players[p].update()

            for e in self._enemies.values():
                e.update()
                
            self._logger.info("Sending latest state to server")
            await self._connection.send(json.dumps(self.player.get_state()))

            self._render()

            pygame.display.update()
            await asyncio.sleep(1 / self._fps)
            
        self._logger.info("Ending Game Engine . . .")
        pygame.quit()
        await self._connection.close()

