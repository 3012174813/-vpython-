from vpython import *

场景 = canvas(title = "滑块与摩擦力模拟\n",width=800, height=400, background=color.white)

地面 = box(pos=vector(0, -0.1, 0), size=vector(20, 0.1, 5), color=color.green)
滑块 = box(pos=vector(-8, 0.5, 0), size=vector(1, 1, 1), color=color.blue, make_trail=True,opacity=0.5,速度=vector(5, 0, 0), 质量=1, 摩擦系数=0.2)

速度箭头 = arrow(pos=滑块.pos, axis=滑块.速度*0.3, color=color.red)

def 设置质量(滑块值):
    滑块.质量 = 滑块值.value
slider(min=0.1, max=5, value=1, bind=设置质量,pos = 场景.title_anchor)
场景.append_to_title("质量 (千克)\n")

def 设置速度(滑块值):
    滑块.速度.x = 滑块值.value
slider(min=-10, max=10, value=5, bind=设置速度,pos = 场景.title_anchor)
场景.append_to_title("初速度 (米/秒)\n")

def 设置摩擦(滑块值):
    滑块.摩擦系数 = 滑块值.value
slider(min=0, max=1, value=0.2, bind=设置摩擦,pos = 场景.title_anchor)
场景.append_to_title("摩擦系数\n")

def 重置模拟():
    滑块.pos = vector(-8, 0.5, 0)
    滑块.clear_trail()
button(text="重置", bind=重置模拟)

时间 = 0
时间步长 = 0.01
while True:
    rate(100)
    
    if mag(滑块.速度) > 0:
        摩擦力 = -norm(滑块.速度) * 滑块.质量 * 9.8 * 滑块.摩擦系数
    else:
        摩擦力 = vector(0, 0, 0)

    加速度 = 摩擦力 / 滑块.质量
    滑块.速度 += 加速度 * 时间步长
    滑块.pos += 滑块.速度 * 时间步长

    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度 * 0.3
    
    时间 += 时间步长
