from vpython import *
import numpy as np

场景 = canvas(title="地球和卫星模型RK4", width=800, height=800, background=color.white)

G = 6.67430e-11  
地球质量 = 5.972e24  
地球半径 = 6.371e6  
缩放比例 = 1e-6  
地球 = sphere(pos=vector(0, 0, 0), radius=地球半径 * 缩放比例, texture=textures.earth)
初始轨道半径 = 42e6  
当前轨道半径 = 初始轨道半径  
累计时间 = 0  

# 滑动条控制轨道半径
def 更新轨道半径(滑动条值):
    global 当前轨道半径, 卫星状态, 累计时间
    当前轨道半径 = 滑动条值.value * 1e7  # 滑动条范围：0.7e7 ~ 20e7
    初始线速度 = np.sqrt(G * 地球质量 / 当前轨道半径)
    卫星状态 = np.array([当前轨道半径, 0, 0, 0, 初始线速度, 0])  # [x, y, z, vx, vy, vz]
    卫星.pos = vector(当前轨道半径, 0, 0) * 缩放比例
    卫星.clear_trail()
    卫星.make_trail = True
    累计时间 = 0
    轨道半径标签.text = f'轨道半径: {当前轨道半径/1e6:.1f}k km'

轨道半径滑动条 = slider(min=0.7, max=20, value=4.2, step=0.1, bind=更新轨道半径, length=600, right=15, pos=场景.title_anchor)

# 标签显示
轨道半径标签 = label(text=f'轨道半径: {初始轨道半径/1e6:.1f}k km',   pos=vector(0, -地球.radius*2, 0), box=False)
线速度标签 = label(text='线速度:',  pos=vector(0, -地球.radius*3, 0), box=False)
角速度标签 = label(text='角速度: ',  pos=vector(0, -地球.radius*4, 0), box=False)
周期标签 = label(text='周期: ', pos=vector(0, -地球.radius*5, 0), box=False)
加速度标签 = label(text='加速度: ', pos=vector(0, -地球.radius*6, 0), box=False)
运行时间标签 = label(text='运行时间:', pos=vector(0, -地球.radius*7, 0), box=False)

卫星半径 = 0.5 * 地球半径 * 缩放比例  
卫星 = sphere(pos=vector(初始轨道半径, 0, 0) * 缩放比例, radius=卫星半径, color=color.white, make_trail=True)
卫星状态 = np.array([初始轨道半径, 0, 0, 0, np.sqrt(G * 地球质量 / 初始轨道半径), 0])

计算步长 = 100  

def 计算引力加速度(位置向量):
    距离 = np.linalg.norm(位置向量)
    return -G * 地球质量 * 位置向量 / (距离 ** 3)

def RK4(当前状态, 时间步长):
 
    x, y, z, vx, vy, vz = 当前状态
    位置 = np.array([x, y, z])
    速度 = np.array([vx, vy, vz])
    
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
    
    return np.array([新位置[0], 新位置[1], 新位置[2], 新速度[0], 新速度[1], 新速度[2]])

while True:
    rate(100) 
    
    卫星状态 = RK4(卫星状态, 计算步长)
    x, y, z = 卫星状态[0], 卫星状态[1], 卫星状态[2]
    卫星.pos = vector(x, y, z) * 缩放比例
    
    当前位置 = np.array([x, y, z])
    当前速度 = np.array([卫星状态[3], 卫星状态[4], 卫星状态[5]])
    实际距离 = np.linalg.norm(当前位置)
    线速度大小 = np.linalg.norm(当前速度)
    
    角速度 = 线速度大小 / 实际距离
    轨道周期 = 2 * np.pi / 角速度
    加速度大小 = G * 地球质量 / (实际距离 ** 2)
    
    累计时间 += 计算步长
    线速度标签.text = f'线速度: {线速度大小:.1f} 米/秒'
    角速度标签.text = f'角速度: {角速度:.2e} 弧度/秒'
    周期标签.text = f'周期: {轨道周期/3600:.2f} 小时'
    加速度标签.text = f'加速度: {加速度大小:.2f} 米/秒²'
    运行时间标签.text = f'运行时间: {累计时间/3600:.2f} 小时'