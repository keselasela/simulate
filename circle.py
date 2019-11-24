
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
 
def ellipse(x, a, b, g):
    y = []      # y値をためる
    imgs = []   # プロットをためる入れ物
    c = 1       # y軸の符号スイッチ
 
    # 第1象限から第4象限までの全てのy値を計算
    for i in range(len(g)):
        y_single = b * np.sqrt(1 - (np.power(x[i], 2) / np.power(a, 2)))
        if i == 0:
            pass
        elif np.sign(g[i - 1]) == np.sign(g[i]):
            pass
        else:
            c = -1 * c
 
        y.append(y_single * c)  # y値の符号調整
 
        # グラフ描画
        plt.rcParams['font.size'] = 14
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xticks(np.arange(-2, 2, 0.5))
        plt.yticks(np.arange(-2, 2, 0.5))
        plt.xlim(-1.5, 1.5)
        plt.ylim(-1.5, 1.5)
 
        # アニメーション用データ作成
        img = plt.plot(x[i], x[i]*x[i], 'b-o')
        imgs.append(img)
    return y, imgs  # 楕円軌道のy値と、アニメーション用プロットを返す
 
a = 1.0                                 # 楕円方程式のa
b = 0.5                                 # 楕円方程式のb
t = np.linspace(-1 * np.pi, np.pi, 100) # －π～πまでの範囲
phase = 0                               # 位相
x = a * np.sin(t - phase)               # 1周期分の正弦波を作成
g = np.gradient(x)                      # xの勾配を計算
 
fig = plt.figure(figsize = (5, 4))      # プロットにためる前にfigureを作っておく
 
y, imgs = ellipse(x, a, b, g)           # 楕円軌道のプロットデータを関数で計算
 
# アニメーションを作る
ani = animation.ArtistAnimation(fig, imgs, interval=10)
ani.save('ellipse-course.gif', writer = 'imagemagick', fps = 30)
 
# グラフを表示する
plt.show()
plt.close()