from vpython import *
import random

场景 = canvas(title='电子跃迁模拟', width=1000, height=700, background=color.white)

原子列表 = []
电子列表 = []
光子列表 = []

for i in range(5):
    原子位置 = vector(-10 + i*5, -4, 0)
    原子 = sphere(pos=原子位置, radius=1, color=color.yellow)
    原子列表.append(原子)
 
    轨道列表 = []
    for n in range(1, 5):
        轨道半径 = (2 - 1/n**2) * 5
        轨道位置 = 原子位置 + vector(0, 轨道半径, 0)
        轨道能量 = -13.6 / (n**2)
        轨道 = box(pos=轨道位置, size=vector(3, 0.1, 0.1), color=color.white, 能量=轨道能量, n=n)
        轨道列表.append(轨道)
        能级标签 = label(pos=轨道位置 + vector(-2.5, 0, 0), text=f"{轨道能量:.2f}eV", box=False)
    
    原子.轨道列表 = 轨道列表

    初始轨道 = 轨道列表[0]
    电子 = sphere(pos=初始轨道.pos ,radius=0.3,color=color.blue,能级轨道=1,所属原子=原子,停留时间=0,跃迁时间=0)
    电子列表.append(电子)

光子能量滑块 = slider(min=10, max=13, value=10.2, step=0.01, pos=场景.title_anchor, bind=lambda: 更新参数())
能量标签 = label(pos=vector(0, -1, 0), box=False)

def 更新参数():
    能量标签.text = f'光子能量: {光子能量滑块.value:.2f} eV'

更新参数()

def 发射光子():
    for _ in range(5):
        初始位置 = vector(random.uniform(-10,10), random.uniform(0, 8), 2)
        光子 = sphere(
            pos=初始位置,
            radius=0.2,
            color=color.green,
            能量=光子能量滑块.value,
            速度=vector(0, 0, -0.1),
           
        )
        光子列表.append(光子)

def 处理碰撞():
    for 光子 in 光子列表[:]:
        for 电子 in 电子列表[:]:
            if mag(光子.pos - 电子.pos) < 1:
                能级轨道 = 电子.能级轨道
                原子 = 电子.所属原子
                当前轨道能量 = 原子.轨道列表[能级轨道-1].能量
                
                for 轨道 in 原子.轨道列表:
                    if 轨道.n == 能级轨道:
                        continue
                    ΔE = 轨道.能量 - 当前轨道能量
                    if abs(光子.能量 - ΔE) < 0.1:
                    
                        电子.能级轨道 = 轨道.n
                        电子.pos = 轨道.pos 
                
                        if 轨道.n > 能级轨道:
                            电子.跃迁时间 = random.uniform(1, 3)
                        电子.停留时间 = 0
                   
                        光子.visible = False
                        光子列表.remove(光子)
                        break

def 电子跃迁():

    for 电子 in 电子列表:
        if 电子.能级轨道 > 1:
            电子.停留时间 += 0.02
            
            if 电子.停留时间 >= 电子.跃迁时间:

                可选轨道 = [n for n in range(1, 电子.能级轨道)]
                if not 可选轨道:
                    continue
                新能级 = random.choice(可选轨道)

                原子 = 电子.所属原子
                旧轨道能量 = 原子.轨道列表[电子.能级轨道-1].能量
                新轨道能量 = 原子.轨道列表[新能级-1].能量
                能量差 = 新轨道能量 - 旧轨道能量
                
                光子 = sphere(pos=电子.pos+vector(0,1, 0),radius=0.2,color=color.red,能量=abs(能量差),速度=vector(0, 0.1, 0),)
                光子列表.append(光子)
     
                电子.能级轨道 = 新能级
                电子.pos = 原子.轨道列表[新能级-1].pos 
                电子.停留时间 = 0
                电子.跃迁时间 = random.uniform(1, 3) if 新能级 > 1 else 0



while True:
    rate(100)

    if random.random() < 0.1:
        发射光子()

    for 光子 in 光子列表[:]:
        光子.pos += 光子.速度
        if 光子.pos.z < -1 or 光子.pos.y > 8:
            光子.visible = False
            光子列表.remove(光子)
    
    处理碰撞()
    电子跃迁()
    