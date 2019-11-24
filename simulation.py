import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import math
import random

mouse_x, mouse_y = 0.0,0.0

fig = plt.figure(figsize=(11,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

line, = ax2.plot([], [], lw=1)
rover, = ax1.plot([], [], "x")
direction, = ax1.plot([], [], lw=1)


class Rover():
    def __init__(self):
        self.location_x = 0.0
        self.location_y = 0.0
        self.dt = 0.1
        self.length = 5
        self.speed = 2
        self.color = "b"

    def move(self, strength_x, strength_y, yaw):
        self.location_x += self.speed * strength_x * self.dt
        self.location_y += self.speed * strength_y * self.dt
        rover.set_data(self.location_x, self.location_y)
        rover.set_color(self.color)
        direction.set_data([self.location_x, self.location_x + self.length*math.cos(yaw)],[self.location_y,self.location_y+self.length*math.sin(yaw)])

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
        ax1.plot(self.location_x, self.location_y, marker="H",markersize=7)

def motion(event):
    global mouse_x,mouse_y
    mouse_x = event.xdata
    mouse_y = event.ydata
    if event.inaxes == ax2:
        line.set_data([0,mouse_x],[0,mouse_y] )
    else:
        line.set_data([0,0],[0,0])


def main():
 

    ax2.set_xlim(-3, 3)
    ax2.set_ylim(-3, 3)
    ax2.axhline(y=0, c="k",lw=0.7)
    ax2.axvline(x=0, c="k", lw=0.7)
    
    ax1.set_xlim(-50, 50)
    ax1.set_ylim(-50, 50)
    ax1.axhline(y=0, c="k",lw=0.7)
    ax1.axvline(x=0, c="k",lw=0.7)

    c = patches.Circle(xy=(0, 0), radius=1, fc="white",ec='dodgerblue')
    ax2.add_patch(c)
    
    rover = Rover()
    target = Target()


    plt.connect('motion_notify_event', motion)
    while True:
        if mouse_x:
            rover.move(mouse_x, mouse_y, math.atan2(mouse_y, mouse_x))
        
        rover.arrive_at(target)
        plt.pause(0.00001)

if __name__ == "__main__":
    main()
