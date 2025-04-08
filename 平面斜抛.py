from vpython import *
from math import *

场景 = canvas(title='小球斜抛运动', width=800, height=600, background=color.white)
小球 = sphere(pos=vector(0, 0, 0), radius=1, color=color.blue, make_trail=True)  
地面 = box(pos=vector(0, -1, 0), size=vector(50, 0.1, 20), color=color.green) 

时间 = 0
g = 9.8  
dt = 0.01
初始高度 = 0
初始速度 = 15  
初始角度 = 45  

角度 = radians(初始角度)
水平速度 = 初始速度 * cos(角度)
垂直速度 = 初始速度 * sin(角度)
高度 = 初始高度
水平位置 = 0

水平速度箭头 = arrow(pos=小球.pos, axis=vector(水平速度, 0, 0), color=color.red, shaftwidth=0.2)
竖直速度箭头 = arrow(pos=小球.pos, axis=vector(0, 垂直速度, 0), color=color.green, shaftwidth=0.2)
合速度箭头 = arrow(pos=小球.pos, axis=vector(水平速度, 垂直速度, 0), color=color.orange, shaftwidth=0.3)

def 暂停():
    global 暂停
    if not 暂停:
        暂停按钮.text = '运行'
        暂停 = True
    else:
        暂停按钮.text = '暂停'
        暂停 = False
暂停按钮 = button(text='运行', pos=场景.title_anchor, bind=暂停)

def 更新标签():
    初始高度标签.text = f'初始高度: {初始高度:.2f} m'
    初始速度标签.text = f'初始速度: {初始速度:.2f} m/s'
    初始角度标签.text = f'抛射角度: {初始角度:.2f}°'
    合速度 = (水平速度**2 + 垂直速度**2)**0.5
    时间标签.text = f'时间: {时间:.2f} s'   
    高度标签.text = f'高度: {高度:.2f} m'
    速度标签.text = f'速度: {合速度:.2f} m/s (水平:{水平速度:.2f}, 竖直:{垂直速度:.2f})'
    水平位置标签.text = f'水平距离: {水平位置:.2f} m'
    

def 更新速度箭头():
    水平速度箭头.pos = 小球.pos
    水平速度箭头.axis = vector(水平速度, 0, 0)
    竖直速度箭头.pos = 小球.pos
    竖直速度箭头.axis = vector(0, 垂直速度, 0)
    合速度箭头.pos = 小球.pos
    合速度箭头.axis = vector(水平速度, 垂直速度, 0)

def 参数调整(s, 调整类型=None):
    global 高度, 垂直速度, 时间, 初始高度, 水平位置, 水平速度, 初始速度, 初始角度, 角度
    
    if 调整类型 == "高度":
        初始高度 = s.value
    elif 调整类型 == "速度":
        初始速度 = s.value
    elif 调整类型 == "角度":
        初始角度 = s.value
        角度 = radians(初始角度)

    水平速度 = 初始速度 * cos(角度)
    垂直速度 = 初始速度 * sin(角度)
    
    高度 = 初始高度
    水平位置 = 0  
    小球.pos = vector(水平位置, 高度, 0)
    小球.clear_trail() 
 
    时间 = 0
    更新速度箭头()
    更新标签()

高度滑块 = slider(min=0, max=20, value=初始高度, length=300, bind=lambda s: 参数调整(s, "高度"), pos=场景.title_anchor)
速度滑块 = slider(min=0, max=30, value=初始速度, length=300, bind=lambda s: 参数调整(s, "速度"), pos=场景.title_anchor)
角度滑块 = slider(min=0, max=90, value=初始角度, length=300, bind=lambda s: 参数调整(s, "角度"), pos=场景.title_anchor)

初始高度标签 = label(pos=vector(-15, 14, 0), text=f'初始高度: {初始高度:.2f} m', box=False)
初始速度标签 = label(pos=vector(-15, 12, 0), text=f'初始速度: {初始速度:.2f} m/s', box=False)
初始角度标签 = label(pos=vector(-15, 10, 0), text=f'抛射角度: {初始角度:.2f}°', box=False)
最高高度标签 = label(pos=vector(-15, 8, 0), text='最高高度: ', box=False)
最远距离标签 = label(pos=vector(-15, 6, 0), text='最远距离: ', box=False)
高度标签 = label(pos=vector(-15, 4, 0), text='高度:', box=False)
速度标签 = label(pos=vector(-15, 2, 0), text='速度: ', box=False)
时间标签 = label(pos=vector(-15, 0, 0), text='时间:', box=False)
水平位置标签 = label(pos=vector(-15, -2, 0), text='水平距离:', box=False)

def RK4(y, v, dt, g):
    k1v = -g * dt  
    k1y = v * dt
    
    k2v = -g * dt
    k2y = (v + k1v/2) * dt
    
    k3v = -g * dt
    k3y = (v + k2v/2) * dt
    
    k4v = -g * dt
    k4y = (v + k3v) * dt

    new_v = v + (k1v + 2*k2v + 2*k3v + k4v)/6
    new_y = y + (k1y + 2*k2y + 2*k3y + k4y)/6
    
    return new_y, new_v


while True:
    rate(100)
    if not  暂停 and 高度 >= 0:
        高度, 垂直速度 = RK4(高度, 垂直速度, dt, g)
        水平位置 += 水平速度 * dt  
        小球.pos = vector(水平位置, 高度, 0)
        时间 += dt

        if abs(垂直速度) <= 0.1:
            最高高度标签.text = f'最高高度: {高度:.2f} m'
            最高点 = sphere(pos=小球.pos, radius=0.5, color=color.red)
        if abs(高度 - 初始高度) < 0.1 :
            最远距离标签.text = f'最远距离: {水平位置:.2f} m'
            最远点 = sphere(pos=小球.pos, radius=0.5, color=color.green)
        合速度 = (水平速度**2 + 垂直速度**2)**0.5
  
        更新速度箭头()
        更新标签()