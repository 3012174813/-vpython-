from vpython import *

scene = canvas(title="地球和卫星模型", width=800, height=600, background=color.white)

G = 6.67430e-11 
地球质量 = 5.972e24  
地球半径 = 6.371e6  
缩放比例 = 1e-6  
地球 = sphere(pos=vector(0, 0, 0), radius=地球半径 * 缩放比例, texture=textures.earth)
轨道半径 = 10e7  
初始位置 = vector(轨道半径, 0, 0)  
卫星显示半径 = 0.5 * 地球半径 * 缩放比例  
线速度大小 = sqrt(G * 地球质量 / 轨道半径)
线速度 = vector(0, 线速度大小, 0)  

卫星 = sphere(pos=初始位置 * 缩放比例, radius=卫星显示半径, color=color.white, make_trail=True)

时间步长 = 100  
总时间 = 0

while True:
    rate(100)  
    
    # 计算地球对卫星的引力 (F = -GMm/r^2 * r_hat)
    显示坐标 = 卫星.pos - 地球.pos  
    实际距离 = mag(显示坐标) / 缩放比例 
    单位方向向量 = 显示坐标 / mag(显示坐标)  
    
    加速度大小 = G * 地球质量 / (实际距离 ** 2)
    加速度 = -加速度大小 * 单位方向向量  # 加速度向量
    
    # 更新速度和位置（先用实际单位计算，再转换为显示坐标）
    线速度 += 加速度 * 时间步长
    卫星.pos += 线速度 * 时间步长 * 缩放比例
    
    总时间 += 时间步长

