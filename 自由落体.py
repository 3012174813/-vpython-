from vpython import *

场景 = canvas(title='小球自由落体', width=800, height=600, background=color.white)
小球 = sphere(pos=vector(0, 19.6, 0), radius=1, color=color.blue)
地面 = box(pos=vector(0, -1, 0), size=vector(20, 0.1, 20), color=color.green)


时间 = 0
g = 9.8  
dt = 0.001
初始高度 = 19.6
高度 = 初始高度
速度 = 0    

def 高度调整(s):
    global 高度, 速度, 时间, 初始高度
    初始高度 = s.value
    高度 = 初始高度
    小球.pos.y = 高度
    速度 = 0
    时间 = 0
    初始高度标签.text = f'初始高度: {初始高度:.2f} m'
高度滑块 = slider(min=0, max=50, value=初始高度, length=600, bind=高度调整,pos=场景.title_anchor)

初始高度标签 = label(pos=vector(-8, 12, 0), text=f'初始高度: {初始高度:.2f} m',box=False)
高度标签 = label(pos=vector(-8, 10, 0), text='高度:',box=False)
速度标签 = label(pos=vector(-8, 8, 0), text='速度: ',box=False)
时间标签 = label(pos=vector(-8, 6, 0), text='时间:',box=False)
def RK4(y, v, dt, g):
    k1v = -g * dt  
    k1y = v * dt
    
    k2v = -g * dt
    k2y = (v + k1v/2) * dt
    
    k3v = -g * dt
    k3y = (v + k2v/2) * dt
    
    k4v = -g * dt
    k4y = (v + k3v) * dt

    new_v = v + (k1v + 2*k2v + 2*k3v + k4v)/6
    new_y = y + (k1y + 2*k2y + 2*k3y + k4y)/6
    
    return new_y, new_v

  
while True:
    rate(1000)
    if 高度 > 0:
        高度, 速度 = RK4(高度, 速度, dt, g)
        小球.pos.y = 高度
        时间 += dt
        时间标签.text = f'时间: {时间:.2f} s'   
        高度标签.text = f'高度: {高度:.2f} m'
        速度标签.text = f'速度: {速度:.2f} m/s'