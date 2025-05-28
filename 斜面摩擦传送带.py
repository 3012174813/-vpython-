from vpython import *

scene = canvas(title='可调节角度传送带摩擦\n', width=1000, height=600, background=color.white)

传送带长度 = 10
传送带宽度 = 2
传送带速度 = 2
段长度 = 0.1  
时间步长 = 0.001
共速时间 = 0
传送带倾角 = 0.6454
传送带 = []  

传送带中端 = 0.5*vector(cos(传送带倾角)-sin(传送带倾角), sin(传送带倾角)+cos(传送带倾角), 0)
初始速度 = vector(5 * cos(传送带倾角), 5 * sin(传送带倾角), 0)
初始质量 = 1
初始摩擦系数 = 0.2
滑块 = box(pos=传送带中端, size=vector(1, 1, 1), color=color.blue, opacity=0.5, axis=vector(cos(传送带倾角), sin(传送带倾角), 0), 速度=初始速度, 质量=初始质量, 摩擦系数=初始摩擦系数)

速度箭头 = arrow(pos=滑块.pos, axis=滑块.速度*0.3, color=color.red)
速度标签 = label(pos=vector(-6, 1.5, 0), text=f'初速度大小: {mag(滑块.速度):.2f} m/s', box=False)
传送带速度标签 = label(pos=vector(-6, 2.5, 0), text=f'传送带速度: {传送带速度:.2f} m/s', box=False)
摩擦标签 = label(pos=vector(-6, 1, 0), text=f'摩擦系数: {滑块.摩擦系数:.2f}', box=False)
倾角标签 = label(pos=vector(-6, 0.5, 0), text=f'斜面倾角: {degrees(传送带倾角):.1f}°', box=False)
当前速度标签 = label(pos=vector(3, 2, 0), text='当前速度:', box=False)
当前加速度标签 = label(pos=vector(3, 1.5, 0), text='当前加速度: ', box=False)
共速时间标签 = label(pos=vector(3, 1, 0), text='共速时间: ', box=False)

def 创建传送带():
    global 传送带
    for 段 in 传送带:
        段.visible = False
    传送带.clear()

    for i in range(int(传送带长度/段长度)):
        x = -传送带长度/2 * cos(传送带倾角) + i*段长度 * cos(传送带倾角)
        y = -传送带长度/2 * sin(传送带倾角) + i*段长度 * sin(传送带倾角)
        段 = box(pos=vector(x, y, 0), size=vector(段长度, 0.02, 传送带宽度), 
                texture=textures.wood, axis=vector(cos(传送带倾角), sin(传送带倾角), 0))
        传送带.append(段)

def 更新倾角(s):
    global 传送带倾角, 传送带中端
    传送带倾角 = s.value
    倾角标签.text = f'斜面倾角: {degrees(传送带倾角):.1f}°'
    传送带中端 = 0.5*vector(cos(传送带倾角)-sin(传送带倾角), sin(传送带倾角)+cos(传送带倾角), 0)
    滑块.axis = vector(cos(传送带倾角), sin(传送带倾角), 0)
    创建传送带()
    重置模拟()
    
def 更新参数(滑动条, 参数类型):
    global 传送带速度
    if 参数类型 == "速度":
        速度标签.text = f'初速度大小: {滑动条.value:.2f} m/s'
    elif 参数类型 == "摩擦系数":
        滑块.摩擦系数 = 滑动条.value
        摩擦标签.text = f'摩擦系数: {滑块.摩擦系数:.2f}'
    elif 参数类型 == "传送带速度":
        传送带速度 = 滑动条.value
        传送带速度标签.text = f'传送带速度: {传送带速度:.2f} m/s'
    重置模拟()

def 重置模拟():
    global 共速时间
    滑块.pos = 传送带中端
    共速时间 = 0
    滑块.速度 = vector(速度滑动条.value * cos(传送带倾角), 速度滑动条.value * sin(传送带倾角), 0)
    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度*0.3

创建传送带()

倾角滑动条 = slider(min=-1.57, max=1.57, value=传送带倾角, bind=更新倾角, pos=scene.title_anchor, step=1.57/90)
scene.append_to_title(" 传送带倾角调节 ")

传送带速度滑动条 = slider(min=-5, max=5, value=传送带速度, bind=lambda s: 更新参数(s, "传送带速度"), pos=scene.title_anchor, step=0.1)
scene.append_to_title(" 传送带速度调节 \n")

速度滑动条 = slider(min=-5, max=5, value=mag(滑块.速度), bind=lambda s: 更新参数(s, "速度"), pos=scene.title_anchor, step=0.1)
scene.append_to_title(" 初速度大小 ")

摩擦滑动条 = slider(min=0, max=1, value=滑块.摩擦系数, bind=lambda s: 更新参数(s, "摩擦系数"), pos=scene.title_anchor, step=0.01)
scene.append_to_title(" 摩擦系数\n ")

def rk4积分(滑块, 传送带速度, 传送带倾角, 相对位置, 速度, dt):
    def 计算加速度(滑块, 传送带速度, 传送带倾角):
        g = 10 
        重力分量 = -滑块.质量 * g * sin(传送带倾角)  
        法向力 = 滑块.质量 * g * cos(传送带倾角)
        传送带方向 = vector(cos(传送带倾角), sin(传送带倾角), 0)
        滑块速度沿斜面 = dot(滑块.速度, 传送带方向)
        相对速度 = 滑块速度沿斜面 - 传送带速度
        
        if abs(相对速度) < 0.01: 
            最大静摩擦力 = 滑块.摩擦系数 * 法向力
            if abs(重力分量) <= 最大静摩擦力:
                摩擦力 = -重力分量  
            else:
                摩擦力 = -最大静摩擦力 if 重力分量 < 0 else 最大静摩擦力
        else:  
            摩擦力方向 = -sign(相对速度)
            摩擦力 = 摩擦力方向 * 滑块.摩擦系数 * 法向力
    
        加速度大小 = (重力分量 + 摩擦力) / 滑块.质量
        加速度向量 = vector(加速度大小 * cos(传送带倾角), 加速度大小 * sin(传送带倾角), 0)
        当前加速度标签.text = f'当前加速度: {加速度大小:.2f} m/s²'
        return 加速度向量
    
    k1v = 计算加速度(滑块, 传送带速度, 传送带倾角)
    k1x = 速度
 
    k2v = 计算加速度(滑块, 传送带速度, 传送带倾角)
    k2x = 速度 + k1v*dt/2

    k3v = 计算加速度(滑块, 传送带速度, 传送带倾角)
    k3x = 速度 + k2v*dt/2

    k4v = 计算加速度(滑块, 传送带速度, 传送带倾角)
    k4x = 速度 + k3v*dt

    新速度 = 速度 + (k1v + 2*k2v + 2*k3v + k4v)*dt/6
    新相对位置 = 相对位置 + (k1x + 2*k2x + 2*k3x + k4x)*dt/6
    
    return 新相对位置, 新速度

while True:
    rate(400)
        
    for 段 in 传送带:
        dx = 传送带速度 * 时间步长 * cos(传送带倾角)
        dy = 传送带速度 * 时间步长 * sin(传送带倾角)
        段.pos.x += dx
        段.pos.y += dy

        段位置 = (段.pos.x * cos(传送带倾角) + 段.pos.y * sin(传送带倾角))
        if (传送带速度 > 0 and 段位置 > 传送带长度/2) or (传送带速度 < 0 and 段位置 < -传送带长度/2):
            段.pos.x = (-传送带长度/2 if 传送带速度 > 0 else 传送带长度/2) * cos(传送带倾角) + dx
            段.pos.y = (-传送带长度/2 if 传送带速度 > 0 else 传送带长度/2) * sin(传送带倾角) + dy

    相对位置, 滑块.速度 = rk4积分(滑块, 传送带速度, 传送带倾角, 滑块.pos - 传送带中端, 滑块.速度, 时间步长)
    滑块.pos = 相对位置 + 传送带中端
    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度 * 0.3

    传送带方向 = vector(cos(传送带倾角), sin(传送带倾角), 0)
    滑块速度沿斜面 = dot(滑块.速度, 传送带方向)
    当前速度标签.text = f'当前速度: {滑块速度沿斜面:.2f} m/s'
    
    滑块位置沿传送带 = (相对位置.x * cos(传送带倾角)) + (相对位置.y * sin(传送带倾角))
    
    if abs(滑块位置沿传送带) > 传送带长度/2:
        滑块位置沿传送带 = -sign(滑块位置沿传送带) * 传送带长度/2
        相对位置.x = 滑块位置沿传送带 * cos(传送带倾角)
        相对位置.y = 滑块位置沿传送带 * sin(传送带倾角)
        滑块.pos = 相对位置 + 传送带中端

    if abs(滑块速度沿斜面 - 传送带速度) > 0.02:
        共速时间 += 时间步长
        共速时间标签.text = f'共速时间: {共速时间:.2f} s'