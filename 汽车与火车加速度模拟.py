from vpython import *

场景 = canvas(title='汽车与火车加速度模拟', width=1500, height=300, background=color.white)
场景.autoscale = False

火车 = box( size=vector(2, 1, 1), color=color.red,make_trail=True)
汽车 = box( size=vector(1, 0.5, 0.5), color=color.blue,make_trail=True)

跟随 = 汽车  
场景.camera.follow(跟随)

def 更新相机():
    global 跟随
    if 跟随 == 火车:
        跟随 = 汽车
    elif 跟随 == 汽车:
        跟随 = None  
    else:
        跟随 = 火车
    场景.camera.follow(跟随)

切换相机按钮 = button(text='切换相机', bind=更新相机, pos=场景.title_anchor)
场景.append_to_title('\n')

def 更新():
    global 时间
    火车.pos = vector(-位置差滑动条.value/2, 0, 0)
    汽车.pos = vector(位置差滑动条.value/2, 2, 0)
    位置差标签.text = f"初始位置差: {位置差滑动条.value:.1f} m\n"

    火车.速度 = vector(火车初速度滑动条.value, 0, 0)
    火车.加速度 = vector(火车加速度滑动条.value, 0, 0)
    火车初速度标签.text = f"火车初速度: {火车.速度.x:.1f} m/s"
    火车加速度标签.text = f"火车加速度: {火车.加速度.x:.1f} m/s²\n"

    汽车.速度 = vector(汽车初速度滑动条.value, 0, 0)
    汽车.加速度 = vector(汽车加速度滑动条.value, 0, 0)
    汽车初速度标签.text = f"汽车初速度: {汽车.速度.x:.1f} m/s"
    汽车加速度标签.text = f"汽车加速度: {汽车.加速度.x:.1f} m/s²\n"

    时间 = 0
    火车.clear_trail()
    汽车.clear_trail()
    火车速度曲线.delete()
    汽车速度曲线.delete()

位置差滑动条 = slider(min=-20, max=20, value=10, step=1, bind=更新, pos=场景.title_anchor)
位置差标签 = wtext(text="", pos=场景.title_anchor)
火车初速度滑动条 = slider(min=-10, max=10, value=0, step=0.1, bind=更新, pos=场景.title_anchor)
火车初速度标签 = wtext(text="", pos=场景.title_anchor)

火车加速度滑动条 = slider(min=-10, max=10, value=0, step=0.1, bind=更新, pos=场景.title_anchor)
火车加速度标签 = wtext(text="", pos=场景.title_anchor)

汽车初速度滑动条 = slider(min=-10, max=10, value=0, step=0.1, bind=更新, pos=场景.title_anchor)
汽车初速度标签 = wtext(text="", pos=场景.title_anchor)
汽车加速度滑动条 = slider(min=-10, max=10, value=0, step=0.1, bind=更新, pos=场景.title_anchor)
汽车加速度标签 = wtext(text="", pos=场景.title_anchor)

vt图 = graph(title='速度-时间图',  xtitle='时间 (s)', ytitle='速度 (m/s)')
火车速度曲线 = gcurve(color=color.red, label='火车速度')
汽车速度曲线 = gcurve(color=color.blue, label='汽车速度')
def 更新图():
    火车速度曲线.plot(pos=(时间, 火车.速度.x))
    汽车速度曲线.plot(pos=(时间, 汽车.速度.x))

dt = 0.01 
时间 = 0 
更新()
while True:
    rate(100)
    时间 += dt
    火车.速度 += 火车.加速度* dt
    火车.pos +=  火车.速度* dt
    汽车.速度 += 汽车.加速度* dt
    汽车.pos += 汽车.速度* dt
    更新图()

    if abs (火车.pos.x-汽车.pos.x) > 30:
        更新()