from vpython import *
import numpy as np

场景 = canvas(title="等时圆模型", width=800, height=800, background=color.white)
圆半径 = 5
时间 = 0
dt = 0.01 
g = 10  

绿球角度 = np.pi/2
红球角度 = 3*np.pi/2

def 极坐标(角度):
    return vector(圆半径 * np.cos(角度), 圆半径 * np.sin(角度), 0)

圆环 = ring(pos=vector(0,0,0), axis=vector(0,0,1), radius=圆半径, thickness=0.05, color=color.blue)
红球 = sphere(pos=极坐标(红球角度), radius=0.1, color=color.red)
绿球 = sphere(pos=极坐标(绿球角度), radius=0.1, color=color.green)
连线 = curve(pos=[绿球.pos, 红球.pos], radius=0.02, color=color.yellow)
小球 = sphere(pos=绿球.pos, radius=0.08, color=color.orange)

红球标签 = label(pos=vector(0,0,0), box=False)
绿球标签 = label(pos=vector(0,0.5,0), box=False)
连线标签 = label(pos=vector(0,1,0), box=False)
时间标签 = label(pos=vector(0,1.5,0), box=False)
长度标签 = label(pos=vector(0,2.0,0), box=False)  
加速度标签 = label(pos=vector(0,2.5,0), box=False)

运动状态 = {"位置": vector(绿球.pos), "速度": vector(0,0,0)}
运动中 = False

def 斜面角度():
    斜面 = 红球.pos - 绿球.pos
    return np.degrees(np.arctan2(斜面.y, 斜面.x)) % 180, norm(斜面)

def 更新显示():
    红球.pos = 极坐标(红球角度)
    绿球.pos = 极坐标(绿球角度)

    连线.clear()
    连线.append(绿球.pos)
    连线.append(红球.pos)

    连线角度, _ = 斜面角度()
    斜面长度 = mag(红球.pos - 绿球.pos)
    斜面加速度 = g * np.sin(np.radians(连线角度))
    
    红球标签.text = f"红球角度: {np.degrees(红球角度):.1f}°"
    绿球标签.text = f"绿球角度: {np.degrees(绿球角度):.1f}°"
    连线标签.text = f"连线角度: {连线角度:.1f}°"
    时间标签.text = f"时间: {时间:.2f} s"
    长度标签.text = f"斜面长度: {斜面长度:.2f} m"  # 显示斜面长度
    加速度标签.text = f"斜面加速度: {斜面加速度:.2f} m/s²"

    if not 运动中:
        小球.pos = 绿球.pos

def 调整角度(调整类型):
    global 红球角度, 绿球角度
    if 调整类型 == "红球":
        红球角度 = 红球滑块.value
    elif 调整类型 == "绿球":
        绿球角度 = 绿球滑块.value
    更新显示()

def 开始运动():
    global 运动中, 运动状态, 时间
    运动中 = True
    运动状态 = {"位置": vector(绿球.pos), "速度": vector(0,0,0)}
    小球.pos = 绿球.pos
    小球.clear_trail()
    时间 = 0  

红球滑块 = slider(min=0, max=2*np.pi, value=红球角度, step=np.pi/36, bind=lambda: 调整角度("红球"), pos=场景.title_anchor)
绿球滑块 = slider(min=0, max=2*np.pi, value=绿球角度, step=np.pi/36, bind=lambda: 调整角度("绿球"), pos=场景.title_anchor)
开始 = button(bind=开始运动, text="开始运动", pos=场景.title_anchor)

while True:
    rate(100)

    if 运动中:
        时间 += dt
        加速度 = g * np.sin(np.radians(斜面角度()[0])) * 斜面角度()[1]

        运动状态["速度"] += 加速度 * dt
        运动状态["位置"] += 运动状态["速度"] * dt
        小球.pos = 运动状态["位置"]
        
        if mag(运动状态["位置"] - 绿球.pos) >= mag(红球.pos - 绿球.pos):
            运动中 = False
            小球.pos = 红球.pos
    
    更新显示() 