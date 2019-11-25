import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random

#フレーム時間
frame_dt = 0.1  

fig, ax = plt.subplots(figsize=(6,6))
position, = ax.plot([], [], "x")
direction, = ax.plot([], [], lw=1)

class Rover():
    def __init__(self):
        
        self.location_x = 0.0   #ローバー初期位置
        self.location_y = 0.0

        self.yaw =0.0           #ローバー初期角度
        self.length = 5         #ローバーの首の長さ
        self.speed = 1          #ローバーの前進速度
        self.yaw_speed = 0.2    #ローバーの旋回速度
        self.color = "b"        #ローバーの色

    #ローバーを動かす関数
    #IN:    速度割合、角速度割合
    #OUT:   次のフレームにおけるローバーの位置と角度をプロット
    def move(self, velocity_rate, yaw_rate):
        self.yaw        -= self.yaw_speed * yaw_rate * frame_dt
        self.location_x += self.speed * velocity_rate * math.cos(self.yaw) * frame_dt
        self.location_y += self.speed * velocity_rate * math.sin(self.yaw) * frame_dt
        position.set_data(self.location_x, self.location_y)
        position.set_color(self.color)
        direction.set_data([self.location_x, self.location_x + self.length * math.cos(self.yaw)], [self.location_y, self.location_y + self.length * math.sin(self.yaw)])
    
    #接近できたか判定する関数
    #IN:    ターゲットオブジェクト
    #OUT    ターゲットに接近できたか判定
    def arrive_at(self, target):
        distance = math.sqrt((self.location_x - target.location_x)**2 + (self.location_y - target.location_y)**2)
        if (distance <= target.radius):
            self.color = "r"
            target.location_x = random.randint(-45, 45)
            target.location_y = random.randint(-45, 45)
            ax.plot(target.location_x, target.location_y, marker="H", markersize=7)
        else:
            self.color = "b"

class Target():
    def __init__(self):
        self.location_x = random.randint(-45,45)    #ターゲットの初期位置
        self.location_y = random.randint(-45,45)

        self.radius = 5 #ターゲットの半径
        ax.plot(self.location_x, self.location_y, marker="H", markersize=7)

#回転行列関数
#IN:    ベクトルx, 回転角t
#OUT:   回転後のベクトル
def rotation(x, t):
    a = np.array([[np.cos(t), -np.sin(t)],
                  [np.sin(t),  np.cos(t)]])
    ax = np.dot(a, x)        
    return ax

def main():

    #表描画
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.axhline(y=0, c="k",lw=0.7)
    ax.axvline(x=0, c="k", lw=0.7)
    
    #各クラスのインスタンス生成
    rover = Rover()
    target = Target()

    while True:
        loop(rover,target)
        rover.arrive_at(target)
        plt.pause(0.00001)

#アルディーノのループ関数に似せた関数
#IN:    ローバー、ターゲットのオブジェクト
#OUT    ローバーを移動させる
def loop(rover, target):
    '''
    以下の値（velocity_rate, yaw_rate）を変えるようなプログラムを書くと
    走行シミュレーションを作ることができる

    関数名が"loop"となってるように、arduinoプログラミングと同じ書き方で
    プログラムを書くことができる

    velocity_rate とは速度の割合のことで、例えば１ならば、MAXSPEEDで走る
    yaw_rate とは角速度の割合のことで、例えば１ならば、MAXSPEEDで左に旋回する

    '''

    #ローバーを中心としたグローバル座標におけるターゲットベクトルの角度
    radT = math.atan2(target.location_y - rover.location_y, target.location_x - rover.location_x)

    #ローバーが向いてる方向のベクトル
    vr = np.array([math.cos(rover.yaw), math.sin(rover.yaw)])

    #グローバル座標からターゲットベクトルを起点とした座標に変換
    rotated_vr = rotation(vr, -radT)

    #ターゲットベクトル座標におけるローバーが向いてる方向の角度
    rotated_rad = math.atan2(rotated_vr[1], rotated_vr[0])
    
    velocity_rate = 1
    yaw_rate = rotated_rad

    rover.move(velocity_rate, yaw_rate)

if __name__ == "__main__":
    main()
