from vpython import *

场景 = canvas(title='轮上棍轨迹模拟 - 转动变直线往复运动', width=800, height=600, background=color.white,align='left')

车轮半径 = 2
速度 = 4
角位移 = 0
棍长 = 6

时间 = 0
dt = 0.01

轨道 = box(pos=vector(3, 0, 0), size=vector(6, 0.1, 0.1))
圆环 = ring(pos=vector(-3, 0, 0), axis=vector(0, 0, 1), radius=车轮半径, thickness=0.2, color=color.blue)
棍 = box(pos=vector(-3, 0, 0), size=vector(棍长, 0.2, 0.2), color=color.red)
球 = sphere(radius=0.4, color=color.green)

辐条列表 = []
for i in range(6):
    角度 = 2 * pi * i / 6
    终点 = vector(车轮半径 * cos(角度), 车轮半径 * sin(角度), 0)
    辐条 = cylinder(pos=圆环.pos, axis=终点, radius=0.05, color=color.orange)
    辐条列表.append(辐条)

xt图 = graph(title='往复运动xt图', xtitle='时间 (s)', ytitle='位置 (m)',align='right')
位置曲线 = gcurve(color=color.red, graph=xt图)

while True:
    rate(100) 
    角位移 += 速度 / 车轮半径 * dt
    时间 += dt

    for i, 辐条 in enumerate(辐条列表):
        角度 = 2 * pi * i / 6 - 角位移
        辐条.axis = vector(车轮半径 * cos(角度), 车轮半径 * sin(角度), 0)

    轮棍点x = 圆环.pos.x +车轮半径 * cos(-角位移)
    轮棍点y = 车轮半径 * sin(-角位移)
  
    球x = 轮棍点x + sqrt(棍长**2 - 轮棍点y**2)
    球.pos = vector(球x, 0, 0) 

    xt图.xmin = max(0,时间-10) 
    xt图.xmax = max(时间, 10 )
    位置曲线.plot(时间, 球x)

    棍中心x = (轮棍点x + 球x) / 2
    棍中心y = (0 + 轮棍点y) / 2
    棍.pos = vector(棍中心x, 棍中心y, 0)
    棍.axis = vector(球x - 轮棍点x, -轮棍点y, 0)
