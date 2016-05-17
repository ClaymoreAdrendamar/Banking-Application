import pygame, sys
from pygame.locals import *

#initialise correct keyboard
def keyboard_init():
    global keys, K_a, K_z, K_m, K_q, K_w, K_l
    keys = pygame.key.get_pressed()
    K_a = 113
    K_z = 119
    K_m = 59
    K_q = 97
    K_w = 122
    K_l = 108
    

#Initiate the programe
def init():
    global font, SIZE, screen, clock, FPS, in_text, mouse_x, mouse_y,\
    mouse_left, mouse_middle, mouse_right
    
    pygame.init()
    font = pygame.font.Font(None, 30)
    #set the window size (width and height
    SIZE = [800, 600]
    screen = pygame.display.set_mode(SIZE)

    #set window title
    pygame.display.set_caption("text/input test")

     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    FPS = 60

    in_text = Input(50, 50, 110)

    mouse_x = mouse_y = 0
    mouse_left = mouse_middle = mouse_right = False

#End the program
def end():
    pygame.quit()
    sys.exit()

#Play a sound
def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)

#Print text
def print_text(font, x, y, text, colour = (255, 255, 255), target = None):
    """Prints text at a given position and a given font,
       optional colour and surface arguments"""
    texts = text.split('\n')
    img_texts = list()
    for text in texts:
        img_texts.append(font.render(text, True, colour))
    if not target:
        target = pygame.display.get_surface()
    for imgText in img_texts:        
        target.blit(imgText, (x,y))
        y += imgText.get_height() + 2

#Point Class
class Point(object):
    """Represents a two dimensional point with X and Y coordinates"""
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    #X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    X = property(getx, setx)

    #Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    Y = property(gety, sety)

    #Get the distance from another point
    def dist(self, other=None):
        if not other:
            other = type(self)(0,0)
        return math.hypot(self.__x - other.X, self.__y - other.Y)

    def angle(self, other=None):
        if not other:
            other = type(self)(0,0)
        delta = Point(0,0)
        delta.X = self.X - other.X
        delta.Y = self.Y - other.Y
        angle = math.atan2(delta.Y, delta.X)
        angle = math.degrees(angle)-90
        return wrap_angle(angle)

    #retur string
    def __str__(self):
        return "[X: {:.0f}, Y: {:.0f}]".format(self.__x, self.__y)

class Input(object):
    def __init__(self, x, y, width, surface=None, max_char = 0):
        self.surface = surface
        if surface == None:
            self.surface = pygame.display.get_surface()
        self.rect = pygame.Rect(x,y,width,17)
        self.colour = pygame.Color(248,248,255)
        self.shadow = pygame.Color(105,105,105)
        self.text_colour = pygame.Color(0,0,0)
        self.font = pygame.font.Font(None, 15)
        if max_char > width /3 or max_char == 0:
            self.max_char = int(width/7)
        else:
            self.max_char = int(max_char)
        self.text = ''
        self.selected = False
        self.last_tick = 0
        self.answered = False

    def draw(self):
        pygame.draw.rect(self.surface, self.colour, self.rect)
        pygame.draw.rect(self.surface, self.shadow, (self.rect.x,self.rect.y,self.rect.width, 2))
        pygame.draw.rect(self.surface, self.shadow, (self.rect.x,self.rect.y,2,self.rect.height))
        print_text(self.font, self.rect.x+4, self.rect.y+4, self.text[:self.max_char], self.text_colour, self.surface)

    def update(self, ticks):
        if not self.selected:
            if mouse_x > self.rect.x and mouse_x < self.rect.right and \
               mouse_y > self.rect.y and mouse_y < self.rect.bottom and mouse_left:
                self.selected = True
                self.text = ''
                self.answered = False
        elif self.selected:
            global keys
            if self.last_tick + 100 < ticks:
                for letter in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',\
                               'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
                    self.add(letter)
                self.last_tick = ticks
                if keys[K_BACKSPACE]:
                    self.add('a', True)
                if keys[K_RETURN]:
                    self.answered = True
                    self.selected = False

    def add(self, letter, remove=False):
        if remove:
            self.text = self.text[:-1]
            return 0
        if keys[eval('K_'+letter)]:
            self.text += letter
            self.text = self.text[:self.max_char]
            
            
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
        self.clicked = False
        self.text_pos = Point(self.rect.x+self.shade_width*2, self.rect.y+self.shade_width*2)
        self.unClick()
        

    def update(self):
        if mouse_x > self.rect.x and mouse_x < self.rect.right and \
               mouse_y > self.rect.y and mouse_y < self.rect.bottom and mouse_left:
            self.click()
            
        if mouse_x > self.rect.x and mouse_x < self.rect.right and \
               mouse_y > self.rect.y and mouse_y < self.rect.bottom and not mouse_left and self.down == True:
            self.clicked = True
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
        pygame.draw.rect(self.image, self.shade_colour, rect1)
        pygame.draw.rect(self.image, self.shade_colour, rect2)
        print_text(self.font, self.text_pos.X, self.text_pos.Y, self.text, self.text_colour, self.image)
        
        
    def unClick(self):
        self.down = False
        
        self.text_pos = Point(self.shade_width*2, self.shade_width*2)
        rect1 = pygame.Rect(0, self.rect.height - self.shade_width, self.rect.width, self.shade_width) #bottom
        rect2 = pygame.Rect(self.rect.width - self.shade_width, 0, self.shade_width, self.rect.height) #right
        
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.shade_colour, rect1)
        pygame.draw.rect(self.image, self.shade_colour, rect2)
        print_text(self.font, self.text_pos.X, self.text_pos.Y, self.text, self.text_colour, self.image)
    


if __name__ == '__main__':
    init()
    keyboard_init()

    button = Button(300, 300, 100, 40, font, surface=None, text='Button')

    # -------- Main Program Loop -----------
    while True:
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
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
            elif event.type == KEYUP:
                keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]: end()
     
        # --- Game logic should go here
        in_text.update(ticks)
        button.update()
        # --- Drawing code should go here
        screen.fill((211,211,211))
        if in_text.answered:
            print_text(font, 400, 300, in_text.text, (255, 0, 0))
        if button.clicked:
            print_text(font, 400, 350, 'Clicked!', (255, 0, 0))
            button.clicked = False
        in_text.draw()
        button.draw()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(FPS)


