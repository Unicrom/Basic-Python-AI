import itertools
import random, keyboard, time
from copy import deepcopy as copy

# Self learning AI. This class is only the blueprint of the AI, and needs a handler and extension to work.
class AI:
    def __init__(self, matrix, name):
        self.matrix = matrix.copy() # matrix = [[weights], [biases]]
        self.name = name
        self.decisions = 0
        
    def __str__(self):
        return (f'Matrix: {self.matrix}')
    
    def Rename(self, newname):
        '''Renames the AI (self, name)'''
        self.name = newname
        
    def Display(self, showmatrix):
        '''Shows all information about the AI for viewing (self, showmatrix)'''
        if showmatrix == True:
            print('--------------------------------------------')
            print(self.matrix)
        print('--------------------------------------------')
        print(f'{self.name} is a', end=" ")
        # Node Describer
        for i in range(len(self.matrix[0])):
            print(f'{len(self.matrix[0][i])}', end=" ")
        print(f'{len(self.matrix[0][-1][-1])}', end=" ")
        # AI Age (For Learning Type)
        if self.decisions == 1:
            print(f'with {self.decisions} decision made.')
        else:
            print(f'with {self.decisions} decisions made.')

    def Random(self, steps):
        '''Randomizes the AI from 0-1 (to the ten thousanth). Warning, this wipes the AI's brain. (self, steps)'''
        self.matrix = [[], []]
        list1, list2, list3 = [], [], []
        # Randomize Weights
        for i in range(len(steps) - 1):
            for _ in range(steps[i]):
                for _ in range(steps[i + 1]):
                    list2.append(round(random.random() * 2 - 1, 4))
                list1.append(list2)
                list2 = []
            self.matrix[0].append(list1)
            list1 = []
         # Randomize Biases
        for i in range(len(steps)):
            for _ in range(steps[i]):
                if i in [0, len(steps) - 1]:
                    list3.append(0)
                else: 
                    list3.append(round(random.random() * 6 - 3, 4))
            self.matrix[1].append(list3)
            list3 = []

    def Decision(self, inputs):
        '''Place the required inputs and the AI will begin thinking about it's decision. (self, inputs)'''
        # Decision Attempt 3:
        if len(inputs) != len(self.matrix[0][0]):
            return "Input Error"
        FirstNodes = inputs # Setup First Nodes
        for i in range(len(self.matrix[0])):
            NewNodes = []
            for j in range(len(self.matrix[0][i][0])):
                NewNodes.append(0)
                for k in range(len(self.matrix[0][i])):
                    NewNodes[j] += self.matrix[0][i][k][j] * FirstNodes[k]
                NewNodes[j] = round((1 / (1 + (2.71828 ** (-NewNodes[j] + self.matrix[1][i + 1][j])))), 4)
            FirstNodes = NewNodes
        self.decisions += 1
        return NewNodes
    
    def Learn(self, magnitude):
        '''Modify the brain of the AI based on the magnitude. (self, magnitude)'''
        for i in range(len(self.matrix[0])):
            for j in range(len(self.matrix[0][i])):
                for k in range(len(self.matrix[0][i][j])):
                    self.matrix[0][i][j][k] = round(((self.matrix[0][i][j][k]) + (magnitude * random.random() / 13) - (magnitude * 0.5 / 13)), 4)
        for i in range(len(self.matrix[1])):
            for j in range(len(self.matrix[1][i])):
                if i not in [0, len(self.matrix[1]) - 1]:
                    self.matrix[1][i][j] = round((self.matrix[1][i][j]) + (magnitude * random.random() / 5) - (magnitude * 0.5 / 5), 4)
                    

# Think of this as the teacher of all of the AI made to learn or something
# Use an extension to return points and change the setting to generational, 1v1, or learning
class AIHandler:
    def Initialize(self, name, size, mode, AIsteps): # AIsteps == ['r', file name, starting AI, next AIs] means read file.
        # sourcery skip: extract-duplicate-method
        self.name = name
        self.size = size
        self.AIsteps = AIsteps
        self.mode = mode
        self.sessions = 0

        # Setup the classroom
        self.classroom = []
        # Text file format:
        # 1- AI Name
        # 2- AI Matrix
        # 3- AI Decisions
        # 4- Blank Space

        if self.AIsteps[0] == 'r':
            textitem = self.AIsteps # Read format will be [r, txt document, starting number, next numbers]
            try:
                AIfile = open(textitem[1], 'r')
                txtlines = AIfile.read().split('\n')
                for i in range(textitem[2], textitem[2] + textitem[3]):
                    try:
                        NewAI = AI(txtlines[i * 4 - 3], f'{self.name}-{self.sessions}.{i}')
                        self.classroom.append(NewAI)
                    except Exception:
                        print(f'\nAI Handler {self.name} opened an empty AI (ignore following text)')
                        time.sleep(0.0001)
                        exit()
                self.size = len(self.classroom)
            except Exception:
                print(f'\nAI Handler {self.name} opened an invalid file.')
                time.sleep(0.0001)
                exit()

        else:
            for number, i in enumerate(range(self.size), start=1):
                if self.mode == 'l':
                    self.classroom.append(AI([], f'{self.name}-{self.sessions}'))
                else:
                    self.classroom.append(AI([], f'{self.name}-{self.sessions}.{number}'))
                self.classroom[i].Random(self.AIsteps)

        # Test for odd size on 1v1 and non-10 divisible generational handlers
        if self.mode == 'v' and self.size % 2 != 0:
            print()
            print('1v1 handlers can\'t have an odd number of AIs')
            time.sleep(0.01)
            exit()

        if self.mode == 'g' and self.size % 10 != 0:
            print()
            print('Generational handlers can\'t have an odd number of AIs')
            time.sleep(0.01)
            exit()

    def Display(self, showAI):
        '''Displays the AI handler. Set showAI to 'all' to display all of the AI's or 'one' to display one (self, showAI)'''
        if self.mode == 'l': # L
            print(f'AI Handler {self.name} is a learning handler.')
        elif self.mode == 'g': # G
            print(f'AI Handler {self.name} is a generational handler with a size of {self.size}.')
        else: # V
            print(f'AI Handler {self.name} is a 1v1 generational handler with a size of {self.size}.')

        if self.AIsteps[0] != 'r':
            print(f'The AIs in the handler are {self.AIsteps}')
        print(f'{self.sessions} learning sessions made by this handler')

        if showAI == 'all':
            print()
            print('AI list: ')
            for i in self.classroom:
                i.Display(True)
        elif showAI == 'one':
            print()
            print('AI example: ')
            self.classroom[0].Display(True)
        print()
        print()
            
    def Record(self, file):
        '''Records the classroom in a file, it does overrun. You can record in a new file. (self, file)'''
        AIfile = open(file, 'w')
        for i in range(len(self.classroom)):
            AIfile.write(f'{self.classroom[i].name}\n')
            AIfile.write(f'{self.classroom[i].matrix}\n')
            AIfile.write(f'{self.classroom[i].decisions}\n')
            AIfile.write(f'\n')
            
    def Try(self, AInumber, ID):
        '''Tests the functionality of the AI manually. This doesn't help the AI learn. (self, AInumber, ID)'''
        print('Testing the AI...')
        try:
            self.Test(self.classroom[AInumber], f'{ID}-test')
        except Exception:
            print('You put the wrong number. Try again.')
            
    def FindCost(self, output, ExpectedOutput):
        '''A cool way to grade an AI. Used in the Test Function. Lower number means better. (self, output, ExpectedOutput)'''
        if len(output) != len(ExpectedOutput):
            print()
            print('Output length is not the same as the expected output length.')
            time.sleep(0.001)
            exit()
        Cost = sum((output[i] - ExpectedOutput[i])**2 for i in range(len(output)))
        Cost /= len(output)
        return Cost

    def Simulate(self, steps, weight, ID):
        '''The main function of the handler, uses an extension to change the weights of the AI to do the desired task.
           (self, steps, weight) steps = -1 for infinite, space to stop anytime. Weight controls the speed of how the AI learns.
           This function is required an extension (function with the correct id to work).'''
        print('-------------------------')
        print('Simulation Started. Hold space to Stop.')
        print('-------------------------')
        StartTime = time.time()
        pastgrade = 0 # For Learning AI
        savedAI = self.classroom[0] # Also for Learning AI
        while (steps >= 1 or steps == -1) and not keyboard.is_pressed('space'):
            self.sessions += 1
            if self.mode == 'l': # Learning
                self.Learning(pastgrade, savedAI, weight, ID)
                continue
            elif self.mode == 'g': # Generation
                self.Generate(weight, ID)
                continue
            elif self.mode == 'v': # Generation 1v1
                self.Versus(weight, ID)
                continue
            steps -= 1
            
        # After Code
        print(f'This AI has a total of {self.sessions} sessions.')
        print(f'This took a total of {time.time() - StartTime} seconds.')
        print(f'Use self.Record to save the AI\'s. Bye now!')
     
    def Learning(self, pastgrade, savedAI, weight, ID):
        '''Learning handlers have one AI and learns when the AI performs worse then what it did earlier.'''
        self.classroom[0] = savedAI
        self.classroom[0].Learn(weight)
        self.classroom[0].Rename(f'{self.name}-{self.sessions}')
        grade = self.Test(self.classroom[0], ID)
        if grade > pastgrade:
            pastgrade = grade
            savedAI = self.classroom[0]
            print(f'Highest Grade: {grade}')
            
    def Generate(self, weight, ID):
        '''There is multiple AIs that learn and the lower 90% graded dissapears and the upper 10% graded duplicates and learns.'''
        grades = []
        avgGrades = 0
        # Test the AIs
        for i in range(len(self.classroom)):
            self.classroom[i].Rename(f'{self.name}-{self.sessions}.{i}')
            grades.append(self.Test(self.classroom[i], ID))
            avgGrades += grades[-1]
        AIgrades = list(sorted(zip(self.classroom.copy(), grades.copy()), key=lambda x: x[1]))

        # "Eliminate" the bad AIs and duplicate the generation
        del AIgrades[:int((len(AIgrades.copy()) * 0.9))]

        self.classroom = []
        for AIgrade, _ in itertools.product(AIgrades, range(10)):
            self.classroom.append(0)
            self.classroom[-1] = copy(AIgrade[0])
            self.classroom[-1].Learn(weight)

        f, g = zip(*AIgrades.copy())
        print(f'Next Sorted Grades: {g}')

        avgGrades /= len(self.classroom)
        print(f'Avg Grade:{round(avgGrades, 5)}')

    def Versus(self, weight, ID):
        '''Each AI faces each other in a fight to the death every generation, where the winner duplicates.'''
        random.shuffle(self.classroom)
        for i in range(len(self.classroom) / 2):
            # Result can either be 0 or 1 AI tagged with result gets to live.
            result = self.Test([self.classroom[-(i * 2 + 1)], self.classroom[-(i * 2 + 2)]], ID)
            del self.classroom[-(i * 2 + int(not bool(result)) + 1)]
        
        # Duplicate "victory AIs"
        newclassroom = []
        for i in copy(self.classroom):
            newclassroom.append(i.Learn(weight))
            newclassroom[-1].Rename(f'{self.name}-{self.sessions}.{i * 2}')
            newclassroom.append(i.Learn(weight))
            newclassroom[-1].Rename(f'{self.name}-{self.sessions}.{i * 2 + 1}')
            
        self.classroom = newclassroom
        
# AI Instrucions
print('-------------------------------------------------------------')
print('Make an handler using "ai123 (or whatever name) = AIHandler(name, size, mode, AIsteps)"')
print('Size is the size of AI. Mode can be "l", "g", or "v", which is learning, generational, or 1v1')
print('AIsteps is the neural strusture of the AI, or you can read from file with replacing as [r, file, starting number, next numbers')
print('Function Handler List:')
print('Display: Displays the AI. One paramater, set it to "one" for one AI example, "all" for all.')
print('Record: Records the classroom. One parametar, set it to the recording file. Overwrites the file.')
print('Try: Test the AI. Two Parameters, set firse to the AI in the list you want to test, set the second to the ID.')
print('Simulate: Actually does the AI thing. Following paramaters: (# of sessions [-1 for infinite, space to stop], ')
print('speed of learning, extention ID) There, have fun using this!')
print('-------------------------------------------------------------')