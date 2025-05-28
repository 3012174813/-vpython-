from vpython import *

场景 = canvas(title='机车启动模拟', width=800, height=300, background=color.white)

机车 = box(pos=vector(-10, 0, 0), size=vector(2, 0.5, 1), color=color.blue)
机车.速度 = 0.1  
机车.牵引加速度 = 0  
阻加速度 = 1
时间 = 0
dt = 0.01   
当前模式 = '恒功率'    

速度图表 = graph(title='速度-时间图', width=800, height=300, x=0, y=0, xtitle='时间 (秒)', ytitle='速度 (米/秒)')
速度曲线 = gcurve(color=color.red)

def 更新设置():
    global 时间 
    机车.速度 = 0.1
    功率显示.text = f'功率: {功率滑块.value} 瓦'
    加速度显示.text = f'加速度: {加速度滑块.value} 米/秒²'
def 模式切换():
    global 当前模式
    if 模式按钮.text == '切换恒功率启动':
        当前模式 = '恒功率'
        功率滑块.disabled = False
        加速度滑块.disabled = True
        模式按钮.text = '切换恒加速度启动'
    else:
        当前模式 = '恒加速度'
        功率滑块.disabled = False
        加速度滑块.disabled = False
        模式按钮.text = '切换恒功率启动'
    更新设置()

模式按钮 = button(text='切换恒加速度启动', bind=模式切换, pos=场景.title_anchor)
场景.append_to_title(' \n')

功率滑块 = slider(min=1, max=10, value=5, step=1, bind=更新设置, pos=场景.title_anchor)
功率显示 = wtext(text='功率: 5 瓦', pos=场景.title_anchor)

加速度滑块 = slider(min=0.1, max=2, value=1, step=0.1, bind=更新设置, pos=场景.title_anchor)
加速度滑块.disabled = True
加速度显示 = wtext(text='加速度: 1 米/秒²', pos=场景.title_anchor)

更新设置()

while True:
    rate(100)  
    if 当前模式 == '恒功率':
        机车.牵引加速度 = 功率滑块.value / 机车.速度 - 阻加速度
        机车.速度 += 机车.牵引加速度 * dt
    if 当前模式 == '恒加速度':
        机车.牵引加速度 =  加速度滑块.value
        if 机车.速度 * (加速度滑块.value + 阻加速度) > 功率滑块.value:
            机车.牵引加速度 = 功率滑块.value / 机车.速度 - 阻加速度
        机车.速度 += 机车.牵引加速度 * dt
    机车.pos.x += 机车.速度 * dt
    
    if 机车.pos.x > 10:
        机车.pos.x = -10
    
    时间 += dt
    速度曲线.plot(时间, 机车.速度)