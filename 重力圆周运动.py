from vpython import *

场景 = canvas(title="小球在圆管内的圆周运动", width=800, height=800, background=color.white)

重力加速度 = 9.8  
圆管半径 = 5.0   
初始角度 = 0     
初始角速度 = 0   
时间步长 = 0.01  
当前时间 = 0     
小球质量 = 1.0   

外圆环 = ring(pos=vector(0, 0, 0), axis=vector(0, 0, 1), radius=圆管半径+0.2, thickness=0.05, color=color.blue, opacity=0.5)
内圆环 = ring(pos=vector(0, 0, 0), axis=vector(0, 0, 1), radius=圆管半径-0.2, thickness=0.05, color=color.blue, opacity=0.5)

小球 = sphere(pos=vector(圆管半径, 0, 0), radius=0.5, color=color.red, make_trail=True, retain=100, texture=textures.rough, opacity=0.5)

重力箭头 = arrow(pos=小球.pos, axis=vector(0, -重力加速度, 0), color=color.green, shaftwidth=0.1)
切向力箭头 = arrow(pos=小球.pos, axis=vector(0, 0, 0), color=color.blue, shaftwidth=0.1)
管壁压力箭头 = arrow(pos=小球.pos, axis=vector(0, 0, 0), color=color.red, shaftwidth=0.1)

高度标签 = label(pos=vector(-6, 5, 0), text="高度: 0.00 米", box=False)
速度标签 = label(pos=vector(-6, 4.5, 0), text="速度: 0.00 米/秒", box=False)
角度标签 = label(pos=vector(-6, 4, 0), text="运动方向与重力夹角: 0.00°", box=False)
切向力标签 = label(pos=vector(-6, 3.5, 0), text="切向力: 0.00 牛", box=False)
管壁压力标签 = label(pos=vector(-6, 3, 0), text="管壁支持力: 0.00 牛", box=False)
时间标签 = label(pos=vector(-6, 2.5, 0), text="模拟时间: 0.00 秒", box=False)

模拟运行中 = True

def 切换模拟状态(按钮):
    global 模拟运行中
    模拟运行中 = not 模拟运行中
    按钮.text = "继续模拟" if not 模拟运行中 else "暂停模拟"

控制按钮 = button(text="暂停模拟", pos=场景.title_anchor, bind=切换模拟状态)

def 设置角速度(滑块):
    global 初始角速度
    初始角速度 = 滑块.value
    
角速度滑块 = slider(min=0, max=5, value=0, step=0.1, length=300, bind=设置角速度, pos=场景.title_anchor, right=15)

def 重置到最高点():
    global 初始角度, 初始角速度, 当前时间
    初始角度 = pi/2  
    初始角速度 = 0
    当前时间 = 0
    小球.clear_trail()

def 重置到最低点():
    global 初始角度, 初始角速度, 当前时间
    初始角度 = 3*pi/2  
    初始角速度 = 0
    当前时间 = 0
    小球.clear_trail()

def 重置到初始位置():
    global 初始角度, 初始角速度, 当前时间
    初始角度 = 0  
    初始角速度 = 0
    当前时间 = 0
    小球.clear_trail()

最高点按钮 = button(text="重置到最高点", pos=场景.title_anchor, bind=重置到最高点)
最低点按钮 = button(text="重置到最低点", pos=场景.title_anchor, bind=重置到最低点)
初始位置按钮 = button(text="重置到初始位置", pos=场景.title_anchor, bind=重置到初始位置)

while True:
    rate(100)
    
    if not 模拟运行中:
        continue
    
    x坐标 = 圆管半径 * cos(初始角度)
    y坐标 = 圆管半径 * sin(初始角度)
    小球.pos = vector(x坐标, y坐标, 0)

    速度大小 = 初始角速度 * 圆管半径

    重力 = vector(0, -小球质量 * 重力加速度, 0)

    切向力大小 = -小球质量 * 重力加速度 * cos(初始角度)
    切向方向 = vector(-sin(初始角度), cos(初始角度), 0)
    切向力 = 切向力大小 * 切向方向

    向心力大小 = 小球质量 * 速度大小**2 / 圆管半径
    法向力大小 = 小球质量 * 重力加速度 * sin(初始角度) - 向心力大小
    法向方向 = vector(-cos(初始角度), -sin(初始角度), 0)
    管壁压力 = 法向力大小 * 法向方向

    切向加速度 = 切向力大小 / 小球质量
    初始角速度 += 切向加速度 / 圆管半径 * 时间步长

    初始角度 += 初始角速度 * 时间步长

    当前时间 += 时间步长

    重力箭头.pos = 小球.pos
    重力箭头.axis = 重力 /5
    
    切向力箭头.pos = 小球.pos
    切向力箭头.axis = 切向力 /5
    
    管壁压力箭头.pos = 小球.pos
    管壁压力箭头.axis = -管壁压力 /5

    运动方向 = vector(-sin(初始角度), cos(初始角度), 0)
    重力方向 = vector(0, -1, 0)
    夹角 = degrees(acos(运动方向.dot(重力方向)))

    高度标签.text = f"高度: {y坐标:.2f} 米"
    速度标签.text = f"速度: {速度大小:.2f} 米/秒"
    角度标签.text = f"运动方向与重力夹角: {夹角:.2f}°"
    切向力标签.text = f"切向力: {切向力大小:.2f} 牛"
    管壁压力标签.text = f"管壁支持力: {法向力大小:.2f} 牛"
    时间标签.text = f"模拟时间: {当前时间:.2f} 秒"