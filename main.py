from graphics import Canvas
import random
import time

    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400



def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    #create text
    numbers = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 33, 33]
    random.shuffle (numbers)
    
    #create the grid
    size_rectangle = CANVAS_WIDTH // 8
    grid = []
    visibility = [[False for _ in range(8)] for _ in range(8)]  # Track visibility
    index = 0
    for r in range (8):
        grid_row= []
        for c in range (8):
            x1= 0
            y1= 0
            x2= x1+ size_rectangle
            y2 = y1+ size_rectangle
            rectangle= canvas.create_rectangle(x1 +size_rectangle*c, y1 + +size_rectangle*r, x1+ size_rectangle*(c+1),y1+ size_rectangle*(r+1), "white", "black")
            grid_row.append(numbers[index]) 
            index += 1
        grid.append(grid_row)    
    #track cells
    chosen= []
    player_pairs= 0
    computer_pairs=0
    computer_memory = {}
    #check clicks
    while player_pairs < 3 and computer_pairs < 3:
        #player turn
        chosen = player_turn(canvas, grid, visibility, size_rectangle, computer_memory)
        if chosen:
            row1, col1 = chosen[0]
            row2, col2 = chosen[1]
            if grid[row1][col1] != grid[row2][col2]: 
                time.sleep(1)  # Sleep for 1 second
                hide_numbers(canvas, row1, col1, row2, col2, visibility, size_rectangle)
                    
            else:
                print("Match!")
                player_pairs += 1
                time.sleep(1)  # Sleep for 1 second
                show_numbers(canvas, row1, col1, row2, col2, visibility, size_rectangle)
                if grid[row1][col1] in computer_memory:
                    del computer_memory[grid[row1][col1]]
                
            if player_pairs >= 3:
                canvas.create_text(CANVAS_WIDTH / 2, 0, text='Player Wins!', font_size=30, color='purple')
                break
        #computer turn
        time.sleep(1)  # Pause before the computer's turn
        computer_choice = make_computer_choice(grid, visibility, computer_memory)
        if computer_choice is not None:
            (row1, col1), (row2, col2) = computer_choice  
                # Reveal computer choice
            for (row, col) in [computer_choice[0], computer_choice[1]]:
                if not visibility[row][col]:
                    x1 = col * size_rectangle
                    y1 = row * size_rectangle
                    x2 = x1 + size_rectangle
                    y2 = y1 + size_rectangle
                    canvas.create_rectangle(x1, y1, x2, y2, color='white', outline='black')
                    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(grid[row][col]), font_size=14)
                    visibility[row][col] = True
            time.sleep(1)

            if grid[row1][col1] == grid[row2][col2]:
                print("Match!")
                computer_pairs += 1
                time.sleep(2)  # Sleep for 2 seconds
                show_numbers(canvas, row1, col1, row2, col2, visibility, size_rectangle)
                if grid[row1][col1] in computer_memory:
                    del computer_memory[grid[row1][col1]]
                
            else: 
                if grid[row1][col1] in computer_memory:
                    if len(computer_memory[grid[row1][col1]]) < 2 and (row1, col1) not in computer_memory[grid[row1][col1]]:
                        computer_memory[grid[row1][col1]].append((row1, col1))
                    else:
                        computer_memory[grid[row1][col1]] = [(row1, col1)]
                        
                if grid[row2][col2] in computer_memory:
                    if len(computer_memory[grid[row2][col2]]) < 2 and (row2, col2) not in computer_memory[grid[row2][col2]]:
                        computer_memory[grid[row2][col2]].append((row2, col2))
                    else:
                        computer_memory[grid[row2][col2]] = [(row2, col2)]

                time.sleep(2)
                hide_numbers(canvas, row1, col1, row2, col2, visibility, size_rectangle)

            if computer_pairs >= 3: #winner
                canvas.create_text(CANVAS_WIDTH / 2, 0, text='Computer Wins!', font_size=30, color='red')
                break
    canvas.mainloop()



def show_numbers(canvas, row1, col1, row2, col2, visibility, size_rectangle):
    for row, col in [(row1, col1), (row2, col2)]:
        x1 = col * size_rectangle
        y1 = row * size_rectangle
        x2 = x1 + size_rectangle
        y2 = y1 + size_rectangle
        canvas.create_rectangle(x1, y1, x2, y2, color='gray', outline='black')
        visibility[row][col] = True

def hide_numbers(canvas, row1, col1, row2, col2, visibility, size_rectangle):
    for row, col in [(row1, col1), (row2, col2)]:
        x1 = col * size_rectangle
        y1 = row * size_rectangle
        x2 = x1 + size_rectangle
        y2 = y1 + size_rectangle
        canvas.create_rectangle(x1, y1, x2, y2, color='white', outline='black')
        visibility[row][col] = False

def player_turn(canvas, grid, visibility, size_rectangle, memory):
    chosen = []
    while len(chosen) < 2:
        click_position = canvas.get_last_click()
        if click_position is not None:
            x, y = click_position
            col = int (x // size_rectangle)
            row = int (y // size_rectangle)

            if 0 <= row < 8 and 0 <= col < 8:
                if not visibility[row][col]:
                    visibility[row][col] = True
                    number = grid[row][col]
                    
                    x1 = col * size_rectangle
                    y1 = row * size_rectangle
                    x2 = x1 + size_rectangle
                    y2 = y1 + size_rectangle
                    
                    canvas.create_rectangle(x1, y1, x2, y2, color='white', outline='black')
                    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(number), font_size=14)
                    remember_probability = 0.5  # 30% chance to remember 
                    if random.random() < remember_probability:
                        update_memory(memory, number, (row, col))
                    chosen.append((row, col))
    return chosen

def make_computer_choice(grid, visibility, memory):
     # Step 1: Look for any known pairs in memory
    for number, positions in memory.items():
        if len(positions) == 2:
            return positions[0], positions[1]
    
    # Step 2: If no pair in memory, choose randomly
    available_choices = [(r, c) for r in range(8) for c in range(8) if not visibility[r][c]]
    if len(available_choices) < 2:
        return None
  
    choice1 = random.choice(available_choices)
    available_choices.remove(choice1)
    choice2 = random.choice(available_choices)
    return choice1, choice2 
    
def update_memory(memory, number, position):
    # Store up to 2 positions for each number
    if number in memory:
        if len(memory[number]) < 2 and position not in memory[number]:
            memory[number].append(position)
    else:
        memory[number] = [position]

if __name__ == '__main__':
    main()