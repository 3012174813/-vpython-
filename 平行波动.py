from vpython import *

场景 = canvas(title="质点运动形成波\n", width=800, height=600, background=color.white)

def 更新标签():
    球数文本.text = f"球数量: {球数.value}"
    振幅文本.text = f"振幅: {振幅.value}\n"
    角速度文本.text = f"角速度: {角速度.value:.2f}"
    波速文本.text = f"波速: {波速.value}\n"
    波长文本.text = f"波长: {2 * pi * 波速.value / 角速度.value:.2f}"

球数 = slider(min=1, max=100, value=50, step=10, bind=更新标签, pos=场景.title_anchor)
球数文本 = wtext(text=f"球数量: {球数.value}", pos=场景.title_anchor)
振幅 = slider(min=1, max=10, value=5, step=1, bind=更新标签, pos=场景.title_anchor)
振幅文本 = wtext(text=f"振幅: {振幅.value}\n", pos=场景.title_anchor)
角速度 = slider(min=1*pi, max=10*pi, value=5*pi, step=1*pi, bind=更新标签, pos=场景.title_anchor)
角速度文本 = wtext(text=f"角速度: {角速度.value:.2f}", pos=场景.title_anchor)
波速 = slider(min=10, max=100, value=50, step=10, bind=更新标签, pos=场景.title_anchor)
波速文本 = wtext(text=f"波速: {波速.value}\n", pos=场景.title_anchor)
波长文本 = wtext(text=f"波长: {2 * pi * 波速.value / 角速度.value:.2f}", pos=场景.title_anchor)

球体列表 = []

for i in range(100):
    球 = sphere(pos=vector(-50+i, 0, 0), radius=0.5, color=color.blue)
    球体列表.append(球)

t = 0  
dt = 0.001  

while True:
    rate(100) 
    for n, 球 in enumerate(球体列表):
        if n < 球数.value:
            球.visible = True
            球.pos.y = 振幅.value * sin(角速度.value * t + 角速度.value / 波速.value  * n)
        else:
            球.visible = False
    t += dt


