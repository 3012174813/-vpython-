from vpython import *
import random
import numpy as np

场景 = canvas(title='光电效应模拟', width=800, height=600, background=color.white)
图 = graph(title="光电效应电流与电压关系图", xtitle="电压 (V)", ytitle="电流 (mA)", width=600, height=600)

普朗克常数 = 6.626e-34  
光速 = 3.0e8     
电子电荷 = 1.602e-19 
电子质量 = 9.109e-31  

光强 = 50 
波长 = 400  
光功率 = 1
外加电压 = 0 

光子列表 = []
电子列表 = []
曲线列表 = []
金属列表 = {
            
    '铯(Cs)': 1.95, '铷(Rb)': 2.26,     
    '钾(K)': 2.29, '钠(Na)': 2.36,   
    '钙(Ca)': 2.87,'锂(Li)': 2.93,
    '镁(Mg)': 3.66,'铝(Al)': 4.26,  '锌(Zn)': 4.33,
    '铁(Fe)': 4.50, '钨(W)': 4.55  ,     
    '银(Ag)': 4.74, '铜(Cu)': 4.94,    
    '金(Au)': 5.47,'铂(Pt)': 5.93, 
}
当前金属 = '铯(Cs)'
功函数 = 金属列表[当前金属]

金属板 = box(pos=vector(-5,0,0), size=vector(0.5,4,4), opacity=0.7)
金属标签 = label(pos=vector(-5,-5,0), text=f'金属: {当前金属}', color=color.black, box=False)
逸出功标签 = label(pos=vector(-5,-6,0), text=f'逸出功: {功函数} eV', box=False)
收集板 = box(pos=vector(5,0,0), size=vector(0.5,4,4), color=vector(0.7,0.7,0.7), opacity=0.3)
收集板标签 = label(pos=vector(5,-5,0), text='收集板', color=color.black,  box=False)
距离标签 = label(pos=vector(0,-5,0), text='两板距离=10', color=color.black,  box=False)
光源 = sphere(pos=vector(0,5,0), size=vector(1,3,3), color=color.yellow, opacity=0.3,axis=vector(1, 1, 0))
光源标签 = label(pos=vector(0,6,0), text='光源', box=False)
光束箭头 = arrow(pos=vector(-1,4,0), axis=vector(-3,-3,0), shaftwidth=0.5, color=color.yellow)
拐点电压标签 = label(pos=vector(0,7,0),  box=False)

def 更新金属(菜单选择):
    global 当前金属, 功函数
    当前金属 = 菜单选择.selected
    功函数 = 金属列表[当前金属]
    金属标签.text = f'金属: {当前金属}'
    逸出功标签.text = f'逸出功: {功函数} eV'
    更新参数()
 
金属菜单 = menu(choices=list(金属列表.keys()), bind=更新金属, selected=当前金属,pos=场景.title_anchor)

波长滑块 = slider(min=100, max=700, value=400, bind=lambda: 更新参数(),step = 5,pos=场景.title_anchor )
场景.append_to_title("波长 (nm): ")
波长标签 = label(pos=vector(0,10,0), text=f'波长: {波长} nm', box=False)

光强滑块 = slider(min=0, max=100, value=50, bind=lambda: 更新参数(),step = 5,pos=场景.title_anchor)
场景.append_to_title("强度 (%): \n")
光强标签 = label(pos=vector(0,4,0), text=f'强度: {光强  }%', box=False)

电压滑块 = slider(min=-5, max=5, value=0,  bind=lambda: 更新参数(),step = 0.01,pos=场景.title_anchor)
场景.append_to_title("电压 (V): ")
电压标签 = label(pos=vector(0,-7,0), text=f'电压: {外加电压} V',box=False)

信息标签 = label(pos=vector(0,0,0), text='可以激发出电子 最大动能:1.15ev',box=False)
电流标签 = label(pos=vector(0,-6,0), text='电流:', box=False)
能量标签 = label(pos=vector(0,5,0), text='光子能量:3.10ev', box=False)

def 更新光束外观():
    global 光束颜色
    波长值 = 波长滑块.value
    if 波长值 < 440:
        光束颜色 = color.blue
    elif 波长值 < 490:
        光束颜色 = color.cyan
    elif 波长值 < 560:
        光束颜色 = color.green
    elif 波长值 < 590:
        光束颜色 = color.yellow
    elif 波长值 < 630:
        光束颜色 = vector(1.0, 0.5, 0) 
    else:
        光束颜色 = color.red
    光束箭头.color = 光束颜色
    光束箭头.shaftwidth = 光强/100

def 更新参数():
    global 波长, 光强, 外加电压
    波长 = 波长滑块.value
    光强 = 光强滑块.value
    外加电压 = 电压滑块.value
    波长标签.text = f'波长: {波长} nm'
    光强标签.text = f'强度: {光强}%'
    电压标签.text = f'电压: {外加电压} V'
    光子能量 = (普朗克常数 * 光速) / (波长 * 1e-9) / 电子电荷  
    能量标签.text = f'光子能量: {光子能量:.2f} eV'
    更新光束外观()
    if 光子能量 < 功函数:
        信息标签.text = f'光子能量不足 (需要 > {功函数:.2f} eV)'
    else:
        信息标签.text = f'可以激发出电子 (最大动能: {光子能量-功函数:.2f} eV)'

更新光束外观()

def 发射光子():
    global 光子列表,发射数量

    发射数量 = int(光强 / 5) 
    
    for _ in range(发射数量):
        
        初始位置 = vector(random.uniform(-1, 1), random.uniform(4, 6), random.uniform(-1, 1))
        
        光子 = sphere(pos=初始位置, radius=0.1, color=光束颜色)
        光子.速度 = vector(-0.5, -0.5, 0) + vector(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(-0.1, 0.1)) 
        光子列表.append(光子)

def 发射电子():
    global 电子列表

    光子能量 = 普朗克常数 * 光速 / (波长 * 1e-9)
    动能 = 光子能量 - 功函数 * 电子电荷
    if 动能 <= 0:
        return

    for _ in range(发射数量):

        if random.random() < 0.05: 
            
            速度 = sqrt(2 * 动能 / 电子质量)

            极角 = random.uniform(0, 0.3925)  
            方位角 = random.uniform(0, 6.28)
            
            vx = 速度 * cos(极角)  
            vy = 速度 * sin(极角) * cos(方位角)  
            vz = 速度 * sin(极角) * sin(方位角)

            初始位置 = 金属板.pos - vector(-0.5,random.uniform(-2, 2),random.uniform(-2, 2))
            
            电子 = sphere(pos=初始位置, radius=0.2)
            电子.速度 = vector(vx, vy, vz)
            电子列表.append(电子)


def 绘制光电效应曲线():
    global 曲线列表

    光子能量 = (普朗克常数 * 光速) / (波长 * 1e-9) / 电子电荷  # in eV
    功函数_eV = 功函数
    
    if 光子能量 < 功函数_eV:
        拐点电压标签.text = "光子能量不足，无法产生光电流"
        return
 
    遏止电压 = (光子能量 - 功函数_eV)
    电压范围 = np.linspace(-5, 5, 100)
    电流值 = []

    for V in 电压范围:
        if V <= -遏止电压:
            I = 0
        else: 
            电子数 = 光功率/光子能量/10*光强/100
            I = 电子数*(2*光子能量 - 2*功函数_eV + 2*V)**0.5*1000
        电流值.append(I)

    曲线颜色 = 光束颜色

    曲线标签 = f"{当前金属}, {波长}nm, {光强}%"
    曲线 = gcurve(graph=图, color=曲线颜色, width=2, label=曲线标签)
    for V, I in zip(电压范围, 电流值):
        曲线.plot(V, I)
    曲线列表.append(曲线)

    图.legend = True

    遏止点 = gdots(graph=图, color=color.black, size=5)
    遏止点.plot(-遏止电压, 0)
    曲线列表.append(遏止点)

    拐点电压标签.text = f"遏止电压: {-遏止电压:.2f} V"
    拐点电压标签.color = color.black

绘图按钮 = button(text="绘制光电效应曲线", bind=绘制光电效应曲线,pos=场景.title_anchor)

while True:
    rate(100) 

    if random.random() < 0.1: 
        发射光子()

    for 光子 in 光子列表[:]:
        光子.pos += 光子.速度

        if 光子.pos.x <= 金属板.pos.x :
            光子.visible = False
            光子列表.remove(光子)
            电子 = 发射电子()

    for 电子 in 电子列表[:]:

        电子.速度.x += 电压滑块.value*电子电荷/电子质量*1e-8
        电子.pos += 电子.速度*1e-7
        if abs(电子.pos.x) > 6 or abs(电子.pos.y) >3 or abs(电子.pos.z) > 3: 
            电子.visible = False
            电子列表.remove(电子)
