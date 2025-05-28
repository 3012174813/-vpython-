from vpython import *

场景 = canvas(title='小船过河', width=1000, height=600, background=color.white)

传送带速度 = 2

def 创建传送带():
    传送带段 = []
    for i in range(100):
        段 = box(pos=vector(-5 + i*0.1, 0, 0), size=vector(0.1, 0.02, 6), color=color.blue, opacity=0.5)
        传送带段.append(段)
    return 传送带段

传送带 = 创建传送带()

初始位置 = vector(0, 0, 3)
滑块 = box(pos=初始位置, size=vector(0.5, 0.5, 1), velocity=vector(0,0,0), color=color.red, 速度 = vector(0, 0, -3),opacity=0.5)
速度箭头 = arrow(pos=滑块.pos, axis=滑块.velocity*0.3, color=color.red)
速度标签 = label(pos=vector(-4, 1.5, 0), text='小船初速: -3 m/s', box=False)
当前速度标签 = label(pos=vector(4, 2, 0), text='当前速度: (2, -3) m/s', box=False)
传送带速度标签 = label(pos=vector(-4, 0.5, 0), text=f'传送带速度:{传送带速度:.2f} m/s', box=False)
到岸时间标签 = label(pos=vector(4, 1, 0), text='到岸时间: 0.00 s', box=False)

def 更新参数(滑动条, 参数类型):
    global 传送带速度
    if 参数类型 == "传送带速度":
        传送带速度 = 滑动条.value
        传送带速度标签.text = f'传送带速度: {传送带速度:.2f} m/s'
    elif 参数类型 == "角度":
        角度 = 滑动条.value
        新方向 = vector(cos(角度), 0, sin(角度))
        滑块.axis = 新方向 * 0.5
    
    v0 = 速度滑动条.value
    角度 = 角度滑动条.value
    vx = 传送带速度 + v0 * sin(角度)
    vz = v0 * -cos(角度)
    滑块.速度 = vector(vx, 0, vz)
    
    速度箭头.axis = 滑块.速度 * 0.3
    速度标签.text = f'小船初速: {v0:.2f} m/s'
    当前速度标签.text = f'当前速度: ({vx:.2f}, {vz:.2f}) m/s'
  
传送带速度滑块 = slider(min=0, max=5, value=传送带速度, bind=lambda s: 更新参数(s, "传送带速度"), step=0.1, pos=场景.title_anchor)
场景.append_to_title("传送带速度 ")

速度滑动条 = slider(min=0, max=6, value=3, bind=lambda s: 更新参数(s, "速度"), step=0.1, pos=场景.title_anchor)
场景.append_to_title(" 小船初速 \n")

角度滑动条 = slider(min=-1.57, max=1.57, value=0, bind=lambda s: 更新参数(s, "角度"), step=1.57/90, pos=场景.title_anchor)
场景.append_to_title(" 航行角度 ")

时间步长 = 0.01
时间 = 0
while True:
    rate(100)

    for 段 in 传送带:
        段.pos.x += 传送带速度 * 时间步长
        if 段.pos.x > 5:
            段.pos.x -= 10

    滑块.pos += 滑块.速度 * 时间步长
    速度箭头.pos = 滑块.pos
    if 滑块.pos.z > -3:
        时间 += 时间步长
        到岸时间标签.text = f'到岸时间: {时间:.2f} s'

    if 滑块.pos.mag >= 10:
        滑块.pos = 初始位置
        速度箭头.pos = 滑块.pos
        时间 = 0