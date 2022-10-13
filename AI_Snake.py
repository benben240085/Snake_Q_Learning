import pygame
import time
import random
import Agent

pygame.init()

# Initialize colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
grey = (169, 169, 169)
green = (0, 255, 0)
blue = (50, 153, 213)

MAX_MOVES = 3000

# Initialize width and height
dis_width = 400
dis_height = 400

# Set up display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake')

# Set up clock
clock = pygame.time.Clock()

# Set how much the snake moves per tick
snake_block = 20

# Set often the clock ticks
q_vals_n = 50
snake_speed = 20



# Set fonts for the game
font_style = pygame.font.SysFont("bahnschrift", 15)
score_font = pygame.font.SysFont("bahnschrift", 15)


def your_score(score):
    # Drawing score
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [10, 10])


def our_snake(snake_block, snake_list):
    # Drawing snake
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    # Displaying message
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def get_new_position(object_list):
    # Get new position, given a list of objects to avoid
    while True:
        position = (round(random.randrange(0, dis_width - snake_block) / snake_block) *
                    snake_block, round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block)
        if position not in object_list:
            return position


def gameLoop():
    # Initial game conditions
    game_over = False
    reason = None

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = [(x1, y1)]
    length_of_snake = 1

    wall_list = []

    foodx, foody = get_new_position(snake_list)
    bad_foodx, bad_foody = get_new_position(snake_list)

    score = 0
    moves = 0

    while not game_over or moves == MAX_MOVES:
        # Agent moves snake
        action = agent.act(snake_list, (foodx,foody), (bad_foodx, bad_foody), wall_list)
        if action == "L" and x1_change != snake_block:
            x1_change = -snake_block
            y1_change = 0
        elif action == "R" and x1_change != -snake_block:
            x1_change = snake_block
            y1_change = 0
        elif action == "U" and y1_change != snake_block:
            y1_change = -snake_block
            x1_change = 0
        elif action == "D" and y1_change != -snake_block:
            y1_change = snake_block
            x1_change = 0

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        snake_head = (x1, y1)
        snake_list.append(snake_head)

        # Game over conditions (off-screen)
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over, reason = True, "Off-Screen"
        # Check if bad food was found
        if x1 == bad_foodx and y1 == bad_foody:
            bad_foodx, bad_foody = get_new_position(
                snake_list + wall_list + [(foodx, foody)])
            score -= 2
        # If you ate a bad fruit at 0 score, it is game over
        if score < 0:
            game_over, reason = True, "Bad Fruit"
        # Self colision
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over, reason = True, "Self-Collision"
        # Has collided with wall, then it is game over
        if snake_head in wall_list:
            game_over, reason = True, "Wall-Collision"
        
        # Check if food was found
        if x1 == foodx and y1 == foody:
            wall_list.append(get_new_position(wall_list + snake_list))
            foodx, foody = get_new_position(snake_list + wall_list)
            bad_foodx, bad_foody = get_new_position(
                snake_list + wall_list + [(foodx, foody)])
            length_of_snake += 1
            score += 1

        # Delete tail
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Draw background
        dis.fill(blue)
        # Draw good food
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        # Draw bad food
        pygame.draw.rect(
            dis, red, [bad_foodx, bad_foody, snake_block, snake_block])
        # Draw walls
        for wall in wall_list:
            pygame.draw.rect(
                dis, grey, [wall[0], wall[1], snake_block, snake_block])

        # Draw
        our_snake(snake_block, snake_list)
        your_score(score)

        pygame.display.update()

        # Update Q Table
        agent.UpdateQValues(reason)
        moves += 1
        clock.tick(snake_speed)

    return score, reason


game_count = 1

agent = Agent.Agent(dis_width, dis_height, snake_block)

while True:
    agent.Reset()
    if game_count > 100:
        agent.epsilon = 0
    else:
        agent.epsilon = .1
    score, reason = gameLoop()
    print(f"Games: {game_count}; Score: {score}; Reason: {reason}") # Output results of each game to console to monitor as agent is training
    game_count += 1
    if game_count % q_vals_n == 0: # Save qvalues every qvalue_dump_n games
        print("Save Qvals")
        agent.SaveQvalues()