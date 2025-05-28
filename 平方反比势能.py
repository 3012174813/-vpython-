from vpython import *
import numpy as np

场景 = canvas(title='平方反比势能', width=800, height=600, background=color.white)

电荷量 = -1e-9  
库仑常数 = 9e9  
小球 = sphere(pos=vector(0, 0, 0), radius=1, color=color.red)

x最小值, x最大值 = -20, 20
z最小值, z最大值 = -5, 5
y最小值, y最大值 = -20, 20
步长 = 0.5

def 计算电势(位置, 电荷量, 小球位置):
    位置大小 = mag(位置 - 小球位置) if 位置 != 小球位置 else 1e-10
    电势值 = 库仑常数 * 电荷量 / 位置大小
    if 电势值 > y最大值:
        return y最大值
    elif 电势值 < y最小值:
        return y最小值
    return 电势值

def 绘图():
    for obj in 场景.objects:
        if isinstance(obj, quad):
            obj.visible = False
            del obj

    x点 = np.arange(x最小值, x最大值, 步长)
    z点 = np.arange(z最小值, z最大值, 步长)

    电势网格 = np.zeros((len(x点), len(z点)))
    for i in range(len(x点)):
        for j in range(len(z点)):
            位置 = vector(x点[i], 0, z点[j]) 
            电势网格[i, j] = 计算电势(位置, 电荷量, 小球.pos)

    四边形面 = []
    for i in range(len(x点) - 1):
        for j in range(len(z点) - 1):
            x1, z1, y1 = x点[i], z点[j], 电势网格[i, j]
            x2, z2, y2 = x点[i+1], z点[j], 电势网格[i+1, j]
            x3, z3, y3 = x点[i], z点[j+1], 电势网格[i, j+1]
            x4, z4, y4 = x点[i+1], z点[j+1], 电势网格[i+1, j+1]

            四边形面.append(quad(
                vs=[
                    vertex(pos=vector(x1, y1, z1), color=color.blue, opacity=0.5),
                    vertex(pos=vector(x2, y2, z2), color=color.blue, opacity=0.5),
                    vertex(pos=vector(x4, y4, z4), color=color.blue, opacity=0.5),
                    vertex(pos=vector(x3, y3, z3), color=color.blue, opacity=0.5)
                ] ))

def 更新电势图():
    global 电荷量
    电荷量 = 电量滑动条.value*1e-9
    电量标签.text = f'电荷量: {电荷量:.1e} C'
    绘图()

电量滑动条 = slider(min=-10, max=10, value=-1,step = 1, bind=更新电势图,pos = 场景.title_anchor)
电量标签 = wtext(text=f'', pos=场景.title_anchor)
更新电势图()

while True:
    rate(100)
