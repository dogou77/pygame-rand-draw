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
            self.color_out = [self.color_in[0] / 2, self.color_in[1] / 2, self.color_in[2] / 2]
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



# check boxes are drawn as a rectangle from (x, y) to (x + w, y + h) or from the center of x & y and each contains a state
class CheckBox:
    # initializes the check box based on several parameters
    def __init__(self, x, y, w, h, color, color_check, margin = 10, centered = False, default_state = False):
        self.pos        = [x, y]
        self.size       = [w, h]
        self.margin     = margin
        self.color_in   = color
        self.color_chck = color_check
        self.state      = default_state

        self.pos_end    = [x + w, y + h] # gets the lower right hand corner of the checkbox
        self.pos_center = [((x * 2) + w) / 2, ((y * 2) + h) / 2] # gets the center of the checkbox with midpoint formula
        self.hovered    = False

        # runs through equations to offset the check box placement so it appears centered at x & y
        if centered:
            self.pos     = [self.pos_center[0] - self.size[0], self.pos_center[1] - self.size[1]]
            self.pos_end = [self.pos_center[0], self.pos_center[1]]
        
    # renders the check box
    def render(self, screen):
        # get the users mouse location
        mouse = pygame.mouse.get_pos()

        # darkens the input color that is used for when the mouse is over the button
        color_hover= [self.color_in[0] / 2, self.color_in[1] / 2, self.color_in[2] / 2]

        # draw the outline of the check box
        pygame.draw.rect(screen, self.color_in, [self.pos[0], self.pos[1], self.size[0], self.size[1]])

        # if the mouse is over the checkbox, draw a rectangle in it, if the state is true, draw a green rectangle in it
        if self.state:
            pygame.draw.rect(screen, self.color_chck, [self.pos[0] + self.margin, self.pos[1] + self.margin, self.size[0] - (self.margin * 2), self.size[1] - (self.margin * 2)])

        if self.pos[0] <= mouse[0] <= self.pos_end[0] and self.pos[1] <= mouse[1] <= self.pos_end[1]:
            pygame.draw.rect(screen, color_hover, [self.pos[0] + self.margin, self.pos[1] + self.margin, self.size[0] - (self.margin * 2), self.size[1] - (self.margin * 2)])
            self.hovered = True
        else:
            self.hovered = False

    # toggles the check boxes state if it is in the mouse position when clicked
    def toggle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.state = not self.state



# radio buttons are drawn as circles from the center of (x, y) with a radius, work just like check boxes with a state
class RadioButton:
    # class RadioButton is intended to be put into an array with other RadioButtons
    # where if one is pressed, all the other RadioButtons state's are turned to false
    
    #for radio in radio_buttons:
    #    radio.toggle(ev)
    #        if radio.state:
    #            for rad in radio_buttons:
    #                if rad != radio:
    #                    rad.state = False   

    # initializes the radio button based on several parameters
    def __init__(self, x, y, radius, margin, color, color_check, default_state = False):
        self.pos        = [x, y]
        self.radius     = radius
        self.margin     = margin
        self.color_in   = color
        self.color_chck = color_check
        self.state      = default_state

        self.collide_pos = [x - radius, y - radius, x + radius, y + radius] # set up a collision rectangle around the button
        self.hovered     = False

    def render(self, screen):
        # get the users mouse location
        mouse = pygame.mouse.get_pos()

        # darkens the input color that is used for when the mouse is over the button
        color_hover= [self.color_in[0] / 2, self.color_in[1] / 2, self.color_in[2] / 2]

        # draw the outline of the radio button
        pygame.draw.circle(screen, self.color_in, [self.pos[0], self.pos[1]], self.radius)

        # if the mouse is over the radio button, draw a circle in it, if the state is true, draw a green circle in it
        if self.state:
            pygame.draw.circle(screen, self.color_chck, [self.pos[0], self.pos[1]], self.radius - self.margin)

        if self.collide_pos[0] <= mouse[0] <= self.collide_pos[2] and self.collide_pos[1] <= mouse[1] <= self.collide_pos[3]:
            pygame.draw.circle(screen, color_hover, [self.pos[0], self.pos[1]], self.radius - self.margin)
            self.hovered = True
        else:
            self.hovered = False

    # toggles the radio button state if it is in the mouse position when clicked
    def toggle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
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