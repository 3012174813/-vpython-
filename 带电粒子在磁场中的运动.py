from vpython import *

场景 = canvas(title="带电粒子在磁场中的运动 \n", width=800, height=600, background=color.white)

粒子 = sphere(pos=vector(0,0,0), radius=1, color=color.cyan, make_trail=True, retain = 100)

电荷量 = -1  
质量 = 1e-7      
速度 = vector(1e7, 0, 0)  
磁场 = vector(0, 0, 0.1) 

磁场箭头 = []

def 更新():
    global 磁场, 磁场箭头,电荷量,速度
    速度 = vector(速度滑块.value * 1e7, 0, 0)  
    电荷量 = 电荷滑块.value 
    磁场 = vector(0, 0, 磁场滑块.value )  
    电荷标签.text = f"电荷量: {电荷量:.1f} C\n"
    速度标签.text = f"速度: {速度.x:.1e} m/s\n"
    磁场标签.text = f"磁场强度: {磁场.z:.1f} T\n"
    粒子.pos =vector(0,0,0)
    运动半径 = 质量 * 速度.mag / (电荷量 * 磁场.mag)
    半径标签.text = f"运动半径: {运动半径:.2f} m  "
    周期 = 2 * pi * 运动半径 / 速度.mag
    周期标签.text = f"周期: {周期:.1e} s"
    for i in 磁场箭头:
        i.visible = False
        i.delete()

    for x in range(-20, 20, 2):
        for y in range(-20, 20, 2):
            磁场箭头.append(arrow(pos=vector(x, y, 0), axis=磁场*20, opacity=1,shaftwidth=0.1))

电荷滑块 = slider(min=-5, max=5, value=-1, step=0.1, bind=更新, pos=场景.title_anchor)
电荷标签 = wtext(text="\n", pos=场景.title_anchor)
速度滑块 = slider(min=-2, max=2, value=1, step=0.1, bind=更新, pos=场景.title_anchor)
速度标签 = wtext(text="\n", pos=场景.title_anchor)
磁场滑块 = slider(min=-0.5, max=0.5, value=0.1, step=0.1, bind=更新, pos=场景.title_anchor)
磁场标签 = wtext(text="\n", pos=场景.title_anchor)
半径标签 = wtext(text="\n", pos=场景.title_anchor)
周期标签 = wtext(text="\n", pos=场景.title_anchor)
位置标签 = label(pos=vector(0, 0, 0), text="",  box=False)

更新()

dt = 1e-8  

def rk4(pos, 速度, B, q, m, dt):
    def 计算(速度):
        洛伦兹力 = q * cross(速度, B)
        return 洛伦兹力 / m
    
    k1v = 计算(速度) * dt
    k1r = 速度 * dt
    
    k2v = 计算(速度 + 0.5*k1v) * dt
    k2r = (速度 + 0.5*k1v) * dt
    
    k3v = 计算(速度 + 0.5*k2v) * dt
    k3r = (速度 + 0.5*k2v) * dt
    
    k4v = 计算(速度 + k3v) * dt
    k4r = (速度 + k3v) * dt
    
    新速度 = 速度 + (k1v + 2*k2v + 2*k3v + k4v) / 6
    新位置 = pos + (k1r + 2*k2r + 2*k3r + k4r) / 6
    
    return 新位置, 新速度

while True:
    rate(100)  
    
    粒子.pos, 速度 = rk4(粒子.pos, 速度, 磁场, 电荷量, 质量, dt)
    位置标签.text = (f"粒子位置: {粒子.pos.x:.1f}, {粒子.pos.y:.1f}, {粒子.pos.z:.1f}\n")
    
  