from vpython import *

场景 = canvas(title="斜面有摩擦滑块", width=800, height=600, background=color.white)

斜面 = None
斜面倾角 = 0.5236  
斜面长度 = 10
斜面左端 = 0.5*vector(-斜面长度*cos(斜面倾角)+cos(斜面倾角)-sin(斜面倾角), -斜面长度 *sin(斜面倾角)+sin(斜面倾角)+cos(斜面倾角), 0)
初始位置 = vector(0,0, 0)
初始速度 = vector(5 * cos(斜面倾角), 5 * sin(斜面倾角), 0)
初始质量 = 1
初始摩擦系数 = 0.2
时间步长 = 0.01

斜面 = box(pos=vector(0, 0, 0), size=vector(斜面长度, 0.1, 2), color=color.green, axis=vector(cos(斜面倾角), sin(斜面倾角), 0))
滑块 = box(pos=斜面左端, size=vector(1, 1, 1), color=color.blue, opacity=0.5, axis=斜面.axis, 速度=初始速度, 质量=初始质量, 摩擦系数=初始摩擦系数, make_trail=True)

速度箭头 = arrow(pos=滑块.pos, axis=滑块.速度*0.3, color=color.red)
质量标签 = label(pos=vector(-6, 2, 0), text=f'质量: {滑块.质量:.2f} kg', box=False)
速度标签 = label(pos=vector(-6, 1.5, 0), text=f'初速度大小: {mag(滑块.速度):.2f} m/s', box=False)
摩擦标签 = label(pos=vector(-6, 1, 0), text=f'摩擦系数: {滑块.摩擦系数:.2f}', box=False)
倾角标签 = label(pos=vector(-6, 0.5, 0), text=f'斜面倾角: {degrees(斜面倾角):.1f}°', box=False)
当前速度标签 = label(pos=vector(3, 2, 0), text='当前速度:', box=False)
当前加速度标签 = label(pos=vector(3, 1.5, 0), text='当前加速度:', box=False)
位移标签 = label(pos=vector(3, 1, 0), text='位移: ', box=False)
最远位移标签 = label(pos=vector(3, 0.5, 0), text='最远位移: ', box=False)

模拟运行中 = True


def 更新倾角(新倾角):
    global 斜面倾角, 斜面左端, 模拟运行中,斜面
    
    斜面倾角 = 新倾角
    斜面.axis = vector(cos(斜面倾角), sin(斜面倾角), 0)
    滑块.axis = 斜面.axis
    斜面左端 = 0.5*vector(-斜面长度*cos(斜面倾角)+cos(斜面倾角)-sin(斜面倾角),  -斜面长度*sin(斜面倾角)+sin(斜面倾角)+cos(斜面倾角), 0)
    倾角标签.text = f'斜面倾角: {degrees(斜面倾角):.1f}°'

    if 斜面 is not None:
        斜面.visible = False
        del 斜面

    斜面 = box(pos=vector(0, 0, 0), size=vector(斜面长度, 0.1, 2), color=color.green, axis=vector(cos(斜面倾角), sin(斜面倾角), 0))
    重置模拟()


def 更新参数(滑动条, 参数类型):
    global 模拟运行中
    
    if 参数类型 == "质量":
        滑块.质量 = 滑动条.value
        质量标签.text = f'质量: {滑块.质量:.2f} kg'
    elif 参数类型 == "速度":
        速度大小 = 滑动条.value
        速度标签.text = f'初速度大小: {速度大小:.2f} m/s'
    elif 参数类型 == "摩擦系数":
        滑块.摩擦系数 = 滑动条.value
        摩擦标签.text = f'摩擦系数: {滑块.摩擦系数:.2f}'

    重置模拟()


def 重置模拟():
    global 模拟运行中
    滑块.pos = 斜面左端
    滑块.clear_trail() 
    速度大小 = 速度滑动条.value  
    
    滑块.速度 = vector(速度大小 * cos(斜面倾角), 速度大小 * sin(斜面倾角), 0)
    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度*0.3
    模拟运行中 = True


质量滑动条 = slider(min=1, max=5, value=滑块.质量, bind=lambda s: 更新参数(s, "质量"), pos=场景.title_anchor, step=1)
场景.append_to_title("质量\n")

速度滑动条 = slider(min=0, max=10, value=mag(滑块.速度), bind=lambda s: 更新参数(s, "速度"), pos=场景.title_anchor, step=0.1)
场景.append_to_title(" 初速度大小 ")

摩擦滑动条 = slider(min=0, max=1, value=滑块.摩擦系数, bind=lambda s: 更新参数(s, "摩擦系数"), pos=场景.title_anchor, step=0.01)
场景.append_to_title(" 摩擦系数\n ")

倾角滑动条 = slider(min=0, max=1.57, value=斜面倾角, bind=lambda s: 更新倾角(s.value), pos=场景.title_anchor, step=1.57/90)
场景.append_to_title(" 斜面倾角(弧度)")

重置=button(text='重置', bind=重置模拟)

def 计算加速度(位置, 速度):
    g = 10  
    
    重力分量 = -g * sin(斜面倾角)
    最大静摩擦力 = 滑块.摩擦系数 * g * cos(斜面倾角)

    if mag(速度) < 0.1:
        if abs(重力分量) <= 最大静摩擦力:
            return vector(0, 0, 0)  
  
    if mag(速度) > 0:
        摩擦力大小 = 滑块.摩擦系数 * g * cos(斜面倾角)
        摩擦力方向 = -norm(速度) 
        摩擦力 = 摩擦力方向 * 摩擦力大小
    else:
        摩擦力 = -重力分量 if abs(重力分量) <= 最大静摩擦力 else \
               (-最大静摩擦力 if 重力分量 > 0 else 最大静摩擦力)
    
    总加速度 = (重力分量 * norm(斜面.axis)) + 摩擦力
    
    return 总加速度


def rk4积分(位置, 速度, dt):
    加速度 = 计算加速度(位置, 速度)

    if mag(加速度) == 0:
        return 位置, vector(0, 0, 0)

    k1v = 加速度
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


while True:
    rate(100)
    
    if not 模拟运行中:
        continue
    
    斜面方向 = norm(斜面.axis)
    位移向量 = 滑块.pos - 斜面左端
    位移大小 = dot(位移向量, 斜面方向)

    if 位移大小 < 0:
        模拟运行中 = False
    else:
        滑块.pos, 滑块.速度 = rk4积分(滑块.pos, 滑块.速度, 时间步长)
    
    if mag(滑块.速度) <= 0.1:
        最远位移标签.text = f'最远位移: {位移大小:.2f} m'
        最远点 = sphere(pos=滑块.pos, radius=0.1, color=color.red)
    速度箭头.pos = 滑块.pos
    速度箭头.axis = 滑块.速度*0.3
    当前速度大小 = mag(滑块.速度)
    当前加速度大小 = mag(计算加速度(滑块.pos, 滑块.速度))
    当前加速度标签.text = f'当前加速度: {当前加速度大小:.2f} m/s²'
    当前速度标签.text = f'当前速度: {当前速度大小:.2f} m/s'
    位移标签.text = f'位移: {位移大小:.2f} m'