from vpython import *

场景 = canvas(title="滑块与摩擦力模拟", width=1000, height=400, background=color.white)

初始位置 = vector(-8, 0.5, 0)
初始速度 = vector(5, 0, 0)
初始质量 = 1
初始摩擦系数 = 0.2

地面 = box(pos=vector(0, -0.1, 0), size=vector(20, 0.1, 5), color=color.green)
滑块 = box(pos=初始位置, size=vector(1, 1, 1), color=color.blue, opacity=0.5, 速度=初始速度, 质量=初始质量, 摩擦系数=初始摩擦系数 ,make_trail=True)

速度箭头 = arrow(pos=滑块.pos, axis=滑块.速度*0.3, color=color.red)
质量标签 = label(pos=vector(-10, 2, 0), text=f'质量: {滑块.质量:.2f} kg', box=False)
速度标签 = label(pos=vector(-10, 1.5, 0), text=f'水平初速: {滑块.速度.x:.2f} m/s', box=False)
摩擦标签 = label(pos=vector(-10, 1, 0), text=f'摩擦系数: {滑块.摩擦系数:.2f}', box=False)
当前速度标签 = label(pos=vector(5, 2, 0), text='当前速度', box=False)
位移标签 = label(pos=vector(5, 1.5, 0), text='位移', box=False)

def 更新参数(滑动条, 参数类型):
    if 参数类型 == "质量":
        滑块.质量 = 滑动条.value
        质量标签.text = f'质量: {滑块.质量:.2f} kg'
    elif 参数类型 == "速度":
        滑块.速度.x = 滑动条.value
        速度标签.text = f'水平初速: {滑块.速度.x:.2f} m/s'
    elif 参数类型 == "摩擦系数":
        滑块.摩擦系数 = 滑动条.value
        摩擦标签.text = f'摩擦系数: {滑块.摩擦系数:.2f}'
    
    速度箭头.axis = 滑块.速度*0.3

def 重置模拟():
    滑块.pos = 初始位置
    滑块.速度 = vector(速度滑动条.value, 0, 0)
    滑块.质量 = 质量滑动条.value
    滑块.摩擦系数 = 摩擦滑动条.value
    滑块.clear_trail() 
    
    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度*0.3
    
    速度标签.text = f'水平初速: {滑块.速度.x:.2f} m/s'
    当前速度标签.text = '当前速度'
    位移标签.text = '位移'

def 计算加速度(位置, 速度):
   
    if mag(速度) > 0:
        摩擦力方向 = -norm(速度) 
        摩擦力大小 = 滑块.摩擦系数 * 滑块.质量 * 10
        return 摩擦力方向 * 摩擦力大小 / 滑块.质量
    return vector(0, 0, 0)  

def rk4积分(位置, 速度, dt):
   
    k1v = 计算加速度(位置, 速度)
    k1x = 速度
    
    k2v = 计算加速度(位置 + k1x*dt/2, 速度 + k1v*dt/2)
    k2x = 速度 + k1v*dt/2
    
    k3v = 计算加速度(位置 + k2x*dt/2, 速度 + k2v*dt/2)
    k3x = 速度 + k2v*dt/2
    
    k4v = 计算加速度(位置 + k3x*dt, 速度 + k3v*dt)
    k4x = 速度 + k3v*dt
    
    新速度 = 速度 + (k1v + 2*k2v + 2*k3v + k4v)*dt/6
    新位置 = 位置 + (k1x + 2*k2x + 2*k3x + k4x)*dt/6
    
    return 新位置, 新速度

质量滑动条 = slider(min=1, max=5, value=滑块.质量, bind=lambda s: 更新参数(s, "质量"), pos=场景.title_anchor, step=1)
场景.append_to_title("质量\n")

速度滑动条 = slider(min=0, max=10, value=滑块.速度.x, bind=lambda s: 更新参数(s, "速度"), pos=场景.title_anchor, step=0.1)
场景.append_to_title(" 速度 ")

摩擦滑动条 = slider(min=0, max=1, value=滑块.摩擦系数, bind=lambda s: 更新参数(s, "摩擦系数"), pos=场景.title_anchor, step=0.01)
场景.append_to_title(" 摩擦系数\n")

重置按钮 = button(bind=重置模拟, text="重置位置")

时间步长 = 0.01
while True:
    rate(100)
    
    if mag(滑块.速度) > 0.1:  
       滑块.pos, 滑块.速度 = rk4积分(滑块.pos, 滑块.速度, 时间步长)
    else:
        滑块.速度 = vector(0, 0, 0)
    
    当前速度 = mag(滑块.速度)
    位移 = mag(滑块.pos - 初始位置)
    当前速度标签.text = f'当前速度: {当前速度:.2f} m/s'
    位移标签.text = f'位移: {位移:.2f} m'
    
    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度 * 0.3