import pygame
import random
import math
import sys
  
pygame.init()



# buttons are drawn as a rectangle from (position_x, position_y) to (position_x+size_x, postion_y+size_y) and return a true or false when pressed
class Button:
    # initializes button with 4 parameters
    def __init__(self, position_x, position_y, size_x, size_y):
        self.position        = [position_x, position_y]
        self.size            = [size_x, size_y]
        self.position_end    = [position_x + size_x, position_y + size_y] # gets the lower right hand corner of the button
        self.position_center = [((position_x * 2) + size_x) / 2, ((position_y * 2) + size_y) / 2] # gets the center of the button with midpoint formula

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



# check boxes are drawn as a rectangle from (position_x, position_y) to (position_x+size_x, postion_y+size_y) and store a state based on if they have been toggled
class CheckBox:
    # initializes the check box based on 6 parameters
    def __init__(self, default_state, position_x, position_y, size_x, size_y, check_margin):
        self.state           = default_state
        self.position        = [position_x, position_y]
        self.size            = [size_x, size_y]
        self.position_end    = [position_x + size_x, position_y + size_y] # gets the lower right hand corner of the checkbox
        self.position_center = [((position_x * 2) + size_x) / 2, ((position_y * 2) + size_y) / 2] # gets the center of the checkbox with midpoint formula
        self.check_margin    = check_margin
        
    # renders the check box
    def render(self, screen, mouse, color_hover, color_neut, color_confirm):
        # draw the outline of the check box
        pygame.draw.rect(screen, color_neut, [self.position[0], self.position[1], self.size[0], self.size[1]])

        # if the mouse is over the checkbox, draw a rectangle in it, if the state is true, draw a green rectangle in it
        if self.state:
            pygame.draw.rect(screen, color_confirm, [self.position[0] + self.check_margin, self.position[1] + self.check_margin, self.size[0] - (self.check_margin * 2), self.size[1] - (self.check_margin * 2)])
        if self.position[0] <= mouse[0] <= self.position_end[0] and self.position[1] <= mouse[1] <= self.position_end[1]:
            pygame.draw.rect(screen, color_hover, [self.position[0] + self.check_margin, self.position[1] + self.check_margin, self.size[0] - (self.check_margin * 2), self.size[1] - (self.check_margin * 2)])

    # toggles the check boxes state if it is in the mouse position
    def toggle(self, mouse):
        if self.position[0] <= mouse[0] <= self.position_end[0] and self.position[1] <= mouse[1] <= self.position_end[1]:
            self.state = not self.state



# radio buttons are drawn as circles from the center of (position_x, position_y) with a radius, work just like check boxes with a state
class RadioButton:
    # initializes the radio button based on 5 parameters
    def __init__(self, default_state, position_x, position_y, radius, confirm_margin):
        self.state          = default_state
        self.position       = [position_x, position_y]
        self.radius         = radius
        self.confirm_margin = confirm_margin
        self.collision_pos  = [position_x - radius, position_y - radius, position_x + radius, position_y + radius]


    def render(self, screen, mouse, color_hover, color_neut, color_confirm):
        # draw the outline of the radio button
        pygame.draw.circle(screen, color_neut, [self.position[0], self.position[1]], self.radius)

        # if the mouse is over the radio button, draw a circle in it, if the state is true, draw a green circle in it
        if self.state:
            pygame.draw.circle(screen, color_confirm, [self.position[0], self.position[1]], self.radius - self.confirm_margin)
        if self.collision_pos[0] <= mouse[0] <= self.collision_pos[2] and self.collision_pos[1] <= mouse[1] <= self.collision_pos[3]:
            pygame.draw.circle(screen, color_hover, [self.position[0], self.position[1]], self.radius - self.confirm_margin)

    # toggles the radio button state
    def toggle(self, mouse):
        if self.collision_pos[0] <= mouse[0] <= self.collision_pos[2] and self.collision_pos[1] <= mouse[1] <= self.collision_pos[3]:
            self.state = not self.state



# draws text centered at the specified point
def draw_centered_text(screen, text_font, text_str, text_color, position_x, position_y):
    text_size = text_font.size(text_str)
    text = text_font.render(text_str, True , text_color)
    # renders the text at the center of the position provided
    screen.blit(text , (position_x - (text_size[0] / 2), position_y - (text_size[1] / 2)))



# main menu screen
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



# options screen for draw pointer
def screen_menu_draw_pointer(screen):
    # set the state_current to global so that it can change states
    global state_current

    running = True
    # info is the variable that is returned
    info = {
        "sym_x"    : False,
        "sym_y"    : False,
        "color_a"  : False,
        "color_b"  : False,
        "overwrite": False,
        "borders"  : False,
    }
    # initializes a list that is supposed to contain multiple radio buttons so that two are not active at once
    radio_buttons = []

    # initialize check boxes
    check_box_sym_x     = CheckBox(False, 300, 200, 100, 100, 10)
    check_box_sym_y     = CheckBox(False, 600, 200, 100, 100, 10)
    check_box_overwrite = CheckBox(False, 300, 600, 100, 100, 10)
    check_box_borders   = CheckBox(False, 600, 600, 100, 100, 10)

    # initialize radio buttons and add them to the radio_button list
    radio_color_a = RadioButton(False, 350, 450, 50, 10)
    radio_color_b = RadioButton(False, 650, 450, 50, 10)
    radio_buttons.append(radio_color_a)
    radio_buttons.append(radio_color_b)

    # initalize back and forward buttons
    button_back = Button(50, 800, 400, 100)
    button_next = Button(550, 800, 400, 100)

    # initialize fonts
    font_title = pygame.font.SysFont('Arial', 50)
    font_check_box = pygame.font.SysFont('Arial', 40)


    while running:
        mouse = pygame.mouse.get_pos()

        # pygame event queue
        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()
            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # toggles the check boxes if the mouse is in their area
                check_box_sym_x.toggle(mouse)
                check_box_sym_y.toggle(mouse)
                check_box_overwrite.toggle(mouse)
                check_box_borders.toggle(mouse)

                # toggles the radio button in the mouse is in their area, but untoggled ones that are already true
                for radio in radio_buttons:
                    radio.toggle(mouse)
                    if radio.state:
                        for rad in radio_buttons:
                            if rad != radio:
                                rad.state = False

                # gets the states of the back and next buttons then sets a state and exits the loop
                if button_back.get_state(mouse):
                    state_current = "MainMenu"
                    running = False
                if button_next.get_state(mouse):
                    state_current = "PointDraw"
                    running = False

        screen.fill(PURPLE)

        # render the check boxes
        check_box_sym_x.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)
        check_box_sym_y.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)
        check_box_overwrite.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)
        check_box_borders.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)

        # render the radio buttons
        radio_color_a.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)
        radio_color_b.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, GREEN)

        # render the buttons
        button_back.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, font_title, "Back", WHITE)
        button_next.render(screen, mouse, BUTTON_LIGHT, BUTTON_DARK, font_title, "Next", WHITE)

        # draw all the text
        draw_centered_text(screen, font_title, "Point Drawer Options", WHITE, 500, 50)
        draw_centered_text(screen, font_check_box, "X-Axis Symmetry", WHITE, 350, 150)
        draw_centered_text(screen, font_check_box, "Y-Axis Symmetry", WHITE, 650, 150)
        draw_centered_text(screen, font_check_box, "Color Mode A", WHITE, 350, 350)
        draw_centered_text(screen, font_check_box, "Color Mode B", WHITE, 650, 350)
        draw_centered_text(screen, font_check_box, "Overwrite", WHITE, 350, 550)
        draw_centered_text(screen, font_check_box, "Borders", WHITE, 650, 550)

        # updates the frames of the game
        pygame.display.update()

    # set up the return values for info based on the check box states and radio button states
    info["sym_x"]     = check_box_sym_x.state
    info["sym_y"]     = check_box_sym_y.state
    info["color_a"]   = radio_color_a.state
    info["color_b"]   = radio_color_b.state
    info["overwrite"] = check_box_overwrite.state
    info["borders"]   = check_box_borders.state
    return info



# draw pointer screen
def screen_draw_pointer(pixel, screen, info):
    global state_current

    # set default color to black
    color = BLACK
    screen.fill(WHITE)

    # set default rgb colors to gray for color mode a usage
    r = 125
    g = 125
    b = 125

    running = True

    while running:

        if pygame.key.get_focused():
            if pygame.key.get_pressed()[pygame.K_F12]:
                pygame.image.save(screen, "image.png")
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False
        # if the user selected color mode a in the previous screen
        if info["color_a"]:
            # generate a random number from 0 to 2, this selects what rgb value is going to be modified
            color_rand = random.randrange(0, 3, 1)
            # generate a random number from 0 to 1, this selects if the selected rgb value is going to be incremented or decremented
            color_up_down = random.randrange(0, 2, 1)
            color = (r, g, b)
            match color_rand:
                # r
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
                # g
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
                # b
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

        # if the user selected color mode b
        elif info["color_b"]:
            # randomizes all color values and sets them equal to color
            rand_r = random.randrange(1, 255, 1)
            rand_g = random.randrange(1, 255, 1)
            rand_b = random.randrange(1, 255, 1)
            color = (rand_r, rand_g, rand_b)

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

        # prevents the pointer from leaving the screen if option borders is enabled
        if pixel[0] >= 1000 and info["borders"]:
            pixel[0] -= 1
        if pixel[0] <= 0 and info["borders"]:
            pixel[0] += 1
        if pixel[1] >= 1000 and info["borders"]:
            pixel[1] -= 1
        if pixel[1] <= 0 and info["borders"]:
            pixel[1] += 1

        # pygame event queue
        for ev in pygame.event.get():
            # window close
            if ev.type == pygame.QUIT:
                pygame.quit()

        # if the pixel the pointer is over is not white, then make the color white
        if info["overwrite"]:
            if screen.get_at(([pixel[0], pixel[1]])) != (255, 255, 255):
                color = WHITE
        # draw a pixel
        screen.fill(color, ([pixel[0], pixel[1]], (1, 1)))
        # symmetry over x axis
        if info["sym_x"]:
            screen.fill(color, ([pixel[0], -pixel[1]+1000], (1, 1)))
        # symmetry over y axis
        if info["sym_y"]:
            screen.fill(color, ([-pixel[0]+1000, pixel[1]], (1, 1)))
        # symmetry over x & y axis
        if info["sym_x"] and info["sym_y"]:
            screen.fill(color, ([-pixel[0]+1000, -pixel[1]+1000], (1, 1)))
        # update display
        pygame.display.update()
    state_current = "MainMenu"
    pixel[0] = 500
    pixel[1] = 500
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
