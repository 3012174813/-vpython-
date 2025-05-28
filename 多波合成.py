from vpython import *
import numpy as np

场景 = canvas(title='多波合成\n', width=800, height=600, background=color.white)

def 更新标签():
    波1振幅文本.text = f"波1振幅: {波1振幅.value}"
    波2振幅文本.text = f"振幅: {波2振幅.value}\n"
    波1频率文本.text = f"波1频率: {波1频率.value:.2f}"
    波2频率文本.text = f"波2频率: {波2频率.value:.2f}\n"
    波1波速文本.text = f"波1波速: {波1波速.value}"
    波2波速文本.text = f"波2波速: {波2波速.value}\n"

波1振幅 = slider(min=1, max=10, value=5, step=1, bind=更新标签, pos=场景.title_anchor)
波1振幅文本 = wtext(text=f"波1振幅: {波1振幅.value}", pos=场景.title_anchor)
波2振幅 = slider(min=1, max=10, value=5, step=1, bind=更新标签, pos=场景.title_anchor)
波2振幅文本 = wtext(text=f"波2振幅: {波2振幅.value}\n", pos=场景.title_anchor)
波1频率 = slider(min=1, max=5, value=2, step=1, bind=更新标签, pos=场景.title_anchor)
波1频率文本 = wtext(text=f"波1频率: {波1频率.value}", pos=场景.title_anchor)
波2频率 = slider(min=1, max=5, value=2, step=1, bind=更新标签, pos=场景.title_anchor)
波2频率文本 = wtext(text=f"波2频率: {波2频率.value}\n", pos=场景.title_anchor)
波1波速 = slider(min=50, max=100, value=80, step=10, bind=更新标签, pos=场景.title_anchor)
波1波速文本 = wtext(text=f"波1波速: {波1波速.value}", pos=场景.title_anchor)
波2波速 = slider(min=50, max=100, value=80, step=10, bind=更新标签, pos=场景.title_anchor)
波2波速文本 = wtext(text=f"波2波速: {波2波速.value}\n", pos=场景.title_anchor)

波1 = curve(color=color.green, radius=0.02)
波2 = curve(color=color.red, radius=0.02)
波3 = curve(color=color.blue, radius=0.02)

球体列表 = []
for i in range(40):
    球 = sphere(pos=vector(-20+i, 0, 0), radius=0.5, color=color.blue)
    球体列表.append(球)

t = 0  
dt = 0.01  

位置 = np.arange(-20, 20, 1)
while True:
    rate(10) 
    波1.clear()
    波2.clear()
    波3.clear()
    
    角速度1 = 2 * np.pi * 波1频率.value
    角速度2 = 2 * np.pi * 波2频率.value
    相位1 = 位置 / 波1波速.value - t
    相位2 = 位置 / 波2波速.value + t
    y1 = 波1振幅.value * np.sin(角速度1 * 相位1)
    y2 = 波2振幅.value * np.sin(角速度2 * 相位2)
    y3 = y1 + y2
    
    for x, y1, y2, y3 in zip(位置, y1, y2, y3):
        波1.append(pos=vector(x, y1, 0))
        波2.append(pos=vector(x, y2, 0))
        波3.append(pos=vector(x, y3, 0))

    for i, 球 in enumerate(球体列表):
        波1位移 = 波1振幅.value * np.sin(角速度1 * (球.pos.x / 波1波速.value - t))
        波2位移 = 波2振幅.value * np.sin(角速度2 * (球.pos.x / 波2波速.value + t))
        球.pos.y = 波1位移 + 波2位移
    t += dt
