from vpython import *

场景 = canvas(title='电子排布', width=800, height=600, background=color.white)
原子核 = sphere(pos=vector(0,0,0), radius=1, color=color.yellow)

时间步长 = 0.02
当前半径 = 2
轨道列表 = []

for i in range(6):
    轨道 = ring(pos=vector(0,0,0), axis=vector(0,0,1), radius=当前半径, thickness=0.1, opacity=0.2)
    轨道列表.append(轨道)
    当前半径 += 1

电子列表 = []

def 分配电子(原子序数):
    global 电子列表

    for 电子 in 电子列表:
        电子.visible = False
    电子列表 = []

    填充顺序 = [
        (0, 2),   # 1s
        (1, 2),   # 2s
        (1, 6),   # 2p
        (2, 2),   # 3s
        (2, 6),   # 3p
        (3, 2),   # 4s
        (2, 10),  # 3d
        (3, 6),   # 4p
        (4, 2),   # 5s
        (3, 10),  # 4d
        (4, 6),   # 5p
        (5, 2),   # 6s
        (4, 10),  # 5d
        (5, 6),   # 6p
    ]
    
    剩余电子数 = int(原子序数)  
    电子配置 = [0] * 6 
    
    for 层, 容量 in 填充顺序:
        if 剩余电子数 <= 0:
            break
        添加电子数 = min(容量, 剩余电子数)
        电子配置[层] += 添加电子数
        剩余电子数 -= 添加电子数

    for 层, 电子数 in enumerate(电子配置):
        if 电子数 == 0:
            continue
        for i in range(电子数):
            角度 = 2 * pi * i / 电子数
            位置 = vector(轨道列表[层].radius * cos(角度), 轨道列表[层].radius * sin(角度), 0)
            电子 = sphere(pos=位置, radius=0.3, color=color.blue)
            电子列表.append(电子)

def 更新电子数(电子数滑块):
    分配电子(电子数滑块.value)
    电子数标签.text = f'原子序数: {电子数滑块.value}'

电子数滑块 = slider(min=1, max=70, value=1, step=1, bind=更新电子数,pos=场景.title_anchor )
电子数标签 = label(text='原子序数: ', pos=vector(0, 0, 0), box=False)


while True:
    rate(100)
