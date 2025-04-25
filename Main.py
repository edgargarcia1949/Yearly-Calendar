import pygame, sys, asyncio 
from datetime import datetime, time
import calendar
import pygame_widgets
from pygame_widgets.button import Button

pygame.font.init()
font12 = pygame.font.Font("OpenSans-Bold.ttf", 12)
font16 = pygame.font.Font("OpenSans-Bold.ttf", 16)
font24 = pygame.font.Font("OpenSans-SemiBold.ttf", 24)
font26b = pygame.font.Font("OpenSans-Bold.ttf", 26)
font65 = pygame.font.Font("OpenSans-Bold.ttf", 65)

BLACK, WHITE, BLUE, GREEN, MAROON = (0,0,0), (255,255,255), (0,0,255), (0,128,0), (128,0,0) 
PURPLE, TEAL, FUCHSIA, LIME, OLIVE = (128,0,128), (0,128,128), (255,0,255), (0,255,0), (128,128,0) 
NAVYBLUE, RED, ORANGE, AQUA, TAN = (0,0,128), (255,0,0), (255,165,0), (0,255,255), (255,255,200)
COLOURS = [BLUE, GREEN, MAROON, PURPLE, TEAL, FUCHSIA, LIME, OLIVE, NAVYBLUE, RED, ORANGE, AQUA]

MONTH_STRINGS=["DECEMBER", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST",
            "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY"]
WEEK_STRINGS_SHORT=["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
DAY_NUMBERS=[" 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9","10","11","12","13","14","15",
      "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]     
      
RECT7 = (42, 32, 840, 54)     # first and second are position coordinates of rects
RECT8 = (42, 32, 840, 625)    # third and fourth are widths and heights of rects

X1, Y1, Y2, SX1, SY1 = 42, 86, 190, 210, 23

WIDTH = 924
HEIGHT = 714

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT]) 

class MV:
    year = datetime.now().year
    monthYear = []    # list of 12 MonthYr class instances

class MonthYear:
    def __init__(self, nameofmth):
        self.nameofmth = nameofmth  # January through December
        self.stday = 0       # start day from 0 to 6
        self.daysinmth = 0   # from 28 to 31
        self.x = 0           # x position on screen
        self.y = 0           # y position on screen
 
    def do_small_calendar(self, screen):
        ctr=self.stday
        for i in range(self.daysinmth):
            Text.do_text_year(screen, DAY_NUMBERS[i], self.x+ctr%7*30, self.y+ctr//7*25, 30, 25, BLACK, font16)
            ctr+=1         

class Rect:            
    def do_rect(screen, x, y, w, h):
        pygame.draw.rect(screen, BLACK, (x, y, w, h), 1)

class Text:   
    def do_text_year(screen, str, x, y, w, h, color, font):
        i, j = font.size(str)
        text = font.render(str, True, color)
        screen.blit(text, dest = (x+w/2-i/2, y+h/2-j/2))    

class DSY:            
    def year_buttons(screen, bool):            
        def go_ahead():
            MV.year+=1
            DSY.initialize_year()
        
        def go_back():
            MV.year-=1
            DSY.initialize_year()
        
        if bool:                  
            global button
            button = Button(screen, 830, 40, 40, 40, text = '+', font=font26b, margin=10,
                 inactiveColour=(255, 255, 200), hoverColour=(255, 100, 255),
                 pressedColour=(0, 200, 20), radius=20, onClick=lambda: go_ahead())
            global button2
            button2 = Button(screen, 780, 40, 40, 40, text = '-', font=font26b, margin=10,
                 inactiveColour=(255, 255, 200), hoverColour=(255, 100, 255),
                 pressedColour=(0, 200, 20), radius=20, onClick=lambda: go_back())
        else:
            button = None    # done to prevent buttons overlapping
            button2 = None
            
    def initialize_year():
        MV.monthYear = []
        for i in range(12):
            MV.monthYear.append(MonthYear(MONTH_STRINGS[i+1]))
        for i in range(12):
            data = calendar.monthrange(MV.year, i+1)
            MV.monthYear[i].stday = (data[0]+1)%7    # stday instance variable calculated
            MV.monthYear[i].daysinmth = data[1]      # daysinmth instance variable calculated
        for i in range (4):
            for j in range (3):             
                MV.monthYear[i+j*4].x = 42+i*210     # x for small calendar display calculated
                MV.monthYear[i+j*4].y = 124+j*190     # y for small calendar display calculated
        return MV.monthYear 
        
async def main():
    DSY.year_buttons(screen, True)
    show_buttons = True
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:            # up arrow toggles showing of buttons
                    show_buttons = not show_buttons
                if event.key == pygame.K_DOWN:
                    pygame.image.save(screen, 
                        datetime.now().strftime("YearlyCalendar-%m-%d-%y-%H-%M-%S")+".png")    
        screen.fill(WHITE)
        pygame.display.set_caption("Yearly Calendar")
        MV.monthYear = DSY.initialize_year()
            # calc year variables 
        Rect.do_rect(screen, *RECT7)        # top rect around year number
        for i in range (4):
            for j in range (3):
                Rect.do_rect(screen, X1+i*SX1, Y1+j*Y2, SX1, SY1)
                    # rectangle around month name
                Rect.do_rect(screen, X1+i*SX1, Y1+j*Y2, SX1, Y2)
                    # rectangle to separate months
                Text.do_text_year(screen, MV.monthYear[i+j*4].nameofmth,
                    X1+i*SX1, 85+j*Y2, SX1, SY1, COLOURS[i+j*4], font24)   # display month names
        Rect.do_rect(screen, *RECT8)          # rect around body of calendar       
        Text.do_text_year(screen, str(MV.year),  X1-30, 55, 900, 5, BLUE, font65)
            # display year in big letters
        [Text.do_text_year(screen, WEEK_STRINGS_SHORT[k],
            43+k*30+i*SX1, 107+j*Y2, 30, SY1, COLOURS[i+j*4], font12)
        for i in range (4) for j in range (3) for k in range(7)]  # display SUN through SAT 12 times
        [MV.monthYear[i].do_small_calendar(screen) for i in range (12)]
           # displays all 12 small calendars   
        if show_buttons:
            pygame_widgets.update(events)      # text boxes can be turned off with up arrow
            pygame.draw.circle(screen, BLACK, (850, 60), 20, 3)     # for looks
            pygame.draw.circle(screen, BLACK, (800, 60), 20, 3)
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())        
       
       
    




