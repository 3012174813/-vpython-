from vpython import *

场景 = canvas(title='传送带滑块模拟\n', width=1000, height=600, background=color.white)

传送带长度 = 10
传送带宽度 = 2
传送带速度 = 2
段长度 = 0.1  

def 创建传送带():
    传送带段 = []
    for i in range(100):
        段 = box(pos=vector(-传送带长度/2 + i*段长度, 0, 0), size=vector(段长度, 0.02, 传送带宽度), texture=textures.wood)
        传送带段.append(段)
    return 传送带段

传送带 = 创建传送带()

初始位置 = vector(0, 0.5, 0)
初始速度 = vector(0, 0, 0)
相对位移 = 0
共速时间 = 0
初始质量 = 1
初始摩擦系数 = 0.2

滑块 = box(pos=初始位置, size=vector(0.5, 0.5, 0.5), color=color.blue, 速度=初始速度, 质量=初始质量, 摩擦系数=初始摩擦系数, opacity=0.5)

速度箭头 = arrow(pos=滑块.pos, axis=滑块.速度*0.3, color=color.red)
质量标签 = label(pos=vector(-4, 2, 0), text=f'质量: {滑块.质量:.2f} kg', box=False)
速度标签 = label(pos=vector(-4, 1.5, 0), text=f'滑块初速: {mag(滑块.速度):.2f} m/s', box=False)
摩擦标签 = label(pos=vector(-4, 1, 0), text=f'摩擦系数: {滑块.摩擦系数:.2f}', box=False)
当前速度标签 = label(pos=vector(4, 2, 0), text='当前速度', box=False)
相对位移标签 = label(pos=vector(4, 1.5, 0), text='相对位移', box=False)
传送带速度标签 = label(pos=vector(-4, 0.5, 0), text=f'传送带速度:{传送带速度:.2f} m/s', box=False)
共速时间标签 = label(pos=vector(4, 1, 0), text='共速时间', box=False)

def 更新参数(滑动条, 参数类型):
    global 传送带速度
    if 参数类型 == "质量":
        滑块.质量 = 滑动条.value
        质量标签.text = f'质量: {滑块.质量:.2f} kg'
    elif 参数类型 == "速度":
        滑块.速度.x = 滑动条.value
        速度标签.text = f'滑块初速: {滑动条.value:.2f} m/s'
    elif 参数类型 == "摩擦系数":
        滑块.摩擦系数 = 滑动条.value
        摩擦标签.text = f'摩擦系数: {滑块.摩擦系数:.2f}'
    elif 参数类型 == "传送带速度":
        传送带速度 = 滑动条.value
        传送带速度标签.text = f'传送带速度: {传送带速度:.2f} m/s'
    
    速度箭头.axis = 滑块.速度*0.3
    重置模拟()

def 重置模拟():
    global 相对位移, 共速时间
    滑块.pos = 初始位置
    滑块.速度 = vector(速度滑动条.value, 0, 0)
    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度*0.3
    当前速度标签.text = '当前速度'
    相对位移 = 0
    共速时间 = 0
    相对位移标签.text = '相对位移'
    共速时间标签.text = '共速时间'

传送带速度滑块 = slider(min=-10, max=10, value=传送带速度, bind=lambda s: 更新参数(s, "传送带速度"), pos=场景.title_anchor, step=0.1)
场景.append_to_title("传送带速度 ")

速度滑动条 = slider(min=-5, max=5, value=0, bind=lambda s: 更新参数(s, "速度"), pos=场景.title_anchor, step=0.1)
场景.append_to_title(" 滑块初速\n ")

质量滑动条 = slider(min=0.1, max=5, value=滑块.质量, bind=lambda s: 更新参数(s, "质量"), pos=场景.title_anchor, step=0.1)
场景.append_to_title("质量")

摩擦滑动条 = slider(min=0, max=1, value=滑块.摩擦系数, bind=lambda s: 更新参数(s, "摩擦系数"), pos=场景.title_anchor, step=0.01)
场景.append_to_title(" 摩擦系数\n")

重置按钮 = button(bind=重置模拟, text="重置位置")

def 计算加速度(速度):
    if abs(滑块.速度.x - 传送带速度) > 0.01:
        摩擦力方向 = 1 if 滑块.速度.x < 传送带速度 else -1
        摩擦力大小 = 滑块.摩擦系数 * 滑块.质量 * 10
        return vector(摩擦力方向 * 摩擦力大小 / 滑块.质量, 0, 0)
    return vector(0, 0, 0)  

def rk4积分(位置, 速度, dt):
    k1v = 计算加速度(速度)
    k1x = 速度
    
    k2v = 计算加速度(速度 + k1v*dt/2)
    k2x = 速度 + k1v*dt/2
    
    k3v = 计算加速度(速度 + k2v*dt/2)
    k3x = 速度 + k2v*dt/2
    
    k4v = 计算加速度(速度 + k3v*dt)
    k4x = 速度 + k3v*dt
    
    新速度 = 速度 + (k1v + 2*k2v + 2*k3v + k4v)*dt/6
    新位置 = 位置 + (k1x + 2*k2x + 2*k3x + k4x)*dt/6
    
    return 新位置, 新速度

时间步长 = 0.01
while True:
    rate(100) 

    for 段 in 传送带:
        段.pos.x += 传送带速度 * 时间步长
        if (传送带速度 > 0 and 段.pos.x > 传送带长度/2) or (传送带速度 < 0 and 段.pos.x < -传送带长度/2):
            段.pos.x = (-传送带长度/2 if 传送带速度 > 0 else 传送带长度/2) + 传送带速度 * 时间步长

    if abs(滑块.速度.x - 传送带速度) > 0.01:  
        滑块.pos, 滑块.速度 = rk4积分(滑块.pos, 滑块.速度, 时间步长)
        共速时间 += 时间步长
        共速时间标签.text = f'共速时间: {共速时间:.2f} s'
    else:
        滑块.速度.x = 传送带速度 
        滑块.pos.x += 传送带速度 * 时间步长  
        
    if abs(滑块.pos.x) > 传送带长度/2:
        滑块.pos.x = -传送带长度/2 if 滑块.pos.x > 0 else 传送带长度/2
        
    当前速度 = 滑块.速度.x
    相对位移 += (传送带速度-滑块.速度.x) * 时间步长
    当前速度标签.text = f'当前速度: {当前速度:.2f} m/s'
    相对位移标签.text = f'相对位移: {相对位移:.2f} m'
    
    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度 * 0.3