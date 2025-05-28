from vpython import *

场景 = canvas(width=1000, height=600, title='碰撞模拟\n',background=color.white)

def 更新系统():
    小球1.pos = vector(-15, 0, 0)
    小球2.pos = vector(0, 0, 0)
    小球1.质量 = 小球1质量滑块.value
    小球2.质量 = 小球2质量滑块.value
    小球1.radius = 小球1质量滑块.value**(1/3)
    小球2.radius = 小球2质量滑块.value**(1/3)
    小球1.速度.x = 小球1初速度滑块.value
    小球2.速度.x = 小球2初速度滑块.value
    更新标签()
    
def 更新标签():
    小球1质量标签.text = f'小球1质量 {小球1质量滑块.value}kg'
    小球2质量标签.text = f'小球2质量 {小球2质量滑块.value}kg\n'
    小球1初速度标签.text = f'小球1初速度 {小球1初速度滑块.value}m/s'
    小球2初速度标签.text = f'小球2初速度 {小球2初速度滑块.value}m/s\n'
    恢复系数标签.text = f'恢复系数 {恢复系数滑块.value}'
    小球1标签.text = f'小球1 动量 {小球1.质量 * 小球1.速度.x:.2f}kg·m/s\n能量 {小球1.质量 * (小球1.速度.x**2)/2: .2f}J'
    小球2标签.text = f'小球2 动量 {小球2.质量 * 小球2.速度.x:.2f}kg·m/s\n能量 {小球2.质量 * (小球2.速度.x**2)/2: .2f}J'

小球1质量滑块 = slider(min=1, max=50, value=10, step=1, bind=更新系统,pos = 场景.title_anchor)
小球1质量标签 = wtext(text=f'', pos = 场景.title_anchor)
小球2质量滑块 = slider(min=1, max=50, value=10, step=1,  bind=更新系统, pos = 场景.title_anchor)
小球2质量标签 = wtext(text=f'\n', pos = 场景.title_anchor)
小球1初速度滑块 = slider(min=-5, max=5, value=2, step=1, bind=更新系统, pos = 场景.title_anchor)
小球1初速度标签 = wtext(text=f'', pos = 场景.title_anchor)
小球2初速度滑块 = slider(min=-5, max=5, value=1, step=1,  bind=更新系统, pos = 场景.title_anchor)
小球2初速度标签 = wtext(text=f'\n', pos = 场景.title_anchor)
恢复系数滑块 = slider(min=0, max=1, value=0.9, step=0.1,  bind=更新系统, pos = 场景.title_anchor)
恢复系数标签 = wtext(text=f'\n', pos = 场景.title_anchor)

小球1 = sphere(pos=vector(-15, 0, 0), radius=小球1质量滑块.value**(1/3), color=color.red, 速度=vector(小球1初速度滑块.value, 0, 0), 质量=小球1质量滑块.value)
小球1标签 = label(pos=vector(-5, 0, 0), text=f'')
小球2 = sphere(pos=vector(0, 0, 0), radius=小球2质量滑块.value**(1/3), color=color.blue,速度=vector(小球2初速度滑块.value, 0, 0), 质量=小球2质量滑块.value)
小球2标签 = label(pos=vector(5, 0, 0), text=f'')

更新系统()


时间步长 = 0.02
while True:
    rate(100)
    
    小球1.pos += 小球1.速度 * 时间步长
    小球2.pos += 小球2.速度 * 时间步长
    if abs(小球1.pos.x - 小球2.pos.x) < 小球1.radius + 小球2.radius:
        小球1.速度.x = ((小球1.质量 -小球2.质量*恢复系数滑块.value)  * 小球1初速度滑块.value+  (1+ 恢复系数滑块.value) * 小球2.质量 * 小球2初速度滑块.value )/ (小球1.质量 + 小球2.质量)
        小球2.速度.x = ((小球2.质量 -小球1.质量*恢复系数滑块.value)  * 小球2初速度滑块.value+  (1+ 恢复系数滑块.value) * 小球1.质量 * 小球1初速度滑块.value )/ (小球1.质量 + 小球2.质量)
        更新标签()
        
 