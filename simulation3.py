import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import math
import random
frame_dt = 0.1  #フレーム時間

fig, ax = plt.subplots(figsize=(6,6))
plt.subplots_adjust(left=0.25, bottom=0.25)

axcolor = 'gold'
ax_velocity = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_angular_velocity = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)

sli_v = Slider(ax_velocity, 'velocity', -1, 1, valinit=0, valstep=0.01)
sli_a = Slider(ax_angular_velocity, 'Angular_velocity', -1, 1, valinit=0, valstep=0.01)


position, = ax.plot([], [], "x")
direction, = ax.plot([], [], lw=1)


velocity_rate = 0.0
yaw_rate = 0.0

class Rover():
    def __init__(self):
        self.location_x = 0.0
        self.location_y = 0.0
        self.yaw =0.0
        self.length = 5
        self.speed = 1
        self.yaw_speed = 0.5
        self.color = "b"

    def move(self, velocity_rate, yaw_rate):
        self.yaw        += self.yaw_speed * yaw_rate * frame_dt
        self.location_x += self.speed * velocity_rate * math.cos(self.yaw) * frame_dt
        self.location_y += self.speed * velocity_rate * math.sin(self.yaw) * frame_dt
        position.set_data(self.location_x, self.location_y)
        position.set_color(self.color)
        direction.set_data([self.location_x, self.location_x + self.length*math.cos(self.yaw)],[self.location_y,self.location_y+self.length*math.sin(self.yaw)])

    def arrive_at(self, target):
        distance = math.sqrt((self.location_x - target.location_x)**2 + (self.location_y - target.location_y)**2)
        if (distance <= target.radius):
            self.color = "r"
        else:
            self.color = "b"

class Target():
    def __init__(self):
        self.location_x = random.randint(-45,45)
        self.location_y = random.randint(-45,45)
        self.radius = 5
        ax.plot(self.location_x, self.location_y, marker="H", markersize=7)

def update(_):
    global velocity_rate, yaw_rate
    velocity_rate = sli_v.val
    yaw_rate = sli_a.val

def main():

    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.axhline(y=0, c="k",lw=0.7)
    ax.axvline(x=0, c="k", lw=0.7)
    
    rover = Rover()
    target = Target()

    sli_v.on_changed(update)
    sli_a.on_changed(update)

    while True:
        loop(rover)
        rover.arrive_at(target)
        plt.pause(0.00001)

def loop(rover):
    '''
    以下の値（velocity_rate, yaw_rate）を変えるようなプログラムを書くと
    走行シミュレーションを作ることができる

    関数名が"loop"となってるように、arduinoプログラミングと同じ書き方で
    プログラムを書くことができる

    velocity_rate とは速度の割合のことで、例えば１ならば、MAXSPEEDで走る
    yaw_rate とは角速度の割合のことで、例えば１ならば、MAXSPEEDで左に旋回する

    -1 <= velocity_rate, yaw_rate <=1
    
    '''
    rover.move(velocity_rate,yaw_rate)

if __name__ == "__main__":
    main()
