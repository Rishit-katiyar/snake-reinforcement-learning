import pygame
import numpy as np
import random
import sys
import matplotlib.pyplot as plt


class BodyNode():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setParent(self, parent):
        self.parent = parent

    def getPosition(self):
        return (self.x, self.y)

    def getIndex(self):
        return (self.y, self.x)


class Snake():
    def __init__(self, x, y):
        self.head = BodyNode(None, x, y)
        self.tail = self.head

    def moveBodyForwards(self):
        currentNode = self.tail
        while currentNode.parent != None:
            parentPosition = currentNode.parent.getPosition()
            currentNode.setX(parentPosition[0])
            currentNode.setY(parentPosition[1])
            currentNode = currentNode.parent

    def move(self, direction):
        (oldTailX, oldTailY) = self.tail.getPosition()
        self.moveBodyForwards()
        headPosition = self.head.getPosition()
        if direction == 0:
            self.head.setY(headPosition[1] - 1)
        elif direction == 1:
            self.head.setX(headPosition[0] + 1)
        elif direction == 2:
            self.head.setY(headPosition[1] + 1)
        elif direction == 3:
            self.head.setX(headPosition[0] - 1)
        return (oldTailX, oldTailY, *self.head.getPosition())

    def newHead(self, newX, newY):
        newHead = BodyNode(None, newX, newY)
        self.head.setParent(newHead)
        self.head = newHead

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail


class SnakeGame():
    def __init__(self, width, height):
        # Initialize Pygame
        pygame.init()

        # Set the dimensions of the game window
        self.cell_size = 30
        self.width = width * self.cell_size
        self.height = height * self.cell_size
        self.screen = pygame.display.set_mode(
            (self.width, self.height))
        pygame.display.set_caption("Snake Game")

        # Set up the clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        # Game variables
        self.headVal = 2
        self.bodyVal = 1
        self.foodVal = 7
        self.obstacleVal = 5
        self.board = np.zeros([height, width], dtype=int)
        self.length = 1

        startX = width // 2
        startY = height // 2

        # Initialize the snake and spawn the first food
        self.board[startX, startY] = self.headVal
        self.snake = Snake(startX, startY)
        self.spawnFood()
        self.calcState()

        # Food variables
        self.foodIndex = (0, 0)

        # Obstacle variables
        self.numObstacles = 10
        self.obstacles = []
        self.generateObstacles()

        # Game parameters
        self.numActions = 4
        self.lr = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Epsilon-greedy parameter
        self.Q = np.zeros((2**8, self.numActions))  # Q-table
        self.scores = []

    def generateObstacles(self):
        # Generate random obstacles on the board
        for _ in range(self.numObstacles):
            x = random.randint(0, self.width // self.cell_size - 1)
            y = random.randint(0, self.height // self.cell_size - 1)
            if self.board[y, x] == 0:
                self.board[y, x] = self.obstacleVal
                self.obstacles.append((x, y))

    def spawnFood(self):
        # Spawn food at a location not occupied by the snake or obstacles
        emptyCells = []
        for index, value in np.ndenumerate(self.board):
            if value == 0:
                emptyCells.append(index)
        self.foodIndex = random.choice(emptyCells)
        self.board[self.foodIndex] = self.foodVal

    def checkValid(self, direction):
        # Check if move is blocked by a wall, snake's body, or obstacle
        newX, newY = self.potentialPosition(direction)
        if newX == -1 or newX == self.width // self.cell_size:
            return False
        if newY == -1 or newY == self.height // self.cell_size:
            return False
        if self.board[newY, newX] == self.bodyVal or self.board[newY, newX] == self.obstacleVal:
            return False
        return True

    def potentialPosition(self, direction):
        # Calculate the potential position after moving in a direction
        (newX, newY) = self.snake.getHead().getPosition()
        if direction == 0:
            newY -= 1
        elif direction == 1:
            newX += 1
        elif direction == 2:
            newY += 1
        elif direction == 3:
            newX -= 1
        return (newX, newY)

    def calcState(self):
        # Calculate the state based on the snake's position and food direction
        self.state = np.zeros(8, dtype=int)
        for i in range(4):
            self.state[i] = not self.checkValid(i)
        self.state[4:] = self.calcFoodDirection()

    def calcStateNum(self):
        # Calculate an integer number for the state
        stateNum = 0
        for i in range(8):
            stateNum += 2**i * self.state[i]
        return stateNum

    def calcFoodDirection(self):
        # Calculate the direction of the food relative to the snake's head
        foodDirections = np.zeros(4, dtype=int)
        dist = np.array(self.foodIndex) - np.array(
            self.snake.getHead().getIndex())
        if dist[0] < 0:
            foodDirections[0] = 1
        elif dist[0] > 0:
            foodDirections[2] = 1
        if dist[1] > 0:
            foodDirections[1] = 1
        elif dist[1] < 0:
            foodDirections[3] = 1
        return foodDirections

    def plottableBoard(self):
        # Format the board for visualization
        board = np.zeros([self.width // self.cell_size,
                          self.height // self.cell_size])
        currentNode = self.snake.tail
        count = 0
        while True:
            count += 1
            board[currentNode.getIndex()] = 0.2 + 0.8 * count / self.length
            currentNode = currentNode.parent
            if currentNode == None:
                break
        board[self.foodIndex[1], self.foodIndex[0]] = -1
        for obs in self.obstacles:
            board[obs[1], obs[0]] = 0.5
        return board

    def display(self):
        # Display the game on the Pygame window
        self.screen.fill(self.BLACK)
        for y in range(self.height // self.cell_size):
            for x in range(self.width // self.cell_size):
                if self.board[y, x] == self.headVal:
                    pygame.draw.rect(self.screen, self.GREEN, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif self.board[y, x] == self.bodyVal:
                    pygame.draw.rect(self.screen, self.WHITE, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif self.board[y, x] == self.foodVal:
                    pygame.draw.rect(self.screen, self.RED, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif self.board[y, x] == self.obstacleVal:
                    pygame.draw.rect(self.screen, self.BLUE, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()

    def updateQTable(self, action, reward, new_state):
        # Update the Q-table using the Q-learning update rule
        self.Q[self.state, action] = self.Q[self.state, action] + self.lr * (reward + self.gamma * np.max(self.Q[new_state, :]) - self.Q[self.state, action])

    def chooseAction(self):
        # Choose an action using an epsilon-greedy policy
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.numActions - 1)
        else:
            possibleQs = self.Q[self.state, :]
            return np.argmax(possibleQs)

    def makeMove(self, direction):
        # Move the snake in the specified direction
        gameOver = False
        if self.checkValid(direction):
            if self.calcFoodDirection()[direction] == 1:
                reward = 1
            else:
                reward = 0
            (headX, headY) = self.snake.getHead().getPosition()
            self.board[headY, headX] = self.bodyVal

            potX, potY = self.potentialPosition(direction)
            if self.board[potY, potX] == self.foodVal:
                self.snake.newHead(potX, potY)
                self.board[potY, potX] = self.headVal
                self.length += 1
                reward = 2
                self.spawnFood()
            else:
                (oldTailX, oldTailY, newHeadX, newHeadY) = self.snake.move(direction)
                self.board[oldTailY, oldTailX] = 0
                self.board[newHeadY, newHeadX] = self.headVal
        else:
            reward = -2
            gameOver = True
        self.calcState()
        new_state = self.calcStateNum()
        action = self.chooseAction()
        self.updateQTable(action, reward, new_state)
        return (new_state, reward, gameOver, self.length)

    def play_game(self):
        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            action = self.chooseAction()
            new_state, reward, gameOver, score = self.makeMove(action)
            self.display()
            print("Reward:", reward, "Score:", score)
            if gameOver:
                print("Game Over, Score:", score)
                self.reset()
            self.clock.tick(10)

    def reset(self):
        # Reset the game state for a new episode
        self.board = np.zeros([self.height // self.cell_size, self.width // self.cell_size], dtype=int)
        self.generateObstacles()
        startX = self.width // (2 * self.cell_size)
        startY = self.height // (2 * self.cell_size)
        self.board[startY, startX] = self.headVal
        self.snake = Snake(startX, startY)
        self.length = 1
        self.spawnFood()
        self.calcState()

    def train(self, numEpisodes):
        # Train the snake over a specified number of episodes
        for episode in range(numEpisodes):
            gameOver = False
            score = 0
            while not gameOver:
                action = self.chooseAction()
                new_state, reward, gameOver, score = self.makeMove(action)
            self.scores.append(score)
            print("Episode:", episode, "Score:", score)
        self.plot_progress()

    def plot_progress(self):
        # Plot the training progress
        plt.plot(self.scores)
        plt.title('Training Progress')
        plt.xlabel('Episode')
        plt.ylabel('Score')
        plt.show()


if __name__ == "__main__":
    game = SnakeGame(20, 20)
    game.train(1000)  # Train for 1000 episodes
