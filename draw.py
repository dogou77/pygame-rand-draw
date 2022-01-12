import pygame
import random
import math
import sys
  
pygame.init()



class Button:
    # initializes button with 4 parameters
    def __init__(self, position_x, position_y, size_x, size_y):
        self.position         = [position_x, position_y]
        self.size             = [size_x, size_y]
        self.position_end     = [position_x + size_x, position_y + size_y] # gets the lower right hand corner of the button
        self.position_center  = [((position_x * 2) + size_x) / 2, ((position_y * 2) + size_y) / 2] # gets the center of the button with midpoint formula

    # renders the button
    def render(self, screen, mouse, color_hover, color_neut, text_font, text_str, text_color):
        # if the mouse is over the button, draw a rectangle over it, if not then draw the neutral rectangle
        if self.position[0] <= mouse[0] <= self.position_end[0] and self.position[1] <= mouse[1] <= self.position_end[1]:
            pygame.draw.rect(screen, color_hover, [self.position[0], self.position[1], self.size[0], self.size[1]])
        else:
            pygame.draw.rect(screen, color_neut, [self.position[0], self.position[1], self.size[0], self.size[1]])
        # gets the text size for calculating where to put it
        text_size = text_font.size(text_str)
        text = text_font.render(text_str, True , text_color)
        # renders the text at the center of the button
        screen.blit(text , (self.position_center[0] - (text_size[0] / 2), self.position_center[1] - (text_size[1] / 2)))

    # gets the state of the button, if the mouse is in the button, then return true
    def get_state(self, mouse):
        if self.position[0] <= mouse[0] <= self.position_end[0] and self.position[1] <= mouse[1] <= self.position_end[1]:
            return True
        else:
            return False



class CheckBox:
    def __init__(self, default_state, position_x, position_y, size_x, size_y, check_margin):
        self.state            = default_state
        self.position         = [position_x, position_y]
        self.size             = [size_x, size_y]
        self.position_end     = [position_x + size_x, position_y + size_y] # gets the lower right hand corner of the checkbox
        self.position_center  = [((position_x * 2) + size_x) / 2, ((position_y * 2) + size_y) / 2] # gets the center of the checkbox with midpoint formula
        self.check_margin     = check_margin
        
    # renders the check box
    def render(self, screen, mouse, color_hover, color_neut, color_confirm):
        pygame.draw.rect(screen, color_neut, [self.position[0], self.position[1], self.size[0], self.size[1]])

        # if the mouse is over the button, draw a rectangle over it, if not then draw the neutral rectangle
        if self.state:
            pygame.draw.rect(screen, color_confirm, [self.position[0] + self.check_margin, self.position[1] + self.check_margin, self.size[0] - (self.check_margin * 2), self.size[1] - (self.check_margin * 2)])
        if self.position[0] <= mouse[0] <= self.position_end[0] and self.position[1] <= mouse[1] <= self.position_end[1]:
            pygame.draw.rect(screen, color_hover, [self.position[0] + self.check_margin, self.position[1] + self.check_margin, self.size[0] - (self.check_margin * 2), self.size[1] - (self.check_margin * 2)])

    def toggle(self, mouse):
        if self.position[0] <= mouse[0] <= self.position_end[0] and self.position[1] <= mouse[1] <= self.position_end[1]:
            self.state = not self.state



def draw_centered_text(screen, text_font, text_str, text_color, position_x, position_y):
    text_size = text_font.size(text_str)
    text = text_font.render(text_str, True , text_color)
    # renders the text at the center of the button
    screen.blit(text , (position_x - (text_size[0] / 2), position_y - (text_size[1] / 2)))



def screen_menu_main(screen):
    global state_current
    global run_once
    run_once = False

    font = pygame.font.SysFont('Arial',35)

    # buttons
    button_draw_point = Button(50, 50, 500, 100)
    button_draw_lines = Button(50, 200, 500, 100)
    button_quit       = Button(50, 800, 500, 100)

    # gets the position of the mouse as a vector
    mouse = pygame.mouse.get_pos()

    # pygame event queue
    for ev in pygame.event.get():
        # window is closed
        if ev.type == pygame.QUIT:
            pygame.quit()
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # gets the states of multiple buttons, if the mouse was in them when clicked, then go to next state
            if button_draw_point.get_state(mouse):
                state_current = "PointDrawMenu"
            if button_draw_lines.get_state(mouse):
                state_current = "DrawLinesCenter"
            if button_quit.get_state(mouse):
                pygame.quit()
    # fills the screen with a color
    screen.fill(PURPLE)

    # renders the buttons
    button_draw_point.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, font, 'Point Drawer', WHITE)
    button_draw_lines.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, font, 'Lines (Center)', WHITE)
    button_quit.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, font, 'Quit', WHITE)

    # updates the frames of the game
    pygame.display.update()



def screen_menu_draw_pointer(screen):
    global state_current

    running = True
    info = {
        "sym_x": False,
        "sym_y": False,
        "color": False,
    }
    
    check_box_sym_x = CheckBox(False, 150, 200, 100, 100, 10)
    check_box_sym_y = CheckBox(False, 450, 200, 100, 100, 10)
    check_box_color = CheckBox(False, 750, 200, 100, 100, 10)

    button_back = Button(50, 800, 400, 100)
    button_next = Button(550, 800, 400, 100)

    font_title = pygame.font.SysFont('Arial', 50)
    font_check_box = pygame.font.SysFont('Arial', 40)


    while running:
        mouse = pygame.mouse.get_pos()

        # pygame event queue
        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()
            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                check_box_sym_x.toggle(mouse)
                check_box_sym_y.toggle(mouse)
                check_box_color.toggle(mouse)
                if button_back.get_state(mouse):
                    state_current = "MainMenu"
                    running = False
                if button_next.get_state(mouse):
                    state_current = "PointDraw"
                    running = False

        screen.fill(PURPLE)
        check_box_sym_x.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)
        check_box_sym_y.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)
        check_box_color.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)

        button_back.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, font_title, "Back", WHITE)
        button_next.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, font_title, "Next", WHITE)

        draw_centered_text(screen, font_title, "Point Drawer Options", WHITE, 500, 50)
        draw_centered_text(screen, font_check_box, "X-Axis Symmetry", WHITE, 200, 150)
        draw_centered_text(screen, font_check_box, "Y-Axis Symmetry", WHITE, 500, 150)
        draw_centered_text(screen, font_check_box, "Color", WHITE, 800, 150)
        # updates the frames of the game
        pygame.display.update()

    info["sym_x"] = check_box_sym_x.state
    info["sym_y"] = check_box_sym_y.state
    info["color"] = check_box_color.state
    return info



def screen_draw_pointer(pixel, screen, info):
    color = BLACK
    screen.fill(WHITE)
    r = 125
    g = 125
    b = 125
    running = True

    while running:
        if info["color"]:
            color_rand = random.randrange(0, 3, 1)
            color_up_down = random.randrange(0, 2, 1)
            color = (r, g, b)
            match color_rand:
                case 0:
                    match color_up_down:
                        case 0:
                            r += 1
                            if r >= 255:
                                r -= 1
                        case 1:
                            r -= 1
                            if r <= 1:
                                r += 1
                case 1:
                    match color_up_down:
                        case 0:
                            g += 1
                            if g >= 255:
                                g -= 1
                        case 1:
                            g -= 1
                            if g <= 0:
                                g += 1
                case 2:
                    match color_up_down:
                        case 0:
                            b += 1
                            if b >= 255:
                                b -= 1
                        case 1:
                            b -= 1
                            if b <= 1:
                                b += 1

        # generate a random number
        rand_num = random.randrange(1, 10, 1)

        # match random number to corresponding direction based on numpad
        match rand_num:
            case 1:
                pixel[0] -= 1
                pixel[1] -= 1
            case 2:
                pixel[1] -= 1
            case 3:
                pixel[0] += 1
                pixel[1] -= 1
            case 4:
                pixel[0] -= 1
            case 5:
                pixel[0] += 0
                pixel[1] += 0
            case 6:
                pixel[0] += 1
            case 7: 
                pixel[0] -= 1
                pixel[1] += 1
            case 8:
                pixel[1] += 1
            case 9:
                pixel[0] += 1
                pixel[1] += 1

        # pygame event queue
        for ev in pygame.event.get():
            # window close
            if ev.type == pygame.QUIT:
                pygame.quit()

        # draw a pixel
        screen.fill(color, ([pixel[0], pixel[1]], (1, 1)))
        if info["sym_x"]:
            screen.fill(color, ([pixel[0], -pixel[1]+1000], (1, 1)))
        if info["sym_y"]:
            screen.fill(color, ([-pixel[0]+1000, pixel[1]], (1, 1)))
        if info["sym_x"] and info["sym_y"]:
            screen.fill(color, ([-pixel[0]+1000, -pixel[1]+1000], (1, 1)))
        # update display
        pygame.display.update()
    return pixel



def screen_draw_lines_center(screen):
    global run_once

    # fills the screen once
    if run_once == False:
        screen.fill(WHITE)
        run_once = True

    radius = 500

    # generate a random number representing a point on the edge of a circle
    randNum = random.random()*(2*math.pi)
    # convert the polar coordinates to rectangular to draw a line
    pygame.draw.line(screen, BLACK, (500, 500), ((radius*math.cos(randNum))+500, (radius*math.sin(randNum))+500))



# constants
RES = (1000, 1000)

# colors
GREEN        = (  0, 255,   0)
BLACK        = (  0,   0,   0)
WHITE        = (255, 255, 255)
PURPLE       = ( 60,  25,  60)
BUTTON_LIGHT = (170, 170, 170)
BUTTON_DARK  = (100, 100, 100)

# global variables
state_current = "MainMenu"
run_once = False

# variables
pixel = [500, 500]

# opens up a window
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
symtest = [False, False]

# main loop
while True:
    #clock.tick(60)
    if state_current == "MainMenu":
        screen_menu_main(screen)
    if state_current == "PointDrawMenu":
        point_draw_info = screen_menu_draw_pointer(screen)
    if state_current == "PointDraw":
        pixel = screen_draw_pointer(pixel, screen, point_draw_info)
    if state_current == "DrawLinesCenter":
        screen_draw_lines_center(screen)
