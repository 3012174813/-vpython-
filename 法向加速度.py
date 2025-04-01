from vpython import *
import numpy as np

场景 = canvas(title="地球和卫星椭圆轨道模型", width=800, height=800, background=color.white)

G = 6.67430e-11  
地球质量 = 5.972e24  
地球半径 = 6.371e6  
缩放比例 = 1e-6  

地球 = sphere(pos=vector(0, 0, 0), radius=地球半径*缩放比例, texture=textures.earth, opacity=0.7)

半长轴 = 26.6e6  
离心率 = 0.74 
近地点距离 = 半长轴 * (1 - 离心率)

初始位置 = np.array([近地点距离, 0, 0])
初始速度大小 = np.sqrt(G * 地球质量 * (2/近地点距离 - 1/半长轴))
初始速度 = np.array([0, 初始速度大小, 0])
卫星状态 = np.concatenate((初始位置, 初始速度))

累计时间 = 0  
计算步长 = 100  
模拟运行中 = True 

卫星半径 = 0.5 * 地球半径 * 缩放比例  
卫星 = sphere(pos=vector(*初始位置)*缩放比例, radius=卫星半径, color=color.white, make_trail=True,opacity=0.7)

曲率圆 = ring(pos=vector(0,0,0), axis=vector(0,0,1), radius=地球半径*缩放比例, 
thickness=地球半径*缩放比例*0.05, color=color.orange)
引力箭头 = arrow(pos=卫星.pos, axis=vector(0,0,0), color=color.red, shaftwidth=卫星.radius*0.3, visible=True, opacity=0.7)
切向箭头 = arrow(pos=卫星.pos, axis=vector(0,0,0), color=color.blue, shaftwidth=卫星.radius*0.3, visible=True, opacity=0.7)
法向箭头 = arrow(pos=卫星.pos, axis=vector(0,0,0), color=color.green, shaftwidth=卫星.radius*0.3, visible=True, opacity=0.7)


def 创建标签(文本, y位置):
    return label(text=文本, pos=vector(0, -地球.radius*y位置, 0), box=False)


轨道标签 = 创建标签(f'半长轴: {半长轴/1e6:.1f}k km | 离心率: {离心率:.2f}', 2)
近远地点标签 = 创建标签(f'近地点: {半长轴*(1-离心率)/1e6:.1f}k km | 远地点: {半长轴*(1+离心率)/1e6:.1f}k km', 3)
线速度标签 = 创建标签('线速度: ', 4)
角速度标签 = 创建标签('角速度: ', 5)
周期标签 = 创建标签('周期: ', 6)
加速度标签 = 创建标签('加速度: ', 7)
时间标签 = 创建标签('运行时间: ', 8)
状态标签 = 创建标签('状态: 运行中', 9)
曲率标签 = 创建标签('曲率半径: ', 10)
曲率加速度标签 = 创建标签('曲率向心加速度: ', 11)
状态标签.color = color.green

def 切换状态(按钮):
    global 模拟运行中
    模拟运行中 = not 模拟运行中
    按钮.text = "继续模拟" if not 模拟运行中 else "暂停模拟"
    状态标签.text = "状态: 暂停" if not 模拟运行中 else "状态: 运行中"
    状态标签.color = color.red if not 模拟运行中 else color.green

控制按钮 = button(text="暂停模拟", bind=切换状态, pos=场景.title_anchor)

def 更新参数(值):
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
    累计时间 = 0
    
    轨道标签.text = f'半长轴: {半长轴/1e6:.1f}k km | 离心率: {离心率:.2f}'
    近远地点标签.text = f'近地点: {近地点距离/1e6:.1f}k km | 远地点: {半长轴*(1+离心率)/1e6:.1f}k km'

半长轴滑动条 = slider(min=0.7, max=20, value=10, step=0.1, bind=更新参数, length=300, right=15, pos=场景.title_anchor)
离心率滑动条 = slider(min=0, max=0.99, value=0.5, step=0.01, bind=更新参数, length=300, right=15, pos=场景.title_anchor)


def 计算引力(位置):
    距离 = np.linalg.norm(位置)
    return -G * 地球质量 * 位置 / (距离 ** 3)

def 计算曲率(位置, 速度):
    global 法向加速度大小
    速度大小 = np.linalg.norm(速度)
    加速度 = 计算引力(位置)
    
    速度方向 = 速度 / 速度大小
    切向加速度 = np.dot(加速度, 速度方向) * 速度方向
    法向加速度 = 加速度 - 切向加速度
    法向加速度大小 = np.linalg.norm(法向加速度)
    
    曲率半径 = 速度大小**2 / 法向加速度大小 
    法向量 = 法向加速度 / 法向加速度大小
    return 曲率半径, 法向量



def RK4(状态, 步长):
    位置 = 状态[:3]
    速度 = 状态[3:]

    k1位置 = 速度
    k1速度 = 计算引力(位置)
    
    k2位置 = 速度 + 0.5*步长*k1速度
    k2速度 = 计算引力(位置 + 0.5*步长*k1位置)
    
    k3位置 = 速度 + 0.5*步长*k2速度
    k3速度 = 计算引力(位置 + 0.5*步长*k2位置)
    
    k4位置 = 速度 + 步长*k3速度
    k4速度 = 计算引力(位置 + 步长*k3位置)
    
    新位置 = 位置 + (步长/6)*(k1位置 + 2*k2位置 + 2*k3位置 + k4位置)
    新速度 = 速度 + (步长/6)*(k1速度 + 2*k2速度 + 2*k3速度 + k4速度)
    
    return np.concatenate((新位置, 新速度))


while True:
    rate(100)
    
    if not 模拟运行中:
        continue

    卫星状态 = RK4(卫星状态, 计算步长)
    当前位置 = 卫星状态[:3]
    当前速度 = 卫星状态[3:]

    卫星.pos = vector(*当前位置) * 缩放比例

    距离 = np.linalg.norm(当前位置)
    速度大小 = np.linalg.norm(当前速度)
    角速度 = 速度大小 / 距离
    周期 = 2 * np.pi * np.sqrt(半长轴**3 / (G * 地球质量))
    加速度大小 = G * 地球质量 / (距离 ** 2)

    曲率半径, 法向量 = 计算曲率(当前位置, 当前速度)
    曲率圆心 = 当前位置 + 曲率半径 * 法向量

    曲率圆.pos = vector(*曲率圆心) * 缩放比例
    曲率圆.radius = 曲率半径 * 缩放比例
    
    引力加速度 = 计算引力(当前位置)
    引力总大小 = np.linalg.norm(引力加速度)

    速度方向 = 当前速度 / np.linalg.norm(当前速度)
    切向加速度 = np.dot(引力加速度, 速度方向) * 速度方向
    法向加速度 = 引力加速度 - 切向加速度

    对数缩放 = np.log10(引力总大小)
    缩放后的长度 = 地球.radius * (1+对数缩放) /引力总大小*5
    
    引力箭头.pos = 卫星.pos
    引力箭头.axis = vector(*引力加速度) * 缩放后的长度 
    
    切向箭头.pos = 卫星.pos
    切向箭头.axis = vector(*切向加速度) * 缩放后的长度
    法向箭头.pos = 卫星.pos
    法向箭头.axis = vector(*法向加速度)  * 缩放后的长度 
    累计时间 += 计算步长
    曲率标签.text = f'曲率半径: {曲率半径/1e6:.1f} k km'
    曲率加速度标签.text = f'曲率向心加速度: {np.linalg.norm(法向加速度):.2f} 米/秒² | 切向加速度: {np.linalg.norm(切向加速度):.2f} 米/秒²'
    线速度标签.text = f'线速度: {速度大小:.1f} 米/秒'
    角速度标签.text = f'角速度: {角速度:.2e} 弧度/秒'
    周期标签.text = f'周期: {周期/3600:.2f} 小时'
    加速度标签.text = f'加速度: {加速度大小:.2f} 米/秒²'
    时间标签.text = f'运行时间: {累计时间/3600:.2f} 小时'