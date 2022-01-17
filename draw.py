import pygame
import random
import math
import pg_ui_inputs as pguiin
  
pygame.init()

# draws text centered at the specified point
def draw_centered_text(screen, text_font, text_str, text_color, position_x, position_y):
    text_size = text_font.size(text_str)
    text = text_font.render(text_str, True , text_color)
    # renders the text at the center of the position provided
    screen.blit(text , (position_x - (text_size[0] / 2), position_y - (text_size[1] / 2)))

# keyboard commands for input in the drawing screens
def commands(screen, event, toggles):
    if pygame.key.get_focused():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12: # take a screenshot
                pygame.image.save(screen, "image.png")
            if event.key == pygame.K_ESCAPE: # exit to main menu
                toggles["running"] = False
            if event.key == pygame.K_SPACE: # toggle rendering
                toggles["render"] = not toggles["render"]

    return toggles

def randomize_color_a(r, g, b):
    # generate a random number from 0 to 2, this selects what rgb value is going to be modified
    color_rand = random.randrange(0, 3, 1)
    # generate a random number from 0 to 1, this selects if the selected rgb value is going to be incremented or decremented
    color_up_down = random.randrange(0, 2, 1)

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
    color = (r, g, b)
    return color

def randomize_color_b():
    # randomizes all color values and sets them equal to color
    rand_r = random.randrange(1, 255, 1)
    rand_g = random.randrange(1, 255, 1)
    rand_b = random.randrange(1, 255, 1)
    color = (rand_r, rand_g, rand_b)
    return color



# main menu screen
def screen_menu_main(screen):
    # set the state_current to global so that it can change states
    global state_current

    running = True

    # fonts
    font_button = pygame.font.SysFont('Arial', 35)
    font_title  = pygame.font.SysFont('Arial', 50)
    font_author = pygame.font.SysFont('Arial', 20)

    # buttons
    button_draw_point        = pguiin.Button(500, 200, 500, 100, BUTTON_DARK, font_button, "Pointer Drawer", WHITE, True)
    button_draw_circle_lines = pguiin.Button(500, 320, 500, 100, BUTTON_DARK, font_button, "Circular Line Drawer", WHITE, True)
    button_draw_lines        = pguiin.Button(500, 440, 500, 100, BUTTON_DARK, font_button, "Line Drawer", WHITE, True)
    button_draw_rect         = pguiin.Button(500, 560, 500, 100, BUTTON_DARK, font_button, "Rectangle Drawer", WHITE, True)
    button_quit              = pguiin.Button(500, 900, 500, 100, BUTTON_DARK, font_button, "Quit", WHITE, True)

    # pygame event queue
    while running:

        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT or button_quit.get_state(ev):
                pygame.quit()
    
            if button_draw_point.get_state(ev):
                state_current = "PointDrawMenu"
                running = False
            if button_draw_circle_lines.get_state(ev):
                state_current = "CircleLineDrawMenu"
                running = False
            if button_draw_lines.get_state(ev):
                state_current = "LineDrawMenu"
                running = False
            if button_draw_rect.get_state(ev):
                state_current = "RectDrawMenu"
                running = False

        # fills the screen with a color
        screen.fill(PURPLE)

        # renders the text
        draw_centered_text(screen, font_title, "Python Random Drawer", WHITE, 500, 50)
        draw_centered_text(screen, font_author, "By: Brayden Olsen", WHITE, 500, 100)

        # renders the buttons
        button_draw_point.render(screen)
        button_draw_circle_lines.render(screen)
        button_draw_lines.render(screen)
        button_draw_rect.render(screen)
        button_quit.render(screen)

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
        "borders"  : False,
        "is_image" : False,
        "image_str": "",
    }

    # initializes a list that is supposed to contain multiple radio buttons so that two are not active at once
    radio_buttons = []

    # initialize fonts
    font_title    = pygame.font.SysFont('Arial', 50)
    font_input    = pygame.font.SysFont('Arial', 30)
    font_label    = pygame.font.SysFont('Arial', 35)
    font_instruct = pygame.font.SysFont('Arial', 20)

    # initialize check boxes
    check_box_sym_x     = pguiin.CheckBox(125, 250, 100, 100, BUTTON_DARK, GREEN, 10, True)
    check_box_sym_y     = pguiin.CheckBox(375, 250, 100, 100, BUTTON_DARK, GREEN, 10, True)
    check_box_borders   = pguiin.CheckBox(250, 650, 100, 100, BUTTON_DARK, GREEN, 10, True)
    check_box_image     = pguiin.CheckBox(750, 250, 100, 100, BUTTON_DARK, GREEN, 10, True)

    # initialize radio buttons and add them to the radio_button list
    radio_color_a = pguiin.RadioButton(125, 450, 50, 10, BUTTON_DARK, GREEN)
    radio_color_b = pguiin.RadioButton(375, 450, 50, 10, BUTTON_DARK, GREEN)
    radio_buttons.append(radio_color_a)
    radio_buttons.append(radio_color_b)

    # initalize back and forward buttons
    button_back = pguiin.Button(250, 900, 400, 100, BUTTON_DARK, font_label, "Back", WHITE, True)
    button_next = pguiin.Button(750, 900, 400, 100, BUTTON_DARK, font_label, "Next", WHITE, True)

    # initialize text boxes
    text_in_image = pguiin.TextBoxInput(750, 400, 250, 50, BUTTON_DARK, font_input, WHITE, "Enter File Name", False, 5, True)

    while running:

        # pygame event queue
        for ev in pygame.event.get():

            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()
            
            # gets the input from text boxes
            text_in_image.text_input(ev)

            # gets the states of the back and next buttons then sets a state and exits the loop
            if button_back.get_state(ev):
                state_current = "MainMenu"
                running = False
            if button_next.get_state(ev):
                state_current = "PointDraw"
                running = False
            
            # toggles the check boxes if the mouse is in their area
            check_box_sym_x.toggle(ev)
            check_box_sym_y.toggle(ev)
            check_box_borders.toggle(ev)
            check_box_image.toggle(ev)

            # toggles the radio button in the mouse is in their area, but untoggled ones that are already true
            for radio in radio_buttons:
                    radio.toggle(ev)
                    if radio.state:
                        for rad in radio_buttons:
                            if rad != radio:
                                rad.state = False               

        screen.fill(PURPLE)

        # render the check boxes
        check_box_sym_x.render(screen)
        check_box_sym_y.render(screen)
        check_box_borders.render(screen)
        check_box_image.render(screen)

        # render the radio buttons
        radio_color_a.render(screen)
        radio_color_b.render(screen)

        # render the buttons
        button_back.render(screen)
        button_next.render(screen)

        # render text boxes
        if check_box_image.state:
            text_in_image.render(screen)

        # draw all the text
        draw_centered_text(screen, font_title, "Point Drawer Options", WHITE, 500, 50)
        draw_centered_text(screen, font_instruct, "ESC - Exits | F12 - Saves Image | SPACE - Toggle Render", WHITE, 500, 100)
        draw_centered_text(screen, font_label, "X-Axis", WHITE, 125, 140)
        draw_centered_text(screen, font_label, "Symmetry", WHITE, 125, 170)
        draw_centered_text(screen, font_label, "Y-Axis", WHITE, 375, 140)
        draw_centered_text(screen, font_label, "Symmetry", WHITE, 375, 170)
        draw_centered_text(screen, font_label, "Color Mode A", WHITE, 125, 350)
        draw_centered_text(screen, font_label, "Color Mode B", WHITE, 375, 350)
        draw_centered_text(screen, font_label, "Borders", WHITE, 250, 550)
        draw_centered_text(screen, font_label, "Import Image", WHITE, 750, 150)

        # updates the frames of the game
        pygame.display.update()

    # set up the return values for info based on the check box states and radio button states
    info["sym_x"]     = check_box_sym_x.state
    info["sym_y"]     = check_box_sym_y.state
    info["color_a"]   = radio_color_a.state
    info["color_b"]   = radio_color_b.state
    info["borders"]   = check_box_borders.state
    info["is_image"]  = check_box_image.state
    info["image_str"] = text_in_image.text

    return info



# draw pointer screen
def screen_draw_pointer(pixel, screen, info):
    global state_current

    # set default color to black
    color = (0, 0, 0)
    image_ok = True

    toggles = {
        "running" : True,
        "render"  : True,
    }

    screen.fill(WHITE)
    
    # attempts to load the user defined image
    if info["is_image"]:
        try:
            background = pygame.image.load(info["image_str"])
        except:
            image_ok = False

        if image_ok:
            screen.blit(background, (0, 0))

    while toggles["running"]:
        # if the user selected color mode a in the previous screen
        if info["color_a"]:
            color = randomize_color_a(color[0], color[1], color[2])
        # if the user selected color mode b
        elif info["color_b"]:
            # randomizes all color values and sets them equal to color
            color = randomize_color_b()

        # generate a random number
        rand_num = random.randrange(0, 8, 1)

        # match random number to corresponding direction based on numpad
        match rand_num:
            case 0:
                pixel[0] -= 1
                pixel[1] -= 1
            case 1:
                pixel[1] -= 1
            case 2:
                pixel[0] += 1
                pixel[1] -= 1
            case 3:
                pixel[0] -= 1
            case 4:
                pixel[0] += 1
            case 5: 
                pixel[0] -= 1
                pixel[1] += 1
            case 6:
                pixel[1] += 1
            case 7:
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
            toggles = commands(screen, ev, toggles)
        
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
        # update display if space bar is pressed
        if toggles["render"]:
            pygame.display.update()

    state_current = "MainMenu"
    pixel[0] = 500
    pixel[1] = 500
    return pixel
    


# options screen for circular line draw
def screen_menu_circle_line_draw(screen):
    global state_current

    running = True

    # info is the variable that is returned
    info = {
        "radius"    : 100,
        "draw_from" : [0, 0],
        "draw_to"   : [0, 0],
        "color_a"   : False,
        "color_b"   : False,
    }

    radio_buttons = []

    # initialize fonts
    font_title    = pygame.font.SysFont('Arial', 50)
    font_input    = pygame.font.SysFont('Arial', 30)  
    font_label    = pygame.font.SysFont('Arial', 35) 
    font_error    = pygame.font.SysFont('Arial', 45)
    font_commands = pygame.font.SysFont('Arial', 20)

    # initialize back and forward buttons
    button_back = pguiin.Button(250, 900, 400, 100, BUTTON_DARK, font_label, "Back", WHITE, True)
    button_next = pguiin.Button(750, 900, 400, 100, BUTTON_DARK, font_label, "Next", WHITE, True)

    # initialize radio buttons and add them to the radio_button list
    radio_color_a = pguiin.RadioButton(250, 250, 50, 10, BUTTON_DARK, GREEN)
    radio_color_b = pguiin.RadioButton(500, 250, 50, 10, BUTTON_DARK, GREEN)
    radio_buttons.append(radio_color_a)
    radio_buttons.append(radio_color_b)

    # initialize text boxes
    text_in_radius = pguiin.TextBoxInput(750, 250, 50, 50, BUTTON_DARK, font_input, WHITE, "500", True, 5, True)
    text_in_from_x = pguiin.TextBoxInput(710, 450, 60, 50, BUTTON_DARK, font_input, WHITE, "0", True, 5, True)
    text_in_from_y = pguiin.TextBoxInput(790, 450, 60, 50, BUTTON_DARK, font_input, WHITE, "0", True, 5, True)
    text_in_to_x   = pguiin.TextBoxInput(710, 650, 60, 50, BUTTON_DARK, font_input, WHITE, "0", True, 5, True)
    text_in_to_y   = pguiin.TextBoxInput(790, 650, 60, 50, BUTTON_DARK, font_input, WHITE, "0", True, 5, True)

    while running:

        screen.fill(PURPLE)

        # pygame event queue
        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()
            # text input events
            text_in_radius.text_input(ev)
            text_in_from_x.text_input(ev)
            text_in_from_y.text_input(ev)
            text_in_to_x.text_input(ev)
            text_in_to_y.text_input(ev)

            # button events
            if button_back.get_state(ev):
                state_current = "MainMenu"
                running = False
            if button_next.get_state(ev):
                state_current = "CircleLineDraw"
                running = False

            # toggles the radio button in the mouse is in their area, but untoggled ones that are already true
            for radio in radio_buttons:
                radio.toggle(ev)
                if radio.state:
                    for rad in radio_buttons:
                        if rad != radio:
                            rad.state = False
        
        # render buttons
        button_back.render(screen)

        # render radio buttons
        radio_color_a.render(screen)
        radio_color_b.render(screen)

        # render text boxes
        text_in_radius.render(screen)
        text_in_from_x.render(screen)
        text_in_from_y.render(screen)
        text_in_to_x.render(screen)
        text_in_to_y.render(screen)

        # render text
        draw_centered_text(screen, font_title, "Circular Line Drawer Options", WHITE, 500, 50)
        draw_centered_text(screen, font_commands, "ESC - Exits | F12 - Saves Image | SPACE - Toggle Render", WHITE, 500, 100)
        draw_centered_text(screen, font_label, "Color Mode A", WHITE, 250, 150)
        draw_centered_text(screen, font_label, "Color Mode B", WHITE, 500, 150)
        draw_centered_text(screen, font_label, "Radius", WHITE, 750, 150)
        draw_centered_text(screen, font_label, "From", WHITE, 750, 350)
        draw_centered_text(screen, font_label, "X       Y", WHITE, 750, 400)
        draw_centered_text(screen, font_label, "To", WHITE, 750, 550)
        draw_centered_text(screen, font_label, "X       Y", WHITE, 750, 600)

        # error message conditionals
        if not text_in_radius.is_int():
            draw_centered_text(screen, font_error, "Must enter numbers", RED, 750, 900)
        elif not text_in_from_x.is_int() or not text_in_from_y.is_int():
            draw_centered_text(screen, font_error, "Must enter numbers", RED, 750, 900)
        elif not text_in_to_x.is_int() or not text_in_to_y.is_int():
            draw_centered_text(screen, font_error, "Must enter numbers", RED, 750, 900)
        else:
            button_next.render(screen)

        pygame.display.update()

    # update info and return it
    info["radius"]    = text_in_radius.get_int()
    info["draw_from"] = [text_in_from_x.get_int(), text_in_from_y.get_int()]
    info["draw_to"]   = [text_in_to_x.get_int(), text_in_to_y.get_int()]
    info["color_a"]   = radio_color_a.state
    info["color_b"]   = radio_color_b.state

    return info



def screen_circle_line_draw(screen, info):
    global state_current

    screen.fill(WHITE)

    toggles = {
        "running" : True,
        "render"  : True,
    }

    color = (0, 0, 0)

    # set local variables equal to their info counterparts
    radius = info["radius"]
    from_x = info["draw_from"][0]
    from_y = info["draw_from"][1]
    to_x   = info["draw_to"][0]
    to_y   = info["draw_to"][0]

    while toggles["running"]:
        if info["color_a"]:
            color = randomize_color_a(color[0], color[1], color[2])
        if info["color_b"]:
            color = randomize_color_b()

        # pygame event queue
        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()
            toggles = commands(screen, ev, toggles)
        
        # generate a random number representing a point on the edge of a circle
        randNum = random.random()*(2*math.pi)

        # convert the polar coordinates to rectangular to draw a line
        pygame.draw.line(screen, color, (500 + from_x, 500 - from_y), ((radius * math.cos(randNum)) + 500 + to_x, (radius * math.sin(randNum)) + 500 - to_y))

        # display the changes if render is enabled
        if toggles["render"]:
            pygame.display.update()
    state_current = "MainMenu"



def screen_menu_line_draw(screen):
    global state_current
    running = True

    # info is the variable that is returned
    info = {
        "color_a"   : False,
        "color_b"   : False,
    }

    radio_buttons = []

    # initialize fonts
    font_title    = pygame.font.SysFont('Arial', 50)
    font_label    = pygame.font.SysFont('Arial', 35)
    font_commands = pygame.font.SysFont('Arial', 20)

    # initialize back and forward buttons
    button_back = pguiin.Button(250, 900, 400, 100, BUTTON_DARK, font_label, "Back", WHITE, True)
    button_next = pguiin.Button(750, 900, 400, 100, BUTTON_DARK, font_label, "Next", WHITE, True)

    # initialize radio buttons and add them to the radio_button list
    radio_color_a = pguiin.RadioButton(350, 250, 50, 10, BUTTON_DARK, GREEN)
    radio_color_b = pguiin.RadioButton(650, 250, 50, 10, BUTTON_DARK, GREEN)
    radio_buttons.append(radio_color_a)
    radio_buttons.append(radio_color_b)

    while running:

        screen.fill(PURPLE)

        # pygame event queue
        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()

            # button events
            if button_back.get_state(ev):
                state_current = "MainMenu"
                running = False
            if button_next.get_state(ev):
                state_current = "LineDraw"
                running = False
        
            # toggles the radio button in the mouse is in their area, but untoggled ones that are already true
            for radio in radio_buttons:
                radio.toggle(ev)
                if radio.state:
                    for rad in radio_buttons:
                        if rad != radio:
                            rad.state = False
        
        # render buttons
        button_back.render(screen)
        button_next.render(screen)

        # render radio buttons
        radio_color_a.render(screen)
        radio_color_b.render(screen)

        # render text
        draw_centered_text(screen, font_title, "Line Drawer Options", WHITE, 500, 50)
        draw_centered_text(screen, font_commands, "ESC - Exits | F12 - Saves Image | SPACE - Toggle Render", WHITE, 500, 100)
        draw_centered_text(screen, font_label, "Color Mode A", WHITE, 350, 150)
        draw_centered_text(screen, font_label, "Color Mode B", WHITE, 650, 150)

        pygame.display.update()

    info["color_a"] = radio_color_a.state
    info["color_b"] = radio_color_b.state

    return info



# the actual screen that draws random lines
def screen_line_draw(screen, info):
    global state_current

    screen.fill(WHITE)

    toggles = {
        "running" : True,
        "render"  : True,
    }

    color = (0, 0, 0)

    while toggles["running"]:
        if info["color_a"]:
            color = randomize_color_a(color[0], color[1], color[2])
        if info["color_b"]:
            color = randomize_color_b()

        # pygame event queue
        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()
            toggles = commands(screen, ev, toggles)
        
        # generate a random number 
        rand_from_x = random.randrange(-100, 1100)
        rand_from_y = random.randrange(-100, 1100)
        rand_to_x   = random.randrange(-100, 1100)
        rand_to_y   = random.randrange(-100, 1100)

        # convert the polar coordinates to rectangular to draw a line
        pygame.draw.line(screen, color, (rand_from_x, rand_from_y), (rand_to_x, rand_to_y))

        # display the changes if render is enabled
        if toggles["render"]:
            pygame.display.update()
    state_current = "MainMenu"



def screen_menu_rect_draw(screen):
    global state_current
    running = True

    # info is the variable that is returned
    info = {
        "color_a"   : False,
        "color_b"   : False,
    }

    radio_buttons = []

    # initialize fonts
    font_title    = pygame.font.SysFont('Arial', 50)
    font_label    = pygame.font.SysFont('Arial', 35)
    font_commands = pygame.font.SysFont('Arial', 20)

    # initialize back and forward buttons
    button_back = pguiin.Button(250, 900, 400, 100, BUTTON_DARK, font_label, "Back", WHITE, True)
    button_next = pguiin.Button(750, 900, 400, 100, BUTTON_DARK, font_label, "Next", WHITE, True)

    # initialize radio buttons and add them to the radio_button list
    radio_color_a = pguiin.RadioButton(350, 250, 50, 10, BUTTON_DARK, GREEN)
    radio_color_b = pguiin.RadioButton(650, 250, 50, 10, BUTTON_DARK, GREEN)
    radio_buttons.append(radio_color_a)
    radio_buttons.append(radio_color_b)

    while running:

        screen.fill(PURPLE)

        # pygame event queue
        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()

            # button events
            if button_back.get_state(ev):
                state_current = "MainMenu"
                running = False
            if button_next.get_state(ev):
                state_current = "RectDraw"
                running = False
        
            # toggles the radio button in the mouse is in their area, but untoggled ones that are already true
            for radio in radio_buttons:
                radio.toggle(ev)
                if radio.state:
                    for rad in radio_buttons:
                        if rad != radio:
                            rad.state = False
        
        # render buttons
        button_back.render(screen)
        button_next.render(screen)

        # render radio buttons
        radio_color_a.render(screen)
        radio_color_b.render(screen)

        # render text
        draw_centered_text(screen, font_title, "Rectangle Drawer Options", WHITE, 500, 50)
        draw_centered_text(screen, font_commands, "ESC - Exits | F12 - Saves Image | SPACE - Toggle Render", WHITE, 500, 100)
        draw_centered_text(screen, font_label, "Color Mode A", WHITE, 350, 150)
        draw_centered_text(screen, font_label, "Color Mode B", WHITE, 650, 150)

        pygame.display.update()

    info["color_a"] = radio_color_a.state
    info["color_b"] = radio_color_b.state

    return info



# the actual screen that draws random lines
def screen_rect_draw(screen, info):
    global state_current

    screen.fill(WHITE)

    toggles = {
        "running" : True,
        "render"  : True,
    }

    color = (0, 0, 0)

    while toggles["running"]:
        if info["color_a"]:
            color = randomize_color_a(color[0], color[1], color[2])
        if info["color_b"]:
            color = randomize_color_b()

        # pygame event queue
        for ev in pygame.event.get():
            # window is closed
            if ev.type == pygame.QUIT:
                pygame.quit()
            toggles = commands(screen, ev, toggles)
        
        # generate a random number 
        rand_from_x = random.randrange(-100, 1100)
        rand_from_y = random.randrange(-100, 1100)
        rand_to_x   = random.randrange(-100, 1100)
        rand_to_y   = random.randrange(-100, 1100)

        # convert the polar coordinates to rectangular to draw a line
        pygame.draw.rect(screen, color, (rand_from_x, rand_from_y, rand_to_x, rand_to_y))

        # display the changes if render is enabled
        if toggles["render"]:
            pygame.display.update()
    state_current = "MainMenu"

# constants
RES = (1000, 1000)

# colors
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
BLUE         = (  0,   0, 255)
BLACK        = (  0,   0,   0)
WHITE        = (255, 255, 255)
PURPLE       = ( 60,  25,  60)
BUTTON_LIGHT = (170, 170, 170)
BUTTON_DARK  = (100, 100, 100)

# global variables
state_current = "MainMenu"

# variables
pixel = [500, 500]

# opens up a window
screen = pygame.display.set_mode(RES)

# sets the logo and caption for the pygame window
icon = pygame.image.load("icon32x32.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Python Random Drawer")

clock = pygame.time.Clock()

# main loop
while True:
    if state_current == "MainMenu":
        screen_menu_main(screen)
    if state_current == "PointDrawMenu":
        point_draw_info = screen_menu_draw_pointer(screen)
    if state_current == "PointDraw":
        pixel = screen_draw_pointer(pixel, screen, point_draw_info)
    if state_current == "CircleLineDrawMenu":
        circle_line_draw_info = screen_menu_circle_line_draw(screen)
    if state_current == "CircleLineDraw":
        screen_circle_line_draw(screen, circle_line_draw_info)
    if state_current == "LineDrawMenu":
        line_draw_info = screen_menu_line_draw(screen)
    if state_current == "LineDraw":
        screen_line_draw(screen, line_draw_info)
    if state_current == "RectDrawMenu":
        rect_draw_info = screen_menu_rect_draw(screen)
    if state_current == "RectDraw":
        screen_rect_draw(screen, rect_draw_info)
