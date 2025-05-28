from vpython import *

场景 = canvas(title="斜面有摩擦滑块", width=800, height=600, background=color.white)

斜面倾角 = 0.5236  
斜面长度 = 10
斜面左端 = vector(-斜面长度 / 2*cos(斜面倾角), -斜面长度 / 2*sin(斜面倾角), 0)
初始位置 = vector(0,0, 0)
初始速度 = vector(5 * cos(斜面倾角), 5 * sin(斜面倾角), 0)
初始质量 = 1
初始摩擦系数 = 0.2


斜面 = box(pos=vector(0, 0, 0), size=vector(斜面长度, 0.1, 2), color=color.green, axis=vector(cos(斜面倾角), sin(斜面倾角), 0))
滑块 = box(pos=斜面左端+vector(cos(斜面倾角),0,0), size=vector(1, 1, 1), color=color.blue, opacity=0.5, axis=斜面.axis, 速度=初始速度, 质量=初始质量, 摩擦系数=初始摩擦系数, make_trail=True)

while True:
    rate(100)