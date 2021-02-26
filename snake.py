import pygame
import random


class EmptyCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pass


class Level:
    def __init__(self, level_number):
        self.level_cells_content = [[EmptyCell(x, y) for x in range(windowWidth//cellEdgeLength)]
                                    for y in range(windowHeight//cellEdgeLength)]
        if level_number == 1:
            self.create_shape(1, 1, 10, 2)
            self.create_shape(1, 1, 2, 10)
            self.create_shape(46, 18, 47, 28)
            self.create_shape(37, 27, 47, 28)

        if level_number == 2:
            self.create_shape(0, 0, 10, 1)
            self.create_shape(0, 0, 1, 10)
            self.create_shape(47, 18, 48, 29)
            self.create_shape(37, 28, 48, 29)

        if level_number == 3:
            self.create_shape(1, 1, 2, 15)
            self.create_shape(10, 1, 11, 15)
            self.create_shape(20, 1, 21, 15)
            self.create_shape(30, 1, 31, 15)

        if level_number == 4:
            self.create_shape(1, 1, 11, 2)
            self.create_shape(10, 1, 11, 15)
            self.create_shape(20, 1, 21, 15)

    def create_shape(self, start_x, start_y, end_x, end_y):
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                self.level_cells_content[y][x] = Wall(x, y)


class GameField:
    def __init__(self, level_map):
        self.cells_content = level_map.level_cells_content

    def replace_block_id(self, x, y, block):
        self.cells_content[y][x] = block

    def check_for_obstacles(self, x, y):
        try:
            content_found = self.cells_content[y][x]
        except IndexError:
            return "BORDER"
        if type(content_found) == EmptyCell:
            return "EMPTY"
        elif type(content_found) == Rock:
            return "ROCK"
        elif type(content_found) == Wall:
            return "WALL"

    def check_for_borders(self, coord, direction):
        if direction == "RIGHT":
            if coord >= windowWidth//cellEdgeLength - 1:
                return True
        elif direction == "LEFT" or direction == "UP":
            if coord == 0:
                return True
        elif direction == "DOWN":
            if coord >= windowHeight//cellEdgeLength - 1:
                return True
        return False

    def draw(self):
        for column in self.cells_content:
            for cell in column:
                cell.draw()


class SnakeHead:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.last_x = x
        self.last_y = y

    def set_direction(self, direction):
        self.direction = direction

    def move(self):
        if snake.check_for_collisions():
            return True
        if self.direction == "RIGHT":
            right_tile_content = gameField.check_for_obstacles(self.x + 1, self.y)
            is_border_reached = gameField.check_for_borders(self.x, self.direction)
            if is_border_reached:
                right_tile_content = gameField.check_for_obstacles(0, self.y)
                self.last_x = self.x
                self.last_y = self.y
                self.x = -1
            if right_tile_content == "ROCK":
                self.last_x = self.x
                self.last_y = self.y
                self.x += 1
                self.send_messages()
            elif right_tile_content == "EMPTY":
                self.last_x = self.x
                self.last_y = self.y
                self.x += 1
            elif right_tile_content == "WALL":
                return True
            return False
        if self.direction == "DOWN":
            right_tile_content = gameField.check_for_obstacles(self.x, self.y + 1)
            is_border_reached = gameField.check_for_borders(self.y, self.direction)
            if is_border_reached:
                right_tile_content = gameField.check_for_obstacles(self.x, 0)
                self.last_x = self.x
                self.last_y = self.y
                self.y = -1
            if right_tile_content == "ROCK":
                self.last_x = self.x
                self.last_y = self.y
                self.y += 1
                self.send_messages()
            elif right_tile_content == "EMPTY":
                self.last_x = self.x
                self.last_y = self.y
                self.y += 1
            elif right_tile_content == "WALL":
                return True
        if self.direction == "LEFT":
            right_tile_content = gameField.check_for_obstacles(self.x - 1, self.y)
            is_border_reached = gameField.check_for_borders(self.x, self.direction)
            if is_border_reached:
                right_tile_content = gameField.check_for_obstacles(windowWidth//cellEdgeLength - 1, self.y)
                self.last_x = self.x
                self.last_y = self.y
                self.x = windowWidth//cellEdgeLength
            if right_tile_content == "ROCK":
                self.last_x = self.x
                self.last_y = self.y
                self.x -= 1
                self.send_messages()
            elif right_tile_content == "EMPTY":
                self.last_x = self.x
                self.last_y = self.y
                self.x -= 1
            elif right_tile_content == "WALL":
                return True
        if self.direction == "UP":
            right_tile_content = gameField.check_for_obstacles(self.x, self.y - 1)
            is_border_reached = gameField.check_for_borders(self.y, self.direction)
            if is_border_reached:
                right_tile_content = gameField.check_for_obstacles(self.x, windowHeight//cellEdgeLength - 1)
                self.last_x = self.x
                self.last_y = self.y
                self.y = windowHeight//cellEdgeLength
            if right_tile_content == "ROCK":
                self.last_x = self.x
                self.last_y = self.y
                self.y -= 1
                self.send_messages()
            elif right_tile_content == "EMPTY":
                self.last_x = self.x
                self.last_y = self.y
                self.y -= 1

            elif right_tile_content == "WALL":
                return True

    def send_messages(self):
        gameField.replace_block_id(currentRock.x, currentRock.y, EmptyCell(currentRock.x, currentRock.y))
        currentRock.set_status(True)
        snake.add_tile()


class SnakeTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = "DEFAULT"
        self.last_x = x
        self.last_y = y
        self.is_new = True

    def move(self, x, y):
        self.last_x = self.x
        self.last_y = self.y
        self.x = x
        self.y = y

    def draw(self):
        gameScreen.blit(pygame.image.load("SnakeBodyNew.png"), (self.x * cellEdgeLength, self.y * cellEdgeLength))


class Snake:
    def __init__(self, snake_head):
        self.head = snake_head
        self.body = []

    def add_tile(self):
        self.body.insert(0, SnakeTile(self.head.last_x, self.head.last_y))

    def move(self):
        for tileIndex in range(len(self.body)):
            if tileIndex == 0:
                if self.body[tileIndex].is_new:
                    self.body[tileIndex].is_new = False
                else:
                    self.body[tileIndex].move(self.head.last_x, self.head.last_y)
            else:
                if self.body[0].is_new:
                    self.body[tileIndex].move(self.body[tileIndex].last_x, self.body[tileIndex].last_y)
                else:
                    self.body[tileIndex].move(self.body[tileIndex - 1].last_x, self.body[tileIndex - 1].last_y)

    def draw(self):
        for tile in self.body:
            tile.draw()

    def check_for_collisions(self):
        if self.head.direction == "RIGHT":
            x_check = self.head.x + 1
            y_check = self.head.y
        elif self.head.direction == "LEFT":
            x_check = self.head.x - 1
            y_check = self.head.y
        elif self.head.direction == "UP":
            x_check = self.head.x
            y_check = self.head.y - 1
        elif self.head.direction == "DOWN":
            x_check = self.head.x
            y_check = self.head.y + 1
        for tile in self.body:
            if tile.x == x_check and tile.y == y_check:
                return True
        return False


class Rock:
    def __init__(self):
        self.x = random.randint(0, 47)
        self.y = random.randint(0, 20)
        while gameField.check_for_obstacles(self.x, self.y) != "EMPTY":
            self.x = random.randint(0, 47)
            self.y = random.randint(0, 20)
        self.is_eaten = False

    def draw(self):
        gameScreen.blit(pygame.image.load("Rock.png"), (self.x * cellEdgeLength, self.y * cellEdgeLength))

    def set_status(self, status):
        self.is_eaten = status


class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        gameScreen.blit(pygame.image.load("SnakeBlock.png"), (self.x * cellEdgeLength, self.y * cellEdgeLength))


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    WHITE = (255, 255, 255)
    mainFont = pygame.font.Font(None, 200)
    scoreFont = pygame.font.Font(None, 40)
    windowHeight = 725
    windowWidth = 1200
    cellEdgeLength = 25
    gameScreen = pygame.display.set_mode((windowWidth, windowHeight))
    FPS = 60
    isRunning = True
    levelNumber = random.randint(1, 4)
    level = Level(levelNumber)
    gameField = GameField(level)
    snakeHead = SnakeHead(15, 15, 0)
    snake = Snake(snakeHead)
    fpsController = pygame.time.Clock()
    if levelNumber == 2 or levelNumber == 3:
        snakeMoveSpeed = 3
    else:
        snakeMoveSpeed = 3
    timeSinceGameStart = 0
    currentRock = Rock()
    gameField.replace_block_id(currentRock.x, currentRock.y, currentRock)
    score = 0
    score_multiplier = 5
    isSnakeAlive = True

    while isRunning:
        fpsController.tick(FPS)
        timeSinceGameStart += 1
        if isSnakeAlive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        snakeHead.set_direction("RIGHT")
                    if event.key == pygame.K_s:
                        snakeHead.set_direction("DOWN")
                    if event.key == pygame.K_a:
                        snakeHead.set_direction("LEFT")
                    if event.key == pygame.K_w:
                        snakeHead.set_direction("UP")

            if timeSinceGameStart % snakeMoveSpeed == 0:
                if snakeHead.move():
                    isSnakeAlive = False
                snake.move()
            if currentRock.is_eaten:
                score += score_multiplier
                currentRock = Rock()
                gameField.replace_block_id(currentRock.x, currentRock.y, currentRock)
            gameScreen.fill(WHITE)
            gameScreen.blit(pygame.image.load("SnakeTheeth.png"),
                            (snakeHead.x * cellEdgeLength, snakeHead.y * cellEdgeLength))
            scoreMessage = scoreFont.render("score: " + str(score), True, (0, 0, 0))
            gameScreen.blit(scoreMessage, (windowWidth * 0.9, windowHeight * 0.05))
            snake.draw()
            currentRock.draw()
            gameField.draw()
            pygame.display.update()
        else:
            deathMessage = mainFont.render("GAME OVER", True, (255, 0, 0))
            restartButtonMessage1 = mainFont.render("PRESS SPACE", True, (255, 0, 0))
            restartButtonMessage2 = mainFont.render("TO RESTART", True, (255, 0, 0))
            scoreReachedMessage = scoreFont.render("Your score: " + str(score), True, (0, 0, 0))
            gameScreen.blit(deathMessage, (windowWidth * 0.12, windowHeight * 0.1))
            gameScreen.blit(restartButtonMessage1, (windowWidth * 0.1, windowHeight * 0.3))
            gameScreen.blit(restartButtonMessage2, (windowWidth * 0.12, windowHeight * 0.5))
            gameScreen.blit(scoreReachedMessage, (windowWidth * 0.4, windowHeight * 0.7))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        isSnakeAlive = True
                        levelNumber = random.randint(1, 4)
                        level = Level(levelNumber)
                        gameField = GameField(level)
                        snakeHead = SnakeHead(15, 15, 0)
                        snake = Snake(snakeHead)
                        timeSinceGameStart = 0
                        if levelNumber == 2 or levelNumber == 3:
                            snakeMoveSpeed = 3
                        else:
                            snakeMoveSpeed = 3
                        currentRock = Rock()
                        gameField.replace_block_id(currentRock.x, currentRock.y, currentRock)
                        score = 0
    pygame.quit()

