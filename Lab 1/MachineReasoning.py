import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 530, 530
ROWS, COLS = 10, 10
SQUARE_SIZE = 50
SQUARE_SPACING = 3
RADIUS = 10
SELECTED_COLOR = (255, 255, 0)

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 240, 45)
GREEN = (0, 218, 132)
RED = (221, 0, 70)
BLUE = (37, 65, 178)
ORANGE = (255, 177, 45)
COLORS = [YELLOW, GREEN, RED, BLUE, ORANGE]

# Function to generate the board
def generate_board():
    board = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]
    filled_squares = random.sample(range(ROWS * COLS), (ROWS * COLS) // 2)
    for square_index in filled_squares:
        row = square_index // COLS
        col = square_index % COLS
        color = random.choice(COLORS)
        board[row][col] = color
    return board

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Randomly Generated Board")

# Function to draw the board
def draw_board(board, selected_square):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * (SQUARE_SIZE + SQUARE_SPACING) + SQUARE_SPACING,
                               (row ) * (SQUARE_SIZE + SQUARE_SPACING) + SQUARE_SPACING,
                               SQUARE_SIZE - SQUARE_SPACING,
                               SQUARE_SIZE - SQUARE_SPACING)
            pygame.draw.rect(window, board[row][col], rect, border_radius=RADIUS)
            if (row, col) == selected_square:
                pygame.draw.rect(window, SELECTED_COLOR, rect, border_radius=RADIUS, width=3)

# Function to find the row and column of a given position
def get_row_col_from_pos(pos):
    x, y = pos
    row = (y - SQUARE_SPACING) // (SQUARE_SIZE + SQUARE_SPACING)
    col = (x - SQUARE_SPACING) // (SQUARE_SIZE + SQUARE_SPACING)
    return row, col

# Function to write logs to a file
def write_log(log_message):
    with open("logs.txt", "a") as file:
        file.write(log_message + "\n")

# Function to move the square to the target position and pop squares of the same color below
def move_square(board, start, end):
    original_color = board[start[0]][start[1]]  # Store the original color
    path = find_path(board, start, end)
    if path:
        # Log the movement
        log_message = f"Moved square with color {original_color} from {start} to {end}, visited indexes: {' -> '.join(map(str, path))}"
        write_log(log_message)
        for i, position in enumerate(path):
            row, col = position
            if i == len(path) - 1:
                break  # Skip the last position since it's the end position
            next_row, next_col = path[i + 1]  # Get the next position
            
            # Move the square to the next position
            board[row][col] = WHITE
            board[next_row][next_col] = original_color
            
            # Draw the updated board
            draw_board(board, start)
            pygame.display.update()
            time.sleep(0.1)

            # print(board[next_row+1][next_col])

            # # Check the square below if it has the same color
            # if board[next_row+1][next_col] == original_color:
            #     # If the color matches, pop both squares
            #     board[next_row][next_col] = WHITE
            #     board[next_row+1][next_col] = WHITE
        # Check and pop squares below the moved square
        check_and_pop_below(board, path[-1])

# Function to check and pop squares below the moved square
def check_and_pop_below(board, end_position):
    row, col = end_position
    original_color = board[row][col]
    if row + 1 < ROWS:  # Check if the row index for the square below is within the valid range
        if board[row + 1][col] == original_color:
            # If the color matches, pop both squares
            board[row][col] = WHITE
            board[row + 1][col] = WHITE

            # Log the popping action
            log_message = f"Popped squares with color {original_color} at {end_position} and ({row + 1}, {col})"
            write_log(log_message)



from collections import deque

# Function to find a path from start to end using BFS algorithm
def find_path(board, start, end):
    visited = set()  # Set to keep track of visited nodes
    queue = deque([(start, [])])  # Queue for BFS traversal, each element is a tuple of (node, path)
    
    while queue:
        current, path = queue.popleft()  # Dequeue the current node and its path
        
        if current == end:
            return path + [current]  # If the current node is the end, return the path
            
        visited.add(current)  # Mark the current node as visited
        
        # Get the next possible positions
        next_positions = get_next_positions(board, current)
        
        for next_pos in next_positions:
            if next_pos not in visited:
                queue.append((next_pos, path + [current]))  # Enqueue the next node with its path
    
    return None  # If no path is found, return None

# Function to get the next possible positions for the given current position
def get_next_positions(board, current):
    row, col = current
    next_positions = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Possible directions: down, up, right, left
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == WHITE:
            next_positions.append((new_row, new_col))  # Add valid next position
    
    return next_positions


# Main game loop
def main():
    board = generate_board()
    selected_square = None
    is_selected = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_pos(pos)
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if not is_selected:
                        selected_square = (row, col)
                        is_selected = True
                    elif is_selected and selected_square == (row, col):
                        is_selected = False
                    else:
                        if board[row][col] == WHITE:
                            move_square(board, selected_square, (row, col))
                        is_selected = False

        # Clear the screen
        window.fill(WHITE)

        # Draw the board
        draw_board(board, selected_square)

        # Update the display
        pygame.display.update()

if __name__ == "__main__":
    main()
