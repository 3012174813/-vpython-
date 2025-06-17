from vpython import *

场景 = canvas(title='示波器模拟\n', width=800, height=600, background=color.white)

电子电荷 = 1   
电子质量 = 1e-4   
时间步长 = 1e-4  

粒子列表 = []    
def 发射电子():
    粒子 = sphere(pos=vector(-6,0,0), radius=0.3, color=color.cyan, 速度=vector(1e4,0,0))
    粒子列表.append(粒子)

y电场箭头组 = []
z电场箭头组 = []

def 更新场():
    y电场标签.text = f"y方向电场强度: {y电场滑块.value} V/m\n"
    z电场标签.text = f"z方向电场强度: {z电场滑块.value} V/m\n"

    for i in y电场箭头组:
        i.visible = False
    y电场箭头组.clear()
    for i in z电场箭头组:
        i.visible = False
    z电场箭头组.clear()
    
    for x in range(-4, 0, 1):
        for y in range(-2, 2, 1):
            z电场箭头组.append(arrow(opacity=0.2, shaftwidth=abs(z电场滑块.value)/2000,
            pos=vector(x, y, -2) if z电场滑块.value > 0 else vector(x,y,2), 
            axis=vector(0,0,4) if z电场滑块.value > 0 else -vector(0,0,4)))

    for x in range(0, 4, 1):
        for z in range(-2, 2, 1):
            y电场箭头组.append(arrow( opacity=0.2,shaftwidth=abs(y电场滑块.value)/2000,color=color.red,
            pos=vector(x, -2, z) if y电场滑块.value > 0 else vector(x,2,z), 
            axis=vector(0,4,0) if y电场滑块.value > 0 else -vector(0,4,0)))

y电场滑块 = slider(min=-900, max=900, value=100, step=200, bind=更新场, pos=场景.title_anchor)
y电场标签 = wtext(text="\n", pos=场景.title_anchor)
z电场滑块 = slider(min=-900, max=900, value=100, step=200, bind=更新场, pos=场景.title_anchor)
z电场标签 = wtext(text="\n", pos=场景.title_anchor)
位移标签 = label(text="\n", pos=vector(10, 0, 0))

更新场()

上板 = box(pos=vector(-2, 0, 2), size=vector(4, 4, 0.2), color=color.gray(0.7))
下板 = box(pos=vector(-2, 0, -2), size=vector(4, 4, 0.2), color=color.gray(0.7))

前板 = box(pos=vector(2, 2, 0), size=vector(4, 0.2, 4), color=color.gray(0.7))
后板 = box(pos=vector(2, -2, 0), size=vector(4, 0.2, 4), color=color.gray(0.7))

接收屏 = box(pos=vector(10, 0, 0), size=vector(0.1, 10, 10), color=color.green, opacity=0.3)

def 加速度(pos):
    E = vector(0, 0, 0)
    if -5 < pos.x < 0:  
        E.z = z电场滑块.value
    elif 0 < pos.x < 5:          
        E.y = y电场滑块.value
    else:  
        E = vector(0, 0, 0)
    return (电子电荷 / 电子质量) * E

def RK4(粒子):
    r = 粒子.pos
    v = 粒子.速度
    
    k1v = 加速度(r)
    k1r = v
    
    k2v = 加速度(r + 0.5 * 时间步长 * k1r)
    k2r = v + 0.5 * 时间步长 * k1v

    k3v = 加速度(r + 0.5 * 时间步长 * k2r)
    k3r = v + 0.5 * 时间步长 * k2v

    k4v = 加速度(r + 时间步长 * k3r)
    k4r = v + 时间步长 * k3v

    粒子.pos = r + (时间步长/6.0) * (k1r + 2*k2r + 2*k3r + k4r)
    粒子.速度 = v + (时间步长/6.0) * (k1v + 2*k2v + 2*k3v + k4v)
    
    if 粒子.pos.x > 10:  
        粒子.速度 = vector(0, 0, 0)  

while True:
    rate(20) 
    发射电子()

    for 粒子 in 粒子列表:
        RK4(粒子)

    if len(粒子列表) > 20 :
        待删除粒子 = 粒子列表.pop(0)
        位移标签.text = f"位移y: {待删除粒子.pos.y:.2f} m, 位移z: {待删除粒子.pos.z:.2f} m"
        待删除粒子.visible = False
        待删除粒子.delete()