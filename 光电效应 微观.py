from vpython import *
import random

场景 = canvas(title='光电效应 微观', width=1000, height=700, background=color.white)
原子核 = sphere(pos=vector(0,0,0), radius=1, color=color.yellow)

轨道列表 = []
电子列表 = []
光子列表 = []
结合能标签列表 = []
当前半径 = 2
for i in range(6):
    轨道 = ring(pos=vector(0,0,0), axis=vector(0,0,1), radius=当前半径, thickness=0.1, opacity=0.2)
    轨道列表.append(轨道)
    当前半径 += 2

def 更新显示(原子序数):
    global 电子列表, 结合能标签列表

    for 电子 in 电子列表:
        电子.visible = False
    for 标签 in 结合能标签列表:
        标签.visible = False
    
    电子列表 = []
    结合能标签列表 = []

    电子排布, 结合能数据 = 计算结合能(原子序数)

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

    电子索引 = 0
    for 层, 电子数 in enumerate(电子配置):
        if 电子数 == 0:
            continue
        for i in range(电子数):
            角度 = 2 * pi * i / 电子数
            位置 = vector(轨道列表[层].radius * cos(角度), 
                       轨道列表[层].radius * sin(角度), 0)
            电子 = sphere(pos=位置, radius=0.3, 结合能 = 结合能数据[电子索引],速度=vector(0,0,0),color=color.blue)
            结合能标签 = label(pos=电子.pos+vector(0,-1,0), text=f" {电子.结合能:.2f}", box=False)
            结合能标签列表.append(结合能标签)
            电子列表.append(电子)
            电子索引 += 1

def 计算结合能(原子序数):
    轨道列表 = [(n, l) for n in range(1, 8) for l in range(n)]
    轨道列表.sort(key=lambda x: (x[0] + x[1], x[0]))
    
    电子排布 = {}
    已填充电子数 = 0
    for 轨道 in 轨道列表:
        最大容量 = 2 * (2 * 轨道[1] + 1)
        可填充数 = min(最大容量, 原子序数 - 已填充电子数)
        if 可填充数 <= 0:
            break
        电子排布[轨道] = 可填充数
        已填充电子数 += 可填充数

    分组字典 = {}
    for (主量子数, 角量子数), 电子数 in 电子排布.items():
        组标识 = (主量子数, 'sp' if 角量子数 in [0, 1] else 角量子数)
        分组字典[组标识] = 分组字典.get(组标识, 0) + 电子数

    已排序组 = sorted(分组字典.keys(), key=lambda x: x[0])

    结合能列表 = []
    for 组 in 已排序组:
        电子数 = 分组字典[组]
        主量子数, _ = 组
        组索引 = 已排序组.index(组)
        内层电子数 = sum(分组字典[组] for 组 in 已排序组[:组索引])
        同组屏蔽 = (电子数 - 1) * (0.30 if 组 == (1, 'sp') else 0.35)
        屏蔽数 = 内层电子数 + 同组屏蔽
        结合能 = -13.6 * ((原子序数 - 屏蔽数) ** 2) / (主量子数 ** 2)
        结合能列表.extend([结合能] * 电子数)
    
    return 电子排布, 结合能列表


电子数滑块 = slider(min=1, max=70, value=1, step=1, length=300, bind=lambda: 更新显示(电子数滑块.value),pos=场景.title_anchor)

光子能量滑块 = slider(min=1, max=500, value=4,step = 5,bind=lambda: 更新参数(),pos=场景.title_anchor )

def 更新参数():
    global 光子能量
    光子能量 = 光子能量滑块.value
    能量标签 = label(pos=vector(0,15,0), text=f'能量: {光子能量}ev',box=False)
  

更新参数()
def 发射光子():
    光子能量 = 光子能量滑块.value
    for _ in range(20):
        
        初始位置 = vector(random.uniform(-15, 15), random.uniform(-15, 15), 5)
        
        光子 = sphere(pos=初始位置, radius=0.2, color=color.green,能量=光子能量)
        光子.速度 = vector(0, 0, -0.1)
        光子列表.append(光子)

def 碰撞检测与处理():
    for 光子 in 光子列表[:]:
        for 电子 in 电子列表:
            if (光子.pos - 电子.pos).mag < 1:
               if 光子.能量 >= abs(电子.结合能):
                    电子.速度 = vector(0.2, 0, 0)  
                    光子.visible = False
                    光子列表.remove(光子)
                    break

while True:
    rate(100)
    if random.random() < 0.1: 
        发射光子()
    for 光子 in 光子列表[:]:
        光子.pos += 光子.速度

        if 光子.pos.z <= -1 :
            光子.visible = False
            光子列表.remove(光子)
            
    碰撞检测与处理()
    for 电子 in 电子列表:
        电子.pos += 电子.速度

        if 电子.pos.x >= 20 :
            电子.visible = False
            电子列表.remove(电子) 
            更新显示(电子数滑块.value)       
