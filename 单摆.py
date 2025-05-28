from vpython import *

场景 = canvas(width=800, height=600, title='单摆模拟\n', background=color.white)

重力 = 10
摆长 = 2.0
初始角度 = 30 * 1.57/90
当前角度 = 初始角度
角速度 = 0
时间步长 = 0.01
当前时间 = 0
支点 = vector(0, 3, 0)

摆球 = sphere(pos=支点-vector(0,摆长,0), radius=0.2, color=color.red, make_trail=True, retain=30)
摆绳 = cylinder(pos=支点, axis=摆球.pos-支点, radius=0.02, color=color.white)

近似周期标签 = label(pos=vector(0,2,0), text='',box = False)
精确周期标签 = label(pos=vector(0,1,0), text='',box  = False)
误差标签 = label(pos=vector(0,0,0), text='',box  = False)
当前时间标签 = label(pos=vector(0,-1,0), text='',box  = False)

def 更新参数():

    global 初始角度, 当前角度, 角速度, 当前时间, 计数,摆长, 近似周期, 精确周期

    摆长 = 摆长滑块.value
    摆长标签.text=f'摆长: {摆长:.1f}米'
    初始角度 = 初始角度滑块.value
    初始角度标签.text=f'初始角度: {degrees(初始角度):.0f}°'

    当前角度, 角速度, 当前时间 = 初始角度, 0, 0

    近似周期 = 2*pi*sqrt(摆长/重力)
    精确周期 = 近似周期 * (1 + sin(初始角度/2)**2/4 + 9/64*sin(初始角度/2)**4+ 25/256*sin(初始角度/2)**6+ 1225/16384*sin(初始角度/2)**8)

    近似周期标签.text = f'近似周期: {近似周期:.2f}s'
    精确周期标签.text = f'精确周期: {精确周期:.2f}s'
    误差标签.text = f'误差: {100*(精确周期-近似周期)/精确周期:.0f}%'
    当前时间标签.text = f'当前时间: {当前时间:.2f}s'

摆长滑块 = slider(min=1, max=5, value=摆长, step=0.1, pos=场景.title_anchor, bind=更新参数)
摆长标签 = wtext(text=f'', pos=场景.title_anchor)
初始角度滑块 = slider(min=1.57/90, max=1.57, value=初始角度, step=1.57/90, pos=场景.title_anchor, bind=更新参数)
初始角度标签 = wtext(text=f'', pos=场景.title_anchor)

更新参数()

def 更新摆球():
    global 当前角度, 角速度, 当前时间, 计数
    角加速度 = -重力/摆长 * sin(当前角度)
    角速度 += 角加速度 * 时间步长
    当前角度 += 角速度 * 时间步长
    摆球.pos = 支点 + vector(摆长*sin(当前角度), -摆长*cos(当前角度), 0)
    摆绳.axis = 摆球.pos - 支点

    当前时间 += 时间步长
    当前时间标签.text = f'当前时间: {当前时间:.2f}s'

while True:
    rate(100)
    更新摆球()

