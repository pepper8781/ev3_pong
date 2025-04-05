#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import random
import time  # Add this line to import the 'time' module

# Create your objects here.
ev3 = EV3Brick()

# Write your program here.
ev3.speaker.beep()

random.seed(round(time.time()))

motor_a = Motor(Port.A)

class Bar_1():
    def __init__(self):
        self.x = 10
        self.y_top = motor_a.angle() + 49
        self.screen_top = 0
        self.screen_bottom = 127
        self.bar_top = self.y_top - self.screen_top
    
    def display_bar(self):
        self.y_top = motor_a.angle() + 49
        if self.y_top < self.screen_top:
            self.screen_top = self.y_top
            self.screen_bottom = self.screen_top + 127
        
        if self.y_top + 30 > self.screen_bottom:
            self.screen_bottom = self.y_top + 30
            self.screen_top = self.screen_bottom - 127

        self.bar_top = self.y_top - self.screen_top

        ev3.screen.draw_line(x1=self.x,y1=self.bar_top,x2=self.x,y2=self.bar_top+30)

motor_b = Motor(Port.B)

class Bar_2():
    def __init__(self):
        self.x = 167
        self.y_top = motor_b.angle() + 49
        self.screen_top = 0
        self.screen_bottom = 127
        self.bar_top = self.y_top - self.screen_top
    
    def display_bar(self):
        self.y_top = motor_b.angle() + 49
        if self.y_top < self.screen_top:
            self.screen_top = self.y_top
            self.screen_bottom = self.screen_top + 127
        
        if self.y_top + 40 > self.screen_bottom:
            self.screen_bottom = self.y_top + 30
            self.screen_top = self.screen_bottom - 127

        self.bar_top = self.y_top - self.screen_top
        
        ev3.screen.draw_line(x1=self.x,y1=self.bar_top,x2=self.x,y2=self.bar_top+30)

class Pong():
    def __init__(self):
        self.x = 83
        self.y = 68
        self.start_x = random.randint(1, 100)
        self.start_y = random.randint(1, 100)
        if self.start_x % 2 == 1:
            self.x_direction = 2
        else:
            self.x_direction = -2
        if self.start_y % 2 == 1:
            self.y_direction = 2
        else:
            self.y_direction = -2
        self.fin = False
        self.winner = 0

    def move(self, bar1_y, bar2_y):
        self.x += self.x_direction
        self.y += self.y_direction
        if self.x+4 >= 177 or self.x <= 0:
            self.fin = True
            if self.x+4 >= 177:
                self.winner = 1
            else:
                self.winner = 2
        elif self.x-4 <= 10:
            if self.y-4 >= bar1_y and self.y+4 <= bar1_y+ 30:
                self.x_direction = 2
            else:
                pass
        elif self.x+4 >= 167:
            if self.y-4 >= bar2_y and self.y+4 <= bar2_y + 30:
                self.x_direction = -2
            else:
                pass
        if self.y >= 127 or self.y <= 0:            
            self.y_direction *= -1
        
    def disp(self):
        ev3.screen.draw_box(x1=self.x-4,y1=self.y-4,x2=self.x+4,y2=self.y+4,fill=True)

bar1 = Bar_1()
bar2 = Bar_2()
pong = Pong()

while True:
    ev3.screen.clear()
    bar1.display_bar()
    bar2.display_bar()
    pong.disp()
    pong.move(bar1.bar_top , bar2.bar_top)
    if pong.fin:
        break
    wait(50)
ev3.speaker.beep()
ev3.screen.clear()
text = str(pong.winner)+"P WIN!!"
ev3.screen.draw_text(88, 68, text)
wait(3000)