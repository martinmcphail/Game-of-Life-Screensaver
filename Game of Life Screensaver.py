# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 22:43:00 2024

@author: marti
"""

import pygame
import numpy as np
import time
import random

# Define the colors (RGB values)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
MEDIUM_SPRING_GREEN = (0, 250, 154)
LIGHT_SEA_GREEN = (32, 178, 170)

BLACK = (0, 0, 0)
DARK_PURPLE = (48, 25, 52)
DARK_GREEN = (2, 48, 32)

# List of possible colors for live cells
LIVE_COLORS = [WHITE, GREEN, LIGHT_GREEN, MEDIUM_SPRING_GREEN, LIGHT_SEA_GREEN]

# List of possible colors for dead cells
DEAD_COLORS = [BLACK, DARK_PURPLE, DARK_GREEN]

# Initialize Pygame
pygame.init()

# Hide cursor
pygame.mouse.set_visible(False)

# Get the screen dimensions (full screen resolution)
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# Define the cell size for the grid (adjust to your preference)
CELL_SIZE = 50

# Calculate grid dimensions based on screen size
grid_width = SCREEN_WIDTH // CELL_SIZE
grid_height = SCREEN_HEIGHT // CELL_SIZE

# Create the grid for the Game of Life
grid = np.random.randint(2, size=(grid_height, grid_width))

# Set the display mode to fullscreen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Game of Life Screensaver")

def update_grid(grid):
    new_grid = np.copy(grid)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            total = int((grid[i, (j - 1) % grid.shape[1]] + grid[i, (j + 1) % grid.shape[1]] +
                        grid[(i - 1) % grid.shape[0], j] + grid[(i + 1) % grid.shape[0], j] +
                        grid[(i - 1) % grid.shape[0], (j - 1) % grid.shape[1]] + grid[(i - 1) % grid.shape[0], (j + 1) % grid.shape[1]] +
                        grid[(i + 1) % grid.shape[0], (j - 1) % grid.shape[1]] + grid[(i + 1) % grid.shape[0], (j + 1) % grid.shape[1]]))

            if grid[i, j] == 1:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = 0
            else:
                if total == 3:
                    new_grid[i, j] = 1
    return new_grid

def draw_grid(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:  # Alive cell
                color = random.choice(LIVE_COLORS)  # Randomly choose one of the live colors
            else:
                color = random.choices(DEAD_COLORS, [5000,1,1])[0]  # Randomly choose one of the dead colors
                
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to introduce an R-pentomino pattern at a random location
def find_empty_regions(grid):
    empty_regions = []
    
    # Scan the grid for empty 3x3 regions
    for x in range(grid.shape[0] - 2):  # Ensure we stay within bounds
        for y in range(grid.shape[1] - 2):
            # Extract the 3x3 subgrid
            subgrid = grid[x:x+3, y:y+3]
            
            # Check if all cells in the 3x3 subgrid are dead (0)
            if np.all(subgrid == 0):
                empty_regions.append((x, y))
    
    return empty_regions

def introduce_glider_in_empty_region(grid):
    # Get all the empty 3x3 regions
    empty_regions = find_empty_regions(grid)
    
    # If no empty regions are found, return the grid as is
    if not empty_regions:
        print("No empty region found to place a glider.")
        return grid
    
    # Randomly choose one of the empty regions
    x, y = random.choice(empty_regions)
    
    # Define the glider pattern
    glider = np.array([[0, 1, 0], 
                       [0, 0, 1], 
                       [1, 1, 1]])
    
    # Place the glider in the chosen location
    grid[x:x+3, y:y+3] = glider
    print(f"Glider introduced at: ({x}, {y})")
    
    return grid


# Add a delay to ignore any initial input right after starting the screensaver
ignore_input_duration = 2  # Seconds to ignore input after screensaver starts
start_time = time.time()

# Main loop

clock = pygame.time.Clock()
running = True

previous_grid = np.copy(grid)  # To track the previous grid
second_previous_grid = np.copy(grid)  # To track the second previous grid

running = True
while running:
    for event in pygame.event.get():
        # Only check for input after the initial delay
        if time.time() - start_time > ignore_input_duration:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
                running = False

    screen.fill((0, 0, 0))  # Clear the screen
    draw_grid(grid)
    
    # Check for "boring" state BEFORE updating the grid
    if np.array_equal(grid, previous_grid) or np.array_equal(grid, second_previous_grid):
        print("Boring state detected. Introducing glider.")
        grid = introduce_glider_in_empty_region(grid)

    # Now update the grid after the boring check
    new_grid = update_grid(grid)
    
    # Shift grid states for next iteration
    second_previous_grid = np.copy(previous_grid)
    previous_grid = np.copy(grid)
    grid = np.copy(new_grid)
    
    pygame.display.flip()
    pygame.time.delay(40)  # Control the speed of the simulation

    
    """
    clock.tick(30)  # Limit frame rate to 30 FPS
"""
# Show the mouse cursor again after quitting the screensaver
pygame.mouse.set_visible(True)

pygame.quit()