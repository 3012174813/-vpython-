from vpython import *

场景 = canvas(title='轮上棍轨迹模拟', width=800, height=600, background=color.white)

车轮半径 = 2.0  
速度 = 4
角位移 = 0
dt = 0.01

圆环 = ring(pos=vector(0, 0, 0), axis=vector(0, 0, 1), radius=2, thickness=0.2, color=color.blue)
棍 = box(pos=vector(0, 0, 0), size=vector(6, 0.2, 0.2), color=color.red)
球 = sphere( radius=0.3, color=color.green, make_trail=True,retain=100)
辐条列表 = []
for i in range(6):
    角度 = 2 * pi * i / 6
    终点 = vector(车轮半径 * cos(角度), 车轮半径 * sin(角度), 0)
    辐条 = cylinder(pos=圆环.pos, axis=终点, radius=0.05, color=color.orange)
    辐条列表.append(辐条)

while True:
    rate(100) 
    角位移 += 速度 / 车轮半径 * dt

    for i, 辐条 in enumerate(辐条列表):
        角度 = 2 * pi * i / 6 - 角位移
        辐条.axis = vector(车轮半径 * cos(角度), 车轮半径 * sin(角度), 0)

    棍.pos =  vector(2 * cos(-角位移)+3, 2 * sin(-角位移), 0)
    球.pos = vector(2 * cos(-角位移) + 6, 2 * sin(-角位移), 0)
