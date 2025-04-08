from vpython import *
from math import *

场景 = canvas(title='小球平抛运动', width=800, height=600, background=color.white)
小球 = sphere(pos=vector(0, 19.6, 0), radius=1, color=color.blue, make_trail=True)  
地面 = box(pos=vector(0, -1, 0), size=vector(50, 0.1, 20), color=color.green) 

斜面 = None
斜面角度 = 30  
时间 = 0
g = 9.8  
dt = 0.001
初始高度 = 19.6
初始水平速度 = 5  
高度 = 初始高度
水平位置 = 0
垂直速度 = 0    

水平速度箭头 = arrow(pos=小球.pos, axis=vector(初始水平速度, 0, 0), color=color.red, shaftwidth=0.2)
竖直速度箭头 = arrow(pos=小球.pos, axis=vector(0, 0, 0), color=color.green, shaftwidth=0.2)
合速度箭头 = arrow(pos=小球.pos, axis=vector(初始水平速度, 0, 0), color=color.orange, shaftwidth=0.3)

def 更新速度箭头():
    水平速度箭头.pos = 小球.pos
    水平速度箭头.axis = vector(初始水平速度, 0, 0)
    
    竖直速度箭头.pos = 小球.pos
    竖直速度箭头.axis = vector(0, 垂直速度, 0)
    
    合速度箭头.pos = 小球.pos
    合速度箭头.axis = vector(初始水平速度, 垂直速度, 0)

def 更新参数(s,调整类型):
    global 高度, 垂直速度, 时间, 初始高度, 水平位置, 初始水平速度, 斜面角度
    
    if 调整类型 == "高度":
        初始高度 = s.value
    elif 调整类型 == "速度":
        初始水平速度 = s.value
    elif 调整类型 == "角度":
        斜面角度 = s.value
    
    高度 = 初始高度
    水平位置 = 0  
    小球.pos = vector(水平位置, 高度, 0)
    小球.clear_trail() 
    垂直速度 = 0
    时间 = 0

    初始高度标签.text = f'初始高度: {初始高度:.2f} m'
    初始速度标签.text = f'水平初速: {初始水平速度:.2f} m/s'
    
    更新速度箭头()
    更新斜面(斜面角度)

def 更新斜面(角度):
    global 斜面, 斜面角度
    斜面角度 = 角度
    斜面标签.text = f'斜面角度: {斜面角度}°'

    斜面长度 = 初始高度 / sin(斜面角度 * pi/180)
    斜面终点x = 水平位置 + 斜面长度 * cos(斜面角度 * pi/180)
   
    if 斜面 is not None:
        斜面.visible = False

    斜面 = box(pos=vector((水平位置 + 斜面终点x)/2, 初始高度/2, 0), 
size=vector(斜面长度, 0.1, 20),  axis=vector(cos(斜面角度 * pi/180), -sin(斜面角度 * pi/180), 0), color=color.orange, opacity=0.5)

高度滑块 = slider(min=0, max=50, value=初始高度, length=200, bind=lambda s: 更新参数(s, "高度"), pos=场景.title_anchor,step=1)
速度滑块 = slider(min=0, max=20, value=初始水平速度, length=200, bind=lambda s: 更新参数(s,"速度"), pos=场景.title_anchor,step=1)
斜面滑块 = slider(min=0, max=90, value=斜面角度, length=200, bind=lambda s: 更新参数(s,"角度"), pos=场景.title_anchor,step=5)

初始高度标签 = label(pos=vector(-15, 12, 0), text=f'初始高度: {初始高度:.2f} m', box=False)
初始速度标签 = label(pos=vector(-15, 10, 0), text=f'水平初速: {初始水平速度:.2f} m/s', box=False)
高度标签 = label(pos=vector(-15, 8, 0), text='高度:', box=False)
速度标签 = label(pos=vector(-15, 6, 0), text='速度: ', box=False)
时间标签 = label(pos=vector(-15, 4, 0), text='时间:', box=False)
水平位置标签 = label(pos=vector(-15, 2, 0), text='水平距离:', box=False)
斜面标签 = label(pos=vector(-15, 0, 0), text=f'斜面角度: {斜面角度}°', box=False)

更新斜面(斜面角度)

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
    rate(500)
    if 高度 > 0:
        高度, 垂直速度 = RK4(高度, 垂直速度, dt, g)
        水平位置 += 初始水平速度 * dt  
        小球.pos = vector(水平位置, 高度, 0)
        时间 += dt

        合速度 = (初始水平速度**2 + 垂直速度**2)**0.5

        当前角度 = atan((初始高度-高度+0.001)/(水平位置+0.001)) * 180/pi
        当前速度角度 = atan(-垂直速度/(初始水平速度+0.001)) * 180/pi
        if abs(当前角度 - 斜面角度) < 0.1 :
            sphere(pos=小球.pos, radius=0.5, color=color.red)
        if abs(当前速度角度 - 斜面角度) < 0.1 :
            sphere(pos=小球.pos, radius=0.5, color=color.green)
        
        时间标签.text = f'时间: {时间:.2f} s'   
        高度标签.text = f'高度: {高度:.2f} m'
        速度标签.text = f'速度: {合速度:.2f} m/s (水平速度:{初始水平速度:.2f}, 竖直速度:{垂直速度:.2f})'
        水平位置标签.text = f'水平距离: {水平位置:.2f} m'
        
        更新速度箭头()