from vpython import *

场景 = canvas(title='球形波动', width=800, height=600, background=color.white)

def 更新标签():
    球数文本.text = f"球数量: {球数.value}\n"
    相位文本.text = f"相位: {相位.value:.2f}"
    角速度文本.text = f"角速度: {角速度.value:.2f}"
    更新球体()

球数 = slider(min=1, max=100, value=36, step=5, bind=更新标签, pos=场景.title_anchor)
球数文本 = wtext(text=f"球数量: {球数.value}\n", pos=场景.title_anchor)
相位 = slider(min=0, max=90*pi/90, value=5*pi/90, step=5*pi/90, bind=更新标签, pos=场景.title_anchor)
相位文本 = wtext(text=f"相位: {相位.value:.2f}", pos=场景.title_anchor)
角速度 = slider(min=1*pi, max=10*pi, value=5*pi, step=1*pi, bind=更新标签, pos=场景.title_anchor)
角速度文本 = wtext(text=f"角速度: {角速度.value:.2f}", pos=场景.title_anchor)

球体列表 = []
def 更新球体():
    global 球体列表
    for 球 in 球体列表:
        球.visible = False
    球体列表 = []
    for i in range(球数.value):
        角度 = 2 * pi * i / 球数.value
        初位置 = vector(sin(角度), cos(角度), 0) 
        球 = sphere(pos=初位置, radius=0.03, color=color.blue)
        球体列表.append(球)

更新球体()
t = 0
dt = 0.001

while True:
    rate(100)
    t += dt
    for i, 球 in enumerate(球体列表):
        角度 = 2 * pi * i / 球数.value
        位置系数 = sin(角速度.value * t+相位.value*i)
        球.pos = vector(sin(角度), cos(角度), 0) *  位置系数
