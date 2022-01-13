import pygame

# buttons are drawn as a rectangle from (x, y) to (x + w, y + h) or from the center of x & y and return a true or false when pressed
class Button:
    # initializes button with several parameters
    def __init__(self, x, y, w, h, color, text_font, text_str = "", text_color = (255, 255, 255), centered = False):
        self.pos        = [x, y]
        self.size       = [w, h]
        self.color_in   = color
        self.text_font  = text_font
        self.text_str   = text_str
        self.text_color = text_color
        self.color_out  = [color[0], color[1], color[2]] # color output
        self.pos_end    = [x + w, y + h] # gets the lower right hand corner of the button
        self.pos_center = [((x * 2) + w) / 2, ((y * 2) + h) / 2] # gets the center of the button with midpoint formula
        self.hovered    = False

        # runs through equations to offset the button & text placement so it appears centered at x & y
        if centered:
            self.pos        = [self.pos_center[0] - self.size[0], self.pos_center[1] - self.size[1]]
            self.pos_end    = [self.pos_center[0], self.pos_center[1]]
            self.pos_center = [((self.pos[0] * 2) + w) / 2, ((self.pos[1] * 2) + h) / 2]


    # renders the button
    def render(self, screen):
        # get the users mouse location
        mouse = pygame.mouse.get_pos()

        # if the mouse is over the button, lower the output colors values, if not, set to default color values
        if self.pos[0] <= mouse[0] <= self.pos_end[0] and self.pos[1] <= mouse[1] <= self.pos_end[1]:
            self.color_out[0] = self.color_in[0] / 2
            self.color_out[1] = self.color_in[1] / 2
            self.color_out[2] = self.color_in[2] / 2
            self.hovered = True
        else:
            self.color_out = [self.color_in[0], self.color_in[1], self.color_in[2]]
            self.hovered = False
        # draw the rectangle
        pygame.draw.rect(screen, self.color_out, [self.pos[0], self.pos[1], self.size[0], self.size[1]])

        # gets the text size for calculating where to put it
        text_size = self.text_font.size(self.text_str)
        text = self.text_font.render(self.text_str, True , self.text_color)

        # renders the text at the center of the button
        screen.blit(text , (self.pos_center[0] - (text_size[0] / 2), self.pos_center[1] - (text_size[1] / 2)))

    # gets the state of the button, if the mouse is in the button, then return true
    def get_state(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
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



class TextBoxInput:
    def __init__(self, text_default, position_x, position_y, size_x, size_y, hover_margin = 10):
        self.text            = text_default
        self.position        = [position_x, position_y]
        self.size            = [size_x, size_y]
        self.position_end    = [position_x + size_x, position_y + size_y] # gets the lower right hand corner of the button
        self.position_center = [((position_x * 2) + size_x) / 2, ((position_y * 2) + size_y) / 2] # gets the center of the button with midpoint formula
        self.hover_margin    = hover_margin
        self.text_current    = ""
        self.focused         = False
    
    def render(self, screen, mouse, color_hover, color_neut, text_font, text_color):
        # if the mouse is over the text box, or it is focused, draw a rectangle over it, if not then draw the neutral rectangle
        if self.position[0] <= mouse[0] <= self.position_end[0] and self.position[1] <= mouse[1] <= self.position_end[1] or self.focused:
            pygame.draw.rect(screen, color_hover, [self.position[0] + self.hover_margin, self.position[1] + self.hover_margin, self.size[0] - (self.hover_margin * 2), self.size[1] - (self.hover_margin * 2)])
        else:
            pygame.draw.rect(screen, color_neut, [self.position[0], self.position[1], self.size[0], self.size[1]])

        # calculate the size of the input text so that it can be centered
        text_size = text_font.size(self.text)
        text = text_font.render(self.text, True , text_color)

        # renders the text at the y center of the button
        screen.blit(text , (self.position[0] + self.hover_margin, self.position_center[1] - (text_size[1] / 2)))

    def text_input(self, screen, mouse, event):
        # this is put in the event loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.position[0] <= mouse[0] <= self.position_end[0] and self.position[1] <= mouse[1] <= self.position_end[1]:
                self.focused = not self.focused
            else:
                self.focused = False
        # this is the actual typing action
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_RETURN:
                self.focused = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode