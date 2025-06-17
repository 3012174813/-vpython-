from vpython import *

场景 = canvas(title='轮上点轨迹模拟', width=1500, height=300, background=color.white)

车轮半径 = 2.0  
速度 = 4
角位移 = 0
dt = 0.01

地面 = box(pos=vector(0, -2.2, 0), size=vector(30, 0.1, 5),  color=color.green)
圆环 = ring(pos=vector(-10, 0, 0), axis=vector(0, 0, 1), radius=2, thickness=0.2, color=color.blue)
轨迹点 = sphere( radius=0.3,color=color.red, make_trail=True)
辐条列表 = []
for i in range(6):
    角度 = 2 * pi * i / 6
    终点 = vector(车轮半径 * cos(角度), 车轮半径 * sin(角度), 0)
    辐条 = cylinder(pos=圆环.pos, axis=终点, radius=0.05, color=color.orange)
    辐条列表.append(辐条)

距离滑块 = slider(min=0, max=车轮半径, value=0.8, step=0.1,bind = None, pos=场景.title_anchor)

while True:
    rate(100) 

    圆环.pos.x += 速度 * dt
    角位移 += 速度 / 车轮半径 * dt

    for i, 辐条 in enumerate(辐条列表):
        角度 = 2 * pi * i / 6 - 角位移
        辐条.pos.x = 圆环.pos.x 
        辐条.axis = vector(车轮半径 * cos(角度), 车轮半径 * sin(角度), 0)

    点相对位置 = vector(距离滑块.value * cos(-角位移), 距离滑块.value * sin(-角位移), 0)
    轨迹点.pos = 圆环.pos + 点相对位置

    if 圆环.pos.x > 20:        
        轨迹点.clear_trail()
        圆环.pos.x = -圆环.pos.x