import time
from BaseAI import *

class TicTacToeAI(AIHandler):
    '''Exntension for BaseAI to play Tic Tac Toe'''
    def __init__(self, name, size, mode, AIsteps) -> None:
        # Output Info about AI and 
        print('The AIs in the Tic Tac Toe handler should be 28-15-15-9.')
        print('Two AI\'s Will play against each other')
        print('The AI handler has to be Versus')
        print('This Extension edits versus mode as there are three different outcomes for each game')
        print('Following IDs are "Play" and "Test"')

        self.win_conditions = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)) # Win Detection Key
        self.Initialize(name, size, mode, AIsteps) # Initialize the Classroom
    
    # Edited Versus Mode (Incorporates Ties)
    def Versus(self, weight, ID):
        '''Versus Mode for having an AI learn.
        
        AI's play each other, with 3 different Outcomes:
        1. If an AI wins, it duplicates: One stays the same, and the other learn. Result = 1, 2
        2. If the game countinues to long: Both Learn and Stay. Result = 0
        3. If the game is a tie: Both stay and nothing happens to them. Restult = -1
        '''
        
        # Start Versus Varibles
        versus_start = time.time()
        random.shuffle(self.classroom)
        hcl = len(self.classroom)//2

        # AI's Pair up and play each other.
        new_classroom = []
        for i, pair in enumerate(list(map(list, zip(self.classroom[:hcl], self.classroom[hcl:])))):
            result = self.Test(pair, ID) # Test AI Pair
            
            # If an AI wins
            if result > 0:
                for x in range(2): # Duplicates Winnnig AI
                    new_classroom.append(copy(pair[result-1]))
                    new_classroom[-1].Rename(f'{self.name}-{self.sessions}.{(i) * 2 + 1 + x}')
                    
                new_classroom[-1].Learn(weight) # One AI Learns
            elif result == 0: # If Game Ends Because of Repetion
                for x, student in enumerate(pair): # Both AI Stay and Learn
                    new_classroom.append(copy(student))
                    new_classroom[-1].Rename(f'{self.name}-{self.sessions}.{(i) * 2 + 1 + x}')
                    new_classroom[-1].Learn(weight)
            else: # If it was a Tie
                new_classroom.extend(copy(pair)) # Do not do anything to AI's who Tie
        
        self.classroom = new_classroom # Set Classroom to new Class
        
        print(f'Generation {self.sessions} Finished in : {round(time.time() - versus_start, 2)}')
    
    # Control of Events  
    def Test(self, AI, ID):
        '''Controller of AI events'''
        if ID == 'Test': # AI learns in testing mode (Versus)
            return self.mode_test(AI)
        elif ID == 'Play': # Play Against the AI
            return self.mode_play(AI[0])
        else: raise Exception('Unknown ID') # If The ID does not exist
    
    # AI Modes
    def mode_test(self, AI):
        '''AI Learning Proccess (AI vs AI)'''
        
        # Create TIC TAC TOE Varibles
        board = [0]*9
        turn = 1
        game_state = 0
        while True: 
            # AI Play Loop
            for i in range(2):
                 # Get AI's decision for where to play
                move = self.get_highest(AI[i].Decision(self.get_inputs(i, board)))
                
                if not board[move]: board[move] = i+1 # Test if Open Square
                if turn > 5: game_state = self.detect_win(board) # Detects win after turn 6
                # Return Result, if Game has an outcome or turn is greater than 15
                if game_state or turn > 15: return game_state
                turn += 1 
    
    def mode_play(self, AI):
        '''Method to Play Against AI'''
        print(f'\nPlaying {AI.name}\n')
        
        # Initialize Tic Tac Toe Varibles
        board = [0]*9
        
        # Game Loop
        while True:
            # Print Board
            self.print_board(board)
            
            # Get Player Move    
            move = int(input('X to move: '))
            if not board[move]: board[move] = 1
            # Detect Win
            game_state = self.detect_win(board)
            if game_state: break
            
            # Get AI Move
            highest = self.get_highest(AI.Decision(self.get_inputs(1, board)))
            if not board[highest]: board[highest] = 2     
            # Detect Win
            game_state = self.detect_win(board)
            if game_state: break
        
        # Game End Cycle
        self.print_board(board)
        print((0, 'X Won The Game', 'O Won The Game', 'The Game Was A Tie')[game_state])
    
    # Tic Tac Toe Functions    
    def detect_win(self, board):
        '''Detect Tic Tac Toe Win'''
        return next((board[i[0]] for i in self.win_conditions if board[i[0]] == board[i[1]] == board[i[2]]), -1 if 0 not in board else 0,)
    
    def get_highest(self, result):
        '''Get Highest Decision For AI'''
        highest = [0, 0]
        for j, i in enumerate(result):
            if i > highest[1]:
                highest[0] = j
                highest[1] = i
        return highest[0]
    
    def get_inputs(self, player, board):
        '''Get Inputs From Board For AI'''
        inputs = [0] * 28
        inputs[0] = player
        for j, i in enumerate(board):
            if i == 1: inputs[j*3+2] = 1
            elif i == 2: inputs[j*3+3] = 1
            else: inputs[j*3+1] = 1
        return inputs
    
    def print_board(self, board):
        '''Print Board (For Play Mode)'''
        board_key = ('_', 'X', 'O') # Board Key
        for i, square in enumerate(board): # Loop Through Board
            print(f'[{board_key[square]}]', end='')
            if not (i+1) % 3: print('\n')

# Create the AI
Jeremy = TicTacToeAI('Jeremy', 50, 'v', ['r', 'data.txt'])
Jeremy.Simulate(100, 4, 'Test')
Jeremy.Record('data.txt')

