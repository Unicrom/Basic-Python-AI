import random, time, math
from BaseAI import *

class MultiplyAI(AIHandler):
    def __init__(self, name, size, mode, AIsteps):
        print('The AIs in the multiplication handler should be 20-10-10-20.')
        print('The input should be two random numbers, and the output is two numbers for a 2-digit number.')
        print('The AI handler has to be leraning or generational.')
        print('Following IDs are "Qlearn" and "Mtest"')
        self.Initialize(name, size, mode, AIsteps)

    def Test(self, AI, ID):
        '''Does a ten-question multiplication test with grades equal to learning or generational. Grade is between 0 and 1'''
        if ID == 'Qlearn':
            FinalGrade = 0
            for i in range(100):
                f1 = math.floor(i / 10)
                f2 = i % 10
                inputs = [0] * 20 
                inputs[f1] = 1
                inputs[f2 + 10] = 1
                answer = f1 * f2
                ExpectedOutput = [0] * 20
                if len(str(answer)) == 1:
                    ExpectedOutput[0] = 1
                    ExpectedOutput[10 + answer] = 1
                else:
                    ExpectedOutput[math.floor(answer / 10)] = 1
                    ExpectedOutput[10 + answer % 10] = 1

                # Do the Decision
                result = AI.Decision(inputs)
                FinalGrade += 1 - self.FindCost(result, ExpectedOutput)
            FinalGrade /= 100
            return FinalGrade

        elif ID == 'Mtest':
            self.ai_calculate(AI)
        else:
            print('This handler can\'t find the ID.')

    def ai_calculate(self, AI):
        f1 = random.randint(0, 9)
        f2 = random.randint(0, 9)
        inputs = [0] * 20
        inputs[f1] = 1
        inputs[f2 + 10] = 1
        print(f'AI {AI.name} will multiply {f1}x{f2}')
        result = AI.Decision(inputs)

        HighGuess1 = 0
        FoundAnswer1 = 0
        for i in range(10):
            if result[i] > HighGuess1:
                HighGuess1 = result[i]
                FoundAnswer1 = i
        HighGuess2 = 0
        FoundAnswer2 = 0
        for i in range(10):
            if result[i + 10] > HighGuess2:
                HighGuess2 = result[i + 10]
                FoundAnswer2 = i

        print(f'AI answers with {FoundAnswer1}{FoundAnswer2} at a {round(HighGuess1 + HighGuess2 * 50, 4)}% certainty')
        print(result)

# Testing Codes
Carl = MultiplyAI('Carl', 100, 'g', [20, 10, 10, 20])
Carl.Simulate(10000000000, 1, 'Qlearn')
Carl.Test(Carl.classroom[0], 'Mtest')
print(Carl.classroom[0])