import pygame, pickle, sys, os, random
from pygame.locals import *
from MyLibrary import *
from database import *
from Encrypt import *

#Quit the program safely
def end(exit_code=0, save=True):
    if save:
        login.setValue('Money', '\'{}\''.format(total))
        login.setValue('Notes', '\'{}\''.format(text))
    pygame.quit()
    sys.exit(exit_code)

#Set keyboard to azerty
def keyboard_init():
    keys = pygame.key.get_pressed()
    K_a = 113
    K_z = 119
    K_m = 59
    K_q = 97
    K_w = 122
    K_l = 108
    K_COMMA = 109
    K_LEFTPAREN = 53
    K_RIGHTPAREN = 45
    K_QUOTEDBL = 51
    K_PERIOD = 44
    K_BACKSLASH = 35
    K_COLON = 46
    globals().update(locals())
    

def buttons_init():
    global buttons, money_buttons

    buttons = dict()
    money_buttons = dict()

    x = 10
    y = 500
    y_dist = 50
    x_add = 110

    money_buttons['50'] = buttons['50'] = Button(x, y, 100, 40, font, surface=None, text='50 €')
    money_buttons['20'] = buttons['20'] = Button(x, y + y_dist, 100, 40, font, surface=None, text='20 €')
    
    x += x_add
    money_buttons['10'] = buttons['10'] = Button(x, y, 100, 40, font, surface=None, text='10 €')
    money_buttons['5'] = buttons['5'] = Button(x, y + y_dist, 100, 40, font, surface=None, text='5 €')
    
    x += x_add
    money_buttons['2'] = buttons['2'] = Button(x, y, 100, 40, font, surface=None, text='2 €')
    money_buttons['1'] = buttons['1'] = Button(x, y + y_dist, 100, 40, font, surface=None, text='1 €')
    
    x += x_add
    money_buttons['0.5'] = buttons['0.5'] = Button(x, y, 100, 40, font, surface=None, text='0.5 €')
    money_buttons['0.2'] = buttons['0.2'] = Button(x, y + y_dist, 100, 40, font, surface=None, text='0.2 €')
    
    x += x_add
    money_buttons['0.1'] = buttons['0.1'] = Button(x, y, 100, 40, font, surface=None, text='0.1 €')
    money_buttons['0.05'] = buttons['0.05'] = Button(x, y + y_dist, 100, 40, font, surface=None, text='0.05 €')
    
    x += x_add
    money_buttons['0.02'] = buttons['0.02'] = Button(x, y, 100, 40, font, surface=None, text='0.02 €')
    money_buttons['0.01'] = buttons['0.01'] = Button(x, y + y_dist, 100, 40, font, surface=None, text='0.01 €')
    
    x += x_add
    buttons['Add'] = Sub_Button(x, y, 100, 40, font, surface=None, text='  Add')
    buttons['Clear'] = Button(x, y + y_dist, 100, 40, font, surface=None, text='Clear')
    buttons['Submit'] = Button(x, y - y_dist, 100, 40, font, surface=None, text='Submit')

def text_init():
    global text_fields
    text_fields = dict()
    text_fields['Bottom'] = Text_field(10, 450, 300, 40, text = '0')
    text_fields['Total'] = Text_field(100, 100, 300, 300, text = 'Your total is:\n' + str(round(total, 2)) + '\n€')

def input_init():
    global inputs

    inputs = dict()
    inputs['Notes'] = Input(450, 100, 250, 250, text = text)
    

    
def init():
    global font, SIZE, screen, clock, FPS, mouse_x, mouse_y,\
    mouse_left, mouse_middle, mouse_right, mouse_scroll, scroll_move
 
    pygame.init()
    font = pygame.font.Font(None, 30)
    
    #set the window size (width and height
    SIZE = [800, 600]
    screen = pygame.display.set_mode(SIZE)

    #set window title
    pygame.display.set_caption("Bank")

     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    FPS = 60

    mouse_scroll = mouse_x = mouse_y = 0
    mouse_left = mouse_middle = mouse_right = False
    scroll_move = 10

class Button(object):
    def __init__(self, x, y, width, height, font, surface=None, text=''):
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width, height))
        self.surface = surface
        if surface == None:
            self.surface = pygame.display.get_surface()
        self.text = text
        self.font = font
        self.text_colour = (0,0,0)
        self.colour = (255,222,173)
        self.shade_colour = (105,105,105)
        self.shade_width = 4
        self.down = False
        self.__clicked = False
        self.text_pos = Point(self.rect.x+self.shade_width*2, self.rect.y+self.shade_width*2)
        self.unClick()
        

    def update(self, time):
        if mouse_x > self.rect.x and mouse_x < self.rect.right and \
               mouse_y > self.rect.y and mouse_y < self.rect.bottom and mouse_left:
            self.click()
            
        if mouse_x > self.rect.x and mouse_x < self.rect.right and \
               mouse_y > self.rect.y and mouse_y < self.rect.bottom and not mouse_left and self.down == True:
            self.__clicked = True
            self.unClick()
        if not mouse_left or mouse_x < self.rect.x or mouse_x > self.rect.right or \
               mouse_y < self.rect.y or mouse_y > self.rect.bottom:
            self.unClick()
            

    def draw(self):
        self.surface.blit(self.image, (self.rect))

    def click(self):
        self.down = True

        self.text_pos = Point(self.shade_width*2 + 2, self.shade_width*2 + 2)
        rect1 = pygame.Rect(0, 0, self.rect.width, self.shade_width) #top
        rect2 = pygame.Rect(0, 0, self.shade_width, self.rect.height) #left

        self.image.fill(self.colour)
        print_text(self.font, self.text_pos.X, self.text_pos.Y, self.text, self.text_colour, self.image)
        pygame.draw.rect(self.image, self.shade_colour, rect1)
        pygame.draw.rect(self.image, self.shade_colour, rect2)

    def getClicked(self):
        click = False
        if self.__clicked:
            click = True
            self.__clicked = False
        return click
    
    def setClicked(self, clicked):
        self.__clicked = clicked
    Clicked = property(getClicked,setClicked)
        
        
    def unClick(self):
        self.down = False

        self.text_pos = Point(self.shade_width*2, self.shade_width*2)
        rect1 = pygame.Rect(0, self.rect.height - self.shade_width, self.rect.width, self.shade_width) #bottom
        rect2 = pygame.Rect(self.rect.width - self.shade_width, 0, self.shade_width, self.rect.height) #right
        
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.shade_colour, rect1)
        pygame.draw.rect(self.image, self.shade_colour, rect2)
        print_text(self.font, self.text_pos.X, self.text_pos.Y, self.text, self.text_colour, self.image)

class Sub_Button(Button):
    def __init__(self, x, y, width, height, font, surface=None, text='Add'):
        text = '  Add'
        Button.__init__(self, x, y, width, height, font, surface, text)
        self.time = 100
        self.old_ticks = 0
        
    def update(self, ticks):
        if self.old_ticks + self.time < ticks:
            if mouse_x > self.rect.x and mouse_x < self.rect.right and \
                   mouse_y > self.rect.y and mouse_y < self.rect.bottom and mouse_left and self.down == False: #If you click it
                self.text = 'Subtract'
                self.click()
                self.clicked = True
                
            elif mouse_x > self.rect.x and mouse_x < self.rect.right and \
                   mouse_y > self.rect.y and mouse_y < self.rect.bottom and mouse_left and self.down == True: #If you click while it's down it goes up
                self.text = '  Add'
                self.unClick()
                self.clicked = True

            self.old_ticks = ticks

class Text_field(object):
    def __init__(self, x, y, width, height, font=None, surface=None, text='', password=False):
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height))
        if font == None:
            self.font = pygame.font.Font(None, 40)
        else:
            self.font = font
        if surface == None:
            self.surface = pygame.display.get_surface()
        else:
            self.surface = surface

        self.shade_width = 4
        self.shade_colour = Color(105,105,105)
        self.colour = Color(255,255,255)
        self.text_colour = Color(0,0,0)
        self.textX = self.shade_width*2

        self.password = password

        self.setText(text)

    def setText(self, new_text=''):
        self.__text = str(new_text)
        self.image.fill(self.colour)
        if not self.password:
            print_text(self.font,self.textX, self.shade_width*2, self.__text, self.text_colour, self.image)
        else:
            text = ''
            for i in self.Text:
                text += '*'
            print_text(self.font,self.textX, self.shade_width*2, text, self.text_colour, self.image)
        pygame.draw.rect(self.image, self.shade_colour, (0,0,self.rect.width,self.shade_width))#Top
        pygame.draw.rect(self.image, self.shade_colour, (0,0,self.shade_width,self.rect.height))#Left
            
    def getText(self):
        return self.__text
    Text = property(getText,setText)

    def setTextColour(self, colour):
        self.text_colour = colour
        self.Text = self.Text
    Colour = property(fset=setTextColour)

    def draw(self):
        self.surface.blit(self.image, (self.rect.x,self.rect.y))

class Input(Text_field):
    def __init__(self, x, y, width, height, font=None, surface=None, text='', password = False):
        if font == None:
            font = pygame.font.SysFont('Courier New', 15)
        Text_field.__init__(self, x,y,width,height,font,surface,text, password)
        self.colour = Color(255,245,238)
        self.selected = False
        self.last_tick = 0
        self.answered = False
        self.setText(text)
        self.old_keys = list((0 for x in range(323)))
        self.wait = 200

    def update(self, keys, ticks):
        modified = False
        if not self.selected:
            if mouse_x > self.rect.x and mouse_x < self.rect.right and \
               mouse_y > self.rect.y and mouse_y < self.rect.bottom:
                self.selected = True
                self.answered = False
        elif self.selected:
            if mouse_x < self.rect.x or mouse_x > self.rect.right or \
               mouse_y < self.rect.y or mouse_y > self.rect.bottom:
                self.selected = False
                self.answered = True
                return 0
            for letter in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',\
                           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'SPACE', \
                           'COMMA', 'BACKSPACE', 'RETURN', 'LEFTPAREN', 'RIGHTPAREN',\
                           'EQUALS', 'KP0', 'KP1', 'KP2', 'KP3', 'KP4', 'KP5', 'KP6', 'KP7', 'KP8',\
                           'KP9', 'KP_PERIOD', 'PERIOD', 'QUOTEDBL', '8', 'BACKSLASH', 'KP_PLUS', \
                           'COLON'):
                if self.add(letter, ticks):
                    modified = True
            if mouse_scroll:
                self.textX += mouse_scroll
                modified = True
                
            if modified:
                self.Text = self.Text
                self.old_keys = keys
                self.last_tick = ticks

    def add(self, letter, ticks):
        mod = False
        if keys[eval('K_'+letter)] and not self.old_keys[eval('K_'+letter)]:
            mod = True
        elif keys[eval('K_'+letter)] and self.last_tick + self.wait < ticks:
            mod = True
        if mod:
            alt = False
            shift = False
            if keys[K_RALT] or keys[K_LALT]:
                alt = True
            if keys[K_RSHIFT] or keys[K_LSHIFT]:
                shift = True
            if letter == 'SPACE':
                letter = ' '
            elif letter == '8' and alt:
                letter = '\\'
            elif letter == '8':
                letter = '_'
            elif letter == 'COMMA':
                letter = ','
            elif letter == 'COLON':
                letter = ':'
            elif letter == 'BACKSPACE':
                letter = ''
                self.Text = self.Text[:-1]
            elif letter == 'RETURN':
                letter = '\n'
            elif letter == 'LEFTPAREN' and alt:
                letter = '['
            elif letter == 'LEFTPAREN':
                letter = '('
            elif letter == 'RIGHTPAREN' and alt:
                letter = ']'
            elif letter == 'RIGHTPAREN':
                letter = ')'
            elif letter == 'EQUALS':
                letter = '='
            elif letter == 'PERIOD' and shift:
                letter = '.'
            elif letter == 'PERIOD':
                letter = ';'
            elif letter == 'QUOTEDBL':
                letter = '"'
            elif letter[:2] == 'KP':
                if letter == 'KP_PLUS':
                    letter = '+'
                elif letter == 'KP_PERIOD':
                    letter = '.'
                else:
                    letter = letter[-1:]
            if keys[K_LSHIFT] or keys[K_RSHIFT]:
                letter = letter.upper()
            self.Text += letter
            return True       
        
def login():
    global mouse_x, mouse_y, mouse_left, mouse_middle, mouse_right, keys, total, text, login, mouse_scroll
    login = Login('Accounts.db')
    login.addColumn('Money', 'TEXT')
    login.addColumn('Notes', 'TEXT')
    init()
    keyboard_init()

    sign_up = 0
    password = ''
    password2 = ''
    


    login_buttons = dict()
    font = pygame.font.Font(None, 50)
    login_buttons['Sign In'] = Button(600, 400, 150, 60, font, surface=None, text='Sign In')
    font = pygame.font.Font(None, 40)
    login_buttons['Sign Up'] = Button(500, 480, 250, 60, font, surface=None, text='Create Account')

    login_textfields = dict()
    login_textfields['Username'] = Text_field(100, 50, 170, 40, text = 'Username')
    login_textfields['Password'] = Text_field(100, 300, 170, 40, text = 'Password')
    login_textfields['Message'] = Text_field(400, 50, 300, 300, text = '')
    login_textfields['Message'].Colour = Color(255,0,0)

    login_inputs = dict()
    font = pygame.font.SysFont('Courier New', 20)
    login_inputs['Username'] = Input(100, 100, 170, 50, font = font, text = '')
    login_inputs['Password'] = Input(100, 350, 170, 50, font = font, text = '', password = True)
    

    done = False
    
        # -------- Main Program Loop -----------
    while not login.connected:
        mouse_scroll = 0
        ticks = pygame.time.get_ticks()
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == QUIT: end(save=False)
            elif event.type == MOUSEMOTION: mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_left = True
                elif event.button == 2:
                    mouse_middle = True
                elif event.button == 3:
                    mouse_right = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_left = False
                elif event.button == 2:
                    mouse_middle = False
                elif event.button == 3:
                    mouse_right = False
                elif event.button == 4:
                    mouse_scroll = scroll_move
                elif event.button == 5:
                    mouse_scroll = -scroll_move
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
            elif event.type == KEYUP:
                keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]: end(save=False)
     
        # --- Game logic should go here
        # --- Drawing code should go here
        screen.fill((211,211,211))
        for value in login_buttons:
            login_buttons[value].update(ticks)
            login_buttons[value].draw()
            clicked = login_buttons[value].Clicked
            if clicked:
                if value == 'Sign In':
                    if login.connect(login_inputs['Username'].Text, login_inputs['Password'].Text):
                        total = float(login.getValue('Money'))
                        text = login.getValue('Notes')
                    else:
                        login_textfields['Message'].Text = 'Information\nIncorrect'
                if value == 'Sign Up':
                    if sign_up == 0 and login_inputs['Username'].Text != '' and login_inputs['Password'].Text != '':
                        sign_up = 1
                        if login.checkUsername(login_inputs['Username'].Text):
                            login_textfields['Message'].Text = 'Username\nnot\nAvailable'
                            sign_up = 0
                        else:
                            login_textfields['Message'].Text = 'Confirm\nPassword'
                            password = login_inputs['Password'].Text
                            login_inputs['Password'].Text = ''
                    elif sign_up == 1:
                        sign_up = 2
                        if login.checkUsername(login_inputs['Username'].Text):
                            login_textfields['Message'].Text = 'Username\nnot\nAvailable'
                            sign_up = 0
                        else:
                            password2 = login_inputs['Password'].Text
                            if password == password2:
                                login.createAccount(login_inputs['Username'].Text, password)
                                total = 0
                                text = ''
                                login.setValue('Money', '\'{}\''.format(total))
                                login.setValue('Notes', '\'{}\''.format(text))
                            else:
                                password = ''
                                password2 = ''
                                sign_up = 0
                                login_textfields['Message'].Text = 'Passwords\ndon\'t match'
                    else:
                        login_textfields['Message'].Text = 'Information\nIncorrect'
                                
                    
        for value in login_textfields:
            login_textfields[value].draw()
            
        for value in login_inputs:
            login_inputs[value].update(keys, ticks)
            login_inputs[value].draw()
            
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(FPS)

if __name__ == '__main__':
    login()
    init() 
    buttons_init()
    text_init()
    input_init()
    
    add = 0
    old_ticks = 0
    

    # -------- Main Program Loop -----------
    while True:
        mouse_scroll = 0
        ticks = pygame.time.get_ticks()
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == QUIT: end()
            elif event.type == MOUSEMOTION: mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_left = True
                elif event.button == 2:
                    mouse_middle = True
                elif event.button == 3:
                    mouse_right = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_left = False
                elif event.button == 2:
                    mouse_middle = False
                elif event.button == 3:
                    mouse_right = False
                elif event.button == 4:
                    mouse_scroll = scroll_move
                elif event.button == 5:
                    mouse_scroll = -scroll_move
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
            elif event.type == KEYUP:
                keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]: end()
     
        # --- Game logic should go here
        # --- Drawing code should go here
        screen.fill((211,211,211))
        for value in buttons:
            buttons[value].update(ticks)
            buttons[value].draw()
            clicked = buttons[value].Clicked
            if clicked:
                if buttons[value] in money_buttons.values():
                    if buttons['Add'].down == True:
                        add -= float(value)
                    else:
                        add += float(value)
                    text_fields['Bottom'].Text = round(add, 2)
                if value == 'Clear':
                    add = 0
                    text_fields['Bottom'].Text = 0
                if value == 'Submit':
                    total += add
                    text_fields['Total'].Text = 'Your Total is:\n' + str(round(total, 2)) + '\n€'
                    add = 0
                    text_fields['Bottom'].Text = 0
        for text_field in text_fields:
            text_fields[text_field].draw()
        for i in inputs:
            inputs[i].update(keys, ticks)
            inputs[i].draw()
        text = inputs['Notes'].Text

        if old_ticks + 1000 < ticks and login.user == 'Administrator':
            if text[-1:] == ';':
                try:
                    exec(text[:-1])
                except Exception as e:
                    inputs['Notes'].Text = e
                else:
                    if text == inputs['Notes'].Text:
                        inputs['Notes'].Text = text[:-1]
            old_ticks = ticks
            
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(FPS)
