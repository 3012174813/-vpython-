from vpython import *

场景 = canvas(title="速度选择器\n", width=800, height=600, background=color.white)
粒子 = sphere(pos=vector(0, 0, 0), radius=0.5, color=color.cyan, make_trail=True)
上方 = box(pos=vector(0, -10, 0), size=vector(20, 0.1, 4), color=color.gray(0.2))
下方 = box(pos=vector(0, 10, 0), size=vector(20, 0.1, 4), color=color.gray(0.2))

电荷量 = 1 
质量 = 1e-7    
速度 = vector(1e6, 0, 0)  
磁场 = vector(0, 0, 0.3) 
电场 = vector(0, 0, 0)  

磁场箭头组 = []
电场箭头组 = []

def 更新场():
    for i in 磁场箭头组:
        i.visible = False
        i.delete()
    for i in 电场箭头组:
        i.visible = False
        i.delete()
    
    for x in range(-10, 11, 5):
        for y in range(-10, 11, 5):
            磁场箭头组.append(arrow(pos=vector(x, y, 0), axis=vector(0,0,3), opacity=0.3,shaftwidth=磁场滑块.value))

    for x in range(-8, 12, 4):
        for z in range(0, 4, 1):
            电场箭头组.append(arrow(pos=vector(x, -10, z), axis=vector(0,20,0), color=color.red, shaftwidth=电场滑块.value*2e-7 , opacity=0.3 if 电场滑块.value > 0 else 0))

def 更新参数():
    global 磁场, 电场, 电荷量, 速度
    速度 = vector(速度滑块.value * 1e6, 0, 0)  
    磁场 = vector(0, 0, 磁场滑块.value) 
    电场 = vector(0, 电场滑块.value, 0) 
    更新场()

    速度标签.text = f"粒子速度: {速度滑块.value*1e6:.1e}  m/s"
    磁场标签.text = f"磁场强度: {磁场.z:.1f} T\n"
    电场标签.text = f"电场强度: {电场.y:.1e} V/m\n"
    选择速度标签.text = f"选择速度: {abs(电场.y / 磁场.z):.1e}  m/s"

    粒子.pos = vector(0, 0, 0)
    粒子.clear_trail()

速度滑块 = slider(min=1, max=10, value=1.7, step=0.1, bind=更新参数)
速度标签 = wtext(text="")
磁场滑块 = slider(min=0.1, max=0.5, value=0.3, step=0.1, bind=更新参数)
磁场标签 = wtext(text="")
电场滑块 = slider(min=0, max=1e6, value=5e5, step=1e5, bind=更新参数)
电场标签 = wtext(text="")
选择速度标签 = wtext(text="")

更新参数()

dt = 2e-8 
def RK4(位置, 速度, 磁场, 电场, 电荷量, 质量, dt):
    def 计算加速度(速度):
        力 = 电荷量 * (电场 + cross(速度, 磁场))
        return 力 / 质量
    
    k1速度 = 计算加速度(速度) * dt
    k1位置 = 速度 * dt
    
    k2速度 = 计算加速度(速度 + 0.5*k1速度) * dt
    k2位置 = (速度 + 0.5*k1速度) * dt
    
    k3速度 = 计算加速度(速度 + 0.5*k2速度) * dt
    k3位置 = (速度 + 0.5*k2速度) * dt
    
    k4速度 = 计算加速度(速度 + k3速度) * dt
    k4位置 = (速度 + k3速度) * dt
    
    新速度 = 速度 + (k1速度 + 2*k2速度 + 2*k3速度 + k4速度) / 6
    新位置 = 位置 + (k1位置 + 2*k2位置 + 2*k3位置 + k4位置) / 6
    
    return 新位置, 新速度

while True:
    rate(100)  
    粒子.pos, 速度 = RK4(粒子.pos, 速度, 磁场, 电场, 电荷量, 质量, dt)
    if abs(粒子.pos.x) > 11: 
        粒子.clear_trail()
        粒子.pos.x = - 粒子.pos.x