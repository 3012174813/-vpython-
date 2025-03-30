from vpython import *
import numpy as np

场景 = canvas(title="地球和卫星椭圆轨道模型", width=800, height=800, background=color.white)

G = 6.67430e-11  
地球质量 = 5.972e24  
地球半径 = 6.371e6  
缩放比例 = 1e-6  
地球 = sphere(pos=vector(0, 0, 0), radius=地球半径 * 缩放比例, texture=textures.earth)
半长轴 = 26.6e6  
离心率 = 0.74 
累计时间 = 0  
近地点距离 = 半长轴 * (1 - 离心率)
初始位置 = np.array([近地点距离, 0, 0])
初始速度大小 = np.sqrt(G * 地球质量 * (2/近地点距离 - 1/半长轴))
初始速度 = np.array([0, 初始速度大小, 0])

模拟运行中 = True 

轨道参数标签 = label(text=f'半长轴: {半长轴/1e6:.1f}k km | 离心率: {离心率:.2f}', pos=vector(0, -地球.radius*2, 0), box=False)
近远地点标签 = label(text=f'近地点: {半长轴*(1-离心率)/1e6:.1f}k km | 远地点: {半长轴*(1+离心率)/1e6:.1f}k km', pos=vector(0, -地球.radius*3, 0), box=False)
线速度标签 = label(text='线速度: ', pos=vector(0, -地球.radius*4, 0), box=False)
角速度标签 = label(text='角速度: ', pos=vector(0, -地球.radius*5, 0), box=False)
周期标签 = label(text='周期: ', pos=vector(0, -地球.radius*6, 0), box=False)
加速度标签 = label(text='加速度: ', pos=vector(0, -地球.radius*7, 0), box=False)
运行时间标签 = label(text='运行时间: ', pos=vector(0, -地球.radius*8, 0), box=False)
状态标签 = label(text='状态: 运行中', pos=vector(0, -地球.radius*9, 0), color=color.green, box=False)
曲率半径标签 = label(text='曲率半径: ', pos=vector(0, -地球.radius*10, 0), box=False)

卫星半径 = 0.5 * 地球半径 * 缩放比例  
卫星 = sphere(pos=vector(*初始位置) * 缩放比例, radius=卫星半径, color=color.white, make_trail=True)
卫星状态 = np.concatenate((初始位置, 初始速度))
曲率圆箭头 = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, 1),color=color.red, shaftwidth=地球半径 * 缩放比例 * 0.1,visible=True)
曲率圆 = ring(pos=vector(0, 0, 0), axis=vector(0, 0, 1), radius=地球半径 * 缩放比例, thickness=地球半径 * 缩放比例 * 0.05, color=color.orange)

计算步长 = 100  

def 切换模拟状态(按钮):
    global 模拟运行中
    模拟运行中 = not 模拟运行中
    if 模拟运行中:
        按钮.text = "暂停模拟"
    else:
        按钮.text = "继续模拟"
控制按钮 = button(text="暂停模拟", bind=切换模拟状态, pos=场景.title_anchor)

def 更新轨道参数(滑动条值):
    global 半长轴, 离心率, 卫星状态, 累计时间
    半长轴 = 半长轴滑动条.value * 1e7
    离心率 = 离心率滑动条.value
    
    近地点距离 = 半长轴 * (1 - 离心率)
    初始位置 = np.array([近地点距离, 0, 0])
    初始速度大小 = np.sqrt(G * 地球质量 * (2/近地点距离 - 1/半长轴))
    初始速度 = np.array([0, 初始速度大小, 0])
    
    卫星状态 = np.concatenate((初始位置, 初始速度))
    卫星.pos = vector(*初始位置) * 缩放比例
    卫星.clear_trail()
    卫星.make_trail = True
    累计时间 = 0
    
    轨道参数标签.text = f'半长轴: {半长轴/1e6:.1f}k km | 离心率: {离心率:.2f}'
    近远地点标签.text = f'近地点: {近地点距离/1e6:.1f}k km | 远地点: {半长轴*(1+离心率)/1e6:.1f}k km'

半长轴滑动条 = slider(min=0.7, max=20, value=10, step=0.1, bind=更新轨道参数, length=300, right=15, pos=场景.title_anchor)
离心率滑动条 = slider(min=0, max=0.99, value=0.5, step=0.01, bind=更新轨道参数, length=300, right=15, pos=场景.title_anchor)

def 计算引力加速度(位置向量):
    距离 = np.linalg.norm(位置向量)
    return -G * 地球质量 * 位置向量 / (距离 ** 3)

def 计算曲率半径和法向量(位置, 速度):
    距离 = np.linalg.norm(位置)
    速度大小 = np.linalg.norm(速度)
    加速度 = -G * 地球质量 * 位置 / 距离**3
    速度单位向量 = 速度 / 速度大小
    切向加速度 = np.dot(加速度, 速度单位向量) * 速度单位向量
    法向加速度 = 加速度 - 切向加速度
    法向加速度大小 = np.linalg.norm(法向加速度)
    曲率半径 = 速度大小**2 / 法向加速度大小 
    法向量 = 法向加速度 / 法向加速度大小
    return 曲率半径, 法向量

def RK4(当前状态, 时间步长):
    位置 = 当前状态[:3]
    速度 = 当前状态[3:]

    加速度1 = 计算引力加速度(位置)
    速度变化1 = 加速度1
    位置变化1 = 速度

    位置2 = 位置 + 0.5 * 时间步长 * 位置变化1
    加速度2 = 计算引力加速度(位置2)
    速度变化2 = 加速度2
    位置变化2 = 速度 + 0.5 * 时间步长 * 速度变化1

    位置3 = 位置 + 0.5 * 时间步长 * 位置变化2
    加速度3 = 计算引力加速度(位置3)
    速度变化3 = 加速度3
    位置变化3 = 速度 + 0.5 * 时间步长 * 速度变化2

    位置4 = 位置 + 时间步长 * 位置变化3
    加速度4 = 计算引力加速度(位置4)
    速度变化4 = 加速度4
    位置变化4 = 速度 + 时间步长 * 速度变化3

    新位置 = 位置 + (时间步长 / 6) * (位置变化1 + 2*位置变化2 + 2*位置变化3 + 位置变化4)
    新速度 = 速度 + (时间步长 / 6) * (速度变化1 + 2*速度变化2 + 2*速度变化3 + 速度变化4)
    return np.concatenate((新位置, 新速度))


while True:
    rate(100)  
    
    if 模拟运行中:  
        卫星状态 = RK4(卫星状态, 计算步长)
        当前位置 = 卫星状态[:3]
        卫星.pos = vector(*当前位置) * 缩放比例
        当前速度 = 卫星状态[3:]

        实际距离 = np.linalg.norm(当前位置)
        线速度大小 = np.linalg.norm(当前速度)
        角速度 = 线速度大小 / 实际距离 
        轨道周期 = 2 * np.pi * np.sqrt(半长轴**3 / (G * 地球质量))
        加速度大小 = G * 地球质量 / (实际距离 ** 2)
        当前半长轴 = 1 / (2/实际距离 - 线速度大小**2/(G * 地球质量))
        当前离心率 = np.sqrt(1 - np.linalg.norm(np.cross(当前位置, 当前速度))**2 / (G * 地球质量 * 当前半长轴))
        曲率半径, 法向量 = 计算曲率半径和法向量(当前位置, 当前速度)
        累计时间 += 计算步长
        曲率半径, 法向量 = 计算曲率半径和法向量(当前位置, 当前速度)
        曲率圆心物理位置 = 当前位置 + 曲率半径 * 法向量
    
        曲率圆.pos = vector(*曲率圆心物理位置) * 缩放比例  # 圆心位置
        曲率圆.radius = 曲率半径 * 缩放比例  # 圆的半径
        曲率圆.axis = vector(0,0,1) 
        曲率圆箭头.pos = vector(*当前位置) * 缩放比例  
        曲率圆箭头.axis = 曲率圆.pos - 曲率圆箭头.pos
        曲率圆箭头.visible = True

        曲率半径标签.text = f'曲率半径: {曲率半径/1e6:.1f} k km'
        线速度标签.text = f'线速度: {线速度大小:.1f} 米/秒'
        角速度标签.text = f'角速度: {角速度:.2e} 弧度/秒'
        周期标签.text = f'周期: {轨道周期/3600:.2f} 小时'
        加速度标签.text = f'加速度: {加速度大小:.2f} 米/秒²'
        运行时间标签.text = f'运行时间: {累计时间/3600:.2f} 小时'
        轨道参数标签.text = f'半长轴: {半长轴/1e6:.1f}k km | 离心率: {离心率:.2f}'
        近远地点标签.text = f'近地点: {半长轴*(1-离心率)/1e6:.1f}k km | 远地点: {半长轴*(1+离心率)/1e6:.1f}k km'
        状态标签.text = "运行"
        状态标签.color = color.green
    else:
        状态标签.text = "暂停"
        状态标签.color = color.red