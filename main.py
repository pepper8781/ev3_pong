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
motor_b = Motor(Port.B)

class Bar():
    bar_length = 30
    
    def __init__(self, x, motor, screen_height):
        self.motor = motor
        self.correction = 49
        self.x = x
        self.y_top = self.motor.angle() + self.correction
        self.screen_height = screen_height
        self.screen_top = 0
        self.screen_bottom = self.screen_height
        self.bar_top = self.y_top - self.screen_top
    
    def display_bar(self):
        self.y_top = self.motor.angle() + self.correction
        if self.y_top < self.screen_top:
            self.screen_top = self.y_top
            self.screen_bottom = self.screen_top + self.screen_height
        
        if self.y_top + Bar.bar_length > self.screen_bottom:
            self.screen_bottom = self.y_top + Bar.bar_length
            self.screen_top = self.screen_bottom - self.screen_height

        self.bar_top = self.y_top - self.screen_top

        ev3.screen.draw_line(x1=self.x,y1=self.bar_top,x2=self.x,y2=self.bar_top+Bar.bar_length)

class Pong():
    def __init__(self, bar1, bar2, screen_height, screen_width):
        self.x = 83
        self.y = 68
        self.start_x = random.randint(1, 100)
        self.start_y = random.randint(1, 100)
        self.speed = 2
        if self.start_x % 2 == 1:
            self.x_direction = self.speed
        else:
            self.x_direction = -self.speed
        if self.start_y % 2 == 1:
            self.y_direction = self.speed
        else:
            self.y_direction = -self.speed
        self.fin = False
        self.winner = 0
        self.box_half_size = 4
        self.bar1 = bar1
        self.bar2 = bar2
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.display_height = screen_height
        self.display_width = screen_width

    def move(self, bar1_y, bar2_y):
        self.x += self.x_direction
        self.y += self.y_direction
        if self.x+self.box_half_size >= self.display_width or self.x <= 0:
            self.fin = True
            if self.x+self.box_half_size >= self.display_width:
                self.winner = 1
            else:
                self.winner = 2
        elif self.x-self.box_half_size <= self.bar1.x:
            if self.y-self.box_half_size >= self.bar1.y_top and self.y+self.box_half_size <= self.bar1.y_top+ Bar.bar_length:
                self.x_direction = self.speed
            else:
                pass
        elif self.x+self.box_half_size >= self.bar2.x:
            if self.y-self.box_half_size >= self.bar2.y_top and self.y+self.box_half_size <= self.bar2.y_top+ Bar.bar_length:
                self.x_direction = -self.speed
            else:
                pass
        if self.y >= self.display_height or self.y <= 0:            
            self.y_direction *= -1
        
    def draw(self):
        ev3.screen.draw_box(x1=self.x-4,y1=self.y-4,x2=self.x+4,y2=self.y+4,fill=True)

class Game():
    def __init__(self):
        self.screen_height = 127
        self.screen_width = 177
        self.bar1 = Bar(10, motor_a, self.screen_height)
        self.bar2 = Bar(167, motor_b, self.screen_height)
        self.pong = Pong(self.bar1, self.bar2, self.screen_height, self.screen_width)
        self.game_over = False
        self.refresh_rate = 50
    
    def process(self):
        ev3.screen.clear()
        self.bar1.display_bar()
        self.bar2.display_bar()
        self.pong.move(self.bar1.bar_top, self.bar2.bar_top)
        self.pong.draw()
        wait(self.refresh_rate)

game = Game()

while not game.game_over:
    game.process()

ev3.speaker.beep()
ev3.screen.clear()
text = str(game.pong.winner)+"P WIN!!"
ev3.screen.draw_text(game.screen_width//2, game.screen_height//2, text)
wait(3000)