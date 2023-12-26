from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from tkinter import *
from pickle import dump, load
pygame.init()
surface = pygame.display.set_mode((1935, 1040))
 
#def set_difficulty(value, difficulty):
    #print(value)
    #print(difficulty)
 
def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)
    import turtle
    import random
    w = 1000
    h = 500
    food_size = 10
    delay = 100

    offsets = {
        "w": (0, 20),
        "s": (0, -20),
        "a": (-20, 0),
        "d": (20, 0)
    }

    score = 0

    def reset():
        global snake, snake_dir, food_position, pen, score
        snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
        snake_dir = "w"
        food_position = get_random_food_position()
        food.goto(food_position)
        move_snake()
        score = 0
        update_score()

    def move_snake():
        global snake_dir, score

        new_head = snake[-1].copy()
        new_head[0] = snake[-1][0] + offsets[snake_dir][0]
        new_head[1] = snake[-1][1] + offsets[snake_dir][1]
        

        if new_head in snake[:-1]:
            reset()
        else:
            snake.append(new_head)

            if not food_collision():
                snake.pop(0)

            if snake[-1][0] > w / 2:
                snake[-1][0] -= w
            elif snake[-1][0] < -w / 2:
                snake[-1][0] += w
            elif snake[-1][1] > h / 2:
                snake[-1][1] -= h
            elif snake[-1][1] < -h / 2:
                snake[-1][1] += h

            pen.clearstamps()

            for segment in snake:
                pen.goto(segment[0], segment[1])
                pen.stamp()

            screen.update()

            turtle.ontimer(move_snake, delay)

    def food_collision():
        global food_position, score
        if get_distance(snake[-1], food_position) < 20:
            score += 1
            update_score()
            food_position = get_random_food_position()
            food.goto(food_position)
            return True
        return False

    def get_random_food_position():
        x = random.randint(-w / 2 + food_size, w / 2 - food_size)
        y = random.randint(-h / 2 + food_size, h / 2 - food_size)
        return (x, y)

    def get_distance(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        return distance
    
    def update_score():
        pen_score.clear()
        pen_score.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

    def update_score():
        pen_score.clear()
        pen_score.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

    def go_up():
        global snake_dir
        if snake_dir != "s":
            snake_dir = "w"

    def go_right():
        global snake_dir
        if snake_dir != "a":
            snake_dir = "d"

    def go_down():
        global snake_dir
        if snake_dir != "w":
            snake_dir = "s"

    def go_left():
        global snake_dir
        if snake_dir != "d":
            snake_dir = "a"

    screen = turtle.Screen()
    screen.setup(w, h)
    screen.title("Snake")
    screen.bgcolor("pink")
    screen.tracer(0)

    pen = turtle.Turtle("square")
    pen.color("black")
    pen.penup()

    pen_score = turtle.Turtle()
    pen_score.color("black")
    pen_score.penup()
    pen_score.goto(0, 220)
    pen_score.hideturtle()
    update_score()

    food = turtle.Turtle()
    food.shape("circle")
    food.color("red")
    food.shapesize(food_size / 20)
    food.penup()

    screen.listen()
    screen.onkey(go_up, "w")
    screen.onkey(go_right, "d")
    screen.onkey(go_down, "s")
    screen.onkey(go_left, "a")

    screen.listen()
    screen.onkey(go_up, "W")
    screen.onkey(go_right, "D")
    screen.onkey(go_down, "S")
    screen.onkey(go_left, "A")

    reset()
    turtle.done()
 
#def level_menu():
    #mainmenu._open(level)
 
 
mainmenu = pygame_menu.Menu('Добро пожаловать', 1935, 1040, theme=themes.THEME_SOLARIZED)
#mainmenu.add.text_input('Name: ', default='username')
mainmenu.add.button('Начать игру', start_the_game)
#mainmenu.add.button('Levels', level_menu)
mainmenu.add.button('Выйти', pygame_menu.events.EXIT)
 
#level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=themes.THEME_BLUE)
#level.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
 
loading = pygame_menu.Menu('Выход справа', 1000, 500, theme=themes.THEME_DARK)
#loading.add.progress_bar("Прогресс", progressbar_id = "1", default=0, width = 200, )
 
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))
 
update_loading = pygame.USEREVENT + 0
 
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            #progress.set_value(progress.get_value() + 1)
            #if progress.get_value() == 100:
                #pygame.time.set_timer(update_loading, 0)
        if event.type == pygame.QUIT:
            exit()
 
    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())
 
    pygame.display.update()

