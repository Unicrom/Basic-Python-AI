import random, time, math, pygame, keyboard
from BaseAI import *
from _2048_IMG import *

class _2048AI(AIHandler):
    def __init__(self, name, size, mode, AIsteps):
        print('This 2048 AI should be a 288-15-20-4 structured AI')
        print('The input is one of the 18 possible squares, on all 16 in the grid, and the output is up, down, left, or right.')
        print('Please make it generational.')
        print('IDs are "Learn" and "Test"')
        # Make movelist because bad code to be stated too many times.
        self.moveList = ([[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]],
                         [[12, 8, 4, 0], [13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3]],
                         [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]],
                         [[3, 2, 1, 0], [7, 6, 5, 4], [11, 10, 9, 8], [15, 14, 13, 12]])
        # Square values because bad code to multiply manually
        self.SquareValues = (0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072)
        self.Initialize(name, size, mode, AIsteps)
        
    def SetupGrid(self, amplifier):
        grid = [0] * 16 # Clear the Grid
        self.PlaceSquare(grid, amplifier) # Place two random squares in the grid
        self.PlaceSquare(grid, amplifier)
        return grid
        
    def PlaceSquare(self, grid, amplifier):
        '''Places a random square on an empty space in the grid (self, grid)'''
        # Get two procedually random number things (0-1)...
        funRandom = ((amplifier + grid[0] * 0.8 * grid[1] + grid[2] * 0.2 + grid[4] * 0.6 + grid[6] * 0.1 * grid[5] + grid[8] * 0.5 + grid[11] * grid[10] * 0.4 * grid[11] + grid[12] * 1.1 + grid[14] * 0.7 * grid[15]) / 10) % 1
        otherFunRandom = (((funRandom * amplifier) + grid[1] * 0.9 + grid[3] * 0.7 * grid[0] + grid[5] * 0.8 * grid[6] + grid[7] * 0.3 * grid[8] + grid[9] * 0.5 * grid[8] + grid[11] * 0.4 + grid[13] * 0.6 * grid[12] + grid[15] * 0.2 * grid[14]) / 10) % 1
        # Find all empty spaces (if any)
        emptySpaces = []
        for i in range(len(grid)):
            if grid[i] == 0: emptySpaces.append(i) 
        # Fill an empty space with a 2 or a 4
        if len(emptySpaces) != 0:
            if funRandom > 0.1: grid[emptySpaces[math.floor(otherFunRandom * len(emptySpaces))]] = 1
            else: grid[emptySpaces[math.floor(otherFunRandom * len(emptySpaces))]] = 2
        return grid
    
    def Squishify(self, grid, inputs, amplifier):
        '''Squishes the grid based on the arrow key inputed by the AI'''
        # Record Old Grid
        oldGrid = grid.copy()
        # Find Input
        highestGuess = 0
        for i in range(len(inputs)):
            if inputs[i] > highestGuess:
                highestGuess = inputs[i]
                key = i
        # Squishify the thing
        # Go through every row
        for i in range(4):
            combinedGrid = [0, 0, 0, 0]
            row = [self.moveList[key][i][0], self.moveList[key][i][1], self.moveList[key][i][2], self.moveList[key][i][3]]
            for j in range(1, 4):
                # Go through every square in every row
                if grid[row[j]] != 0:
                    box = j
                    combined = False
                    # Go through every movement in every square in every row...
                    while True:     
                        if box == 0:
                            break
                        elif grid[row[box - 1]] == 0:
                            grid[row[box - 1]] = grid[row[box]]
                            grid[row[box]] = 0
                            box -= 1
                        elif grid[row[box - 1]] == grid[row[box]] and combined == False and combinedGrid[box - 1] == 0:
                            grid[row[box - 1]] += 1
                            grid[row[box]] = 0
                            combined = True
                            combinedGrid[box - 1] = 1
                            self.score += self.SquareValues[grid[row[box - 1]]]
                            box -= 1
                        else:
                            break
        if grid == oldGrid and self.score != 0:
            grid = 'Game Over'
        else:
            self.PlaceSquare(grid, amplifier)
        return grid
    
    def DisplayGame(self, display, grid):
        '''Uses pygame to display the game that is being played by the AI (self, display, grid)'''
        BACKGROUND = (187, 163, 160)
        BLACK = (0, 0, 0)
        waitSpace = False
        if grid == 'update':
            pygame.event.pump()
            return 
        if grid == 'close':
            pygame.quit()
            return 
        if grid == 'setup':
            waitSpace = True
            display = 'Press "Q" to Start...'
            grid = [0] * 16
            pygame.init()
            size = (592, 632)
            pygame.display.set_caption('2048')
            self.gameScreen = pygame.display.set_mode(size)
        self.gameScreen.fill(BACKGROUND)
        # Displays the squares
        if grid != 'Game Over':
            self.displayOldGrid = grid
        for i in range(4):
            for j in range(4):
                image = pygame.image.load(f'GAME2048/_2048_IMG/tile_{self.displayOldGrid[i * 4 + j]}.png')
                self.gameScreen.blit(image, (16 + (i * 144), 56 + (j * 144)))
        # Displays the Text
        font = pygame.font.SysFont("Verdana", 24, bold=True, italic=False)
        txtsurf = font.render(display, True, BLACK)
        self.gameScreen.blit(txtsurf,(10, 10))
        # Updates the Game Screen
        pygame.display.flip()
        pygame.event.pump()
        if waitSpace == True:
            while not keyboard.is_pressed('q'):
                pygame.event.pump()
                time.sleep(0.1)
        
    def Test(self, AI, ID):
        '''Tests the AI for learning and stuff (self, AI, ID)'''
        if ID == 'Learn': # LEARNING AI
            testGames = 50
            # Set self.seed
            if AI.name == self.classroom[0].name:
                self.seed = [random.random() for i in range(testGames)]
            finalGrade = 0
            for i in range(testGames):
                self.score = 0
                grid = self.SetupGrid(self.seed[i])
                while 1:
                    # Turn the grid into binary inputs
                    inputs = [0] * 288
                    for j in range(16):
                        inputs[(j * 18) + grid[j]] = 1
                    result = AI.Decision(inputs)
                    grid = self.Squishify(grid, result, self.seed[i])
                    if grid == 'Game Over':
                        finalGrade += self.score
                        break
            finalGrade /= testGames
            return finalGrade
        
        elif ID == 'Test': # TESTING AI
            self.seed = random.random()
            self.score = 0
            grid = self.SetupGrid(self.seed)
            self.DisplayGame('Starting Game...', 'setup')
            time.sleep(0.4)
            while 1:
                # Turn the grid into binary inputs
                inputs = [0] * 288
                for i in range(16):
                    inputs[(i * 18) + grid[i]] = 1
                result = AI.Decision(inputs)
                grid = self.Squishify(grid, result, self.seed)
                display = f'{AI.name} : {self.score}'
                self.DisplayGame(display, grid)
                if grid == 'Game Over':
                    display = f'{AI.name} : {self.score} : Game Over...'
                    self.DisplayGame(display, grid)
                    time.sleep(1)
                    self.DisplayGame(display, 'close')
                    return f'Score: {self.score}'
                time.sleep(0.2)
        elif ID == 'Fun': # FUN AI
            # Keyboard variable
            self.seed = random.random()
            keys = [0] * 4
            self.score = 0
            grid = self.SetupGrid(self.seed)
            self.DisplayGame('Starting Game...', 'setup')
            time.sleep(0.1)
            display = f'{AI.name} : {self.score}'
            self.DisplayGame(display, grid)
            while 1:
                # Wait for Key press
                result = 0
                while result == 0:
                    if not keyboard.is_pressed('left') and keys[0] == 1:
                        keys[0] = 0
                    if not keyboard.is_pressed('right') and keys[1] == 1:
                        keys[1] = 0
                    if not keyboard.is_pressed('up') and keys[2] == 1:
                        keys[2] = 0
                    if not keyboard.is_pressed('down') and keys[3] == 1:
                        keys[3] = 0
                    if keyboard.is_pressed('left') and keys[0] == 0:
                        keys[0] = 1 # UP
                        result = 1
                    if keyboard.is_pressed('right') and keys[1] == 0:
                        keys[1] = 1 # DOWN
                        result = 1
                    if keyboard.is_pressed('up') and keys[2] == 0:
                        keys[2] = 1 # LEFT
                        result = 1
                    if keyboard.is_pressed('down') and keys[3] == 0:
                        keys[3] = 1 # RIGHT
                        result = 1
                    time.sleep(0.02)
                    self.DisplayGame(display, 'update')
                grid = self.Squishify(grid, keys, self.seed)
                for i in keys:
                    if i == 1:
                        i = 2
                display = f'{AI.name} : {self.score}'
                self.DisplayGame(display, grid)
                if grid == 'Game Over':
                    display = f'{AI.name} : {self.score} : Game Over...'
                    self.DisplayGame(display, grid)
                    time.sleep(1)
                    self.DisplayGame(display, 'close')
                    return f'Score: {self.score}'


# Testing Codes
Carl = _2048AI('Carl', 1, 'l', [288, 16, 16, 4])
Carl.Simulate(10000000, 1, 'Learn')
Carl.Test(Carl.classroom[0], 'Test')

# Fun Codes
# Carl = _2048AI('Carl', 1, 'l', [288, 15, 20, 4])  
# Carl.Test(Carl.classroom[0], 'Fun')
