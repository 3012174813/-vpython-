from vpython import *
import numpy as np

场景 = canvas(title='电势叠加', width=800, height=600, background=color.white)

电荷量1 = -1e-9  
电荷量2 = 1e-9
库仑常数 = 9e9  
小球1 = sphere(pos=vector(-5, 0, 0), radius=1, color=color.red)
小球2 = sphere(pos=vector(5, 0, 0), radius=1, color=color.blue)

x最小值, x最大值 = -20, 20
z最小值, z最大值 = -5, 5
y最小值, y最大值 = -20, 20
步长 = 0.5

def 计算电势(位置, 电荷量1, 电荷量2, 小球1位置, 小球2位置):
    位置大小1 = mag(位置 - 小球1位置) if 位置 != 小球1位置 else 1e-10
    电势值1 = 库仑常数 * 电荷量1 / 位置大小1

    位置大小2 = mag(位置 - 小球2位置) if 位置 != 小球2位置 else 1e-10
    电势值2 = 库仑常数 * 电荷量2 / 位置大小2
    
    总电势 = 电势值1 + 电势值2

    if 总电势 > y最大值:
        return y最大值
    elif 总电势 < y最小值:
        return y最小值
    return 总电势

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
            电势网格[i, j] = 计算电势(位置, 电荷量1, 电荷量2, 小球1.pos, 小球2.pos)

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
    global 电荷量1, 电荷量2
    电荷量1 = 电量滑动条1.value * 1e-9
    电荷量2 = 电量滑动条2.value * 1e-9
    小球2.pos.x = 距离滑动条.value
    
    电量标签1.text = f'电荷1电量: {电荷量1:.1e} C\n'
    电量标签2.text = f'电荷2电量: {电荷量2:.1e} C'
    距离标签.text = f'电荷2位置: {小球2.pos.x} m'
    绘图()

电量滑动条1 = slider(min=-10, max=10, value=-1, step=1, bind=更新电势图, pos=场景.title_anchor)
电量标签1 = wtext(text=f'', pos=场景.title_anchor)

电量滑动条2 = slider(min=-10, max=10, value=1, step=1, bind=更新电势图, pos=场景.title_anchor)
电量标签2 = wtext(text=f'', pos=场景.title_anchor)

距离滑动条 = slider(min=0, max=20, value=5, step=1, bind=更新电势图, pos=场景.title_anchor)
距离标签 = wtext(text=f'', pos=场景.title_anchor)

更新电势图()

while True:
    rate(10)