from vpython import *
import random

场景 = canvas(title="磁聚焦 \n", width=800, height=600, background=color.white)
场景.camera.pos = vector(-40, 0, 10)
场景.camera.axis = vector(10, 0, -5)

电荷量 = -1  
质量 = 1e-7      
初速度 = 1e7
磁场 = vector(0, 0, 0.3) 

磁场箭头 = []
粒子列表 = []

def 发射粒子():
    for _ in range(10):
        粒子 = sphere(pos=vector(0,0,-20), radius=0.3, color=color.blue)
        粒子.速度 = 初速度*vector(cos(random.uniform(0, pi)), sin(random.uniform(0, pi)), 0.5)
        粒子列表.append(粒子)

def 更新():
    global 磁场, 磁场箭头,电荷量,速度,球数
    
    磁场 = vector(0, 0, 磁场滑块.value )  
    磁场标签.text = f"磁场强度: {磁场.z:.1f} T\n"
    
    for i in 磁场箭头:
        i.visible = False
        i.delete()

    for x in range(-10, 10, 5):
        for y in range(-10, 10, 5):
            磁场箭头.append(arrow(pos=vector(x, y, -20), axis=磁场*100, opacity=0.4,shaftwidth=0.1))

磁场滑块 = slider(min=0.1, max=0.5, value=0.3, step=0.1, bind=更新, pos=场景.title_anchor)
磁场标签 = wtext(text="\n", pos=场景.title_anchor)

更新()

dt = 1e-7  
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
    rate(30)  
    发射粒子()

    for 粒子 in 粒子列表:
        粒子.pos, 粒子.速度 = rk4(粒子.pos, 粒子.速度, 磁场, 电荷量, 质量, dt)
        if 粒子.pos.mag > 30 :
            粒子.visible = False
            粒子列表.remove(粒子)
    
  