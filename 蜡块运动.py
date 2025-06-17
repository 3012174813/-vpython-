from vpython import *

场景 = canvas(title='蜡块速度合成', width=800, height=600, background=color.white)
场景.autoscale = False

管 = box( size=vector(1, 10, 1), color=color.blue,opacity=0.5)
蜡块 = sphere( radius=0.4, color=color.red,make_trail=True,trail_type = 'points',interval=20)

跟随 = 蜡块  
场景.camera.follow(跟随)
def 更新相机():
    global 跟随
    if 跟随 == 管:
        跟随 = 蜡块
    elif 跟随 == 蜡块:
        跟随 = None  
    else:
        跟随 = 管
    场景.camera.follow(跟随)

切换相机按钮 = button(text='切换相机', bind=更新相机, pos=场景.title_anchor)
场景.append_to_title('\n')

def 更新():
    管.pos = vector(-5, 0, 0)
    蜡块.pos = vector(管.pos.x , -5, 0)
    
    管.速度 = vector(管初速度滑动条.value, 0, 0)
    管.加速度 = vector(管加速度滑动条.value, 0, 0)
    管初速度标签.text = f"管初速度: {管.速度.x:.1f} m/s"
    管加速度标签.text = f"管加速度: {管.加速度.x:.1f} m/s²\n"

    蜡块.速度 = vector(0 ,蜡块初速度滑动条.value,  0)+管.速度
    蜡块.加速度 = vector(0,蜡块加速度滑动条.value, 0)+管.加速度
    蜡块初速度标签.text = f"蜡块初速度: {蜡块.速度.y:.1f} m/s"
    蜡块加速度标签.text = f"蜡块加速度: {蜡块.加速度.y:.1f} m/s²\n"

    管.clear_trail()
    蜡块.clear_trail()

管初速度滑动条 = slider(min=0, max=2, value=0, step=0.1, bind=更新, pos=场景.title_anchor)
管初速度标签 = wtext(text="", pos=场景.title_anchor)
管加速度滑动条 = slider(min=0, max=2, value=0, step=0.1, bind=更新, pos=场景.title_anchor)
管加速度标签 = wtext(text="", pos=场景.title_anchor)

蜡块初速度滑动条 = slider(min=0, max=2, value=0, step=0.1, bind=更新, pos=场景.title_anchor)
蜡块初速度标签 = wtext(text="", pos=场景.title_anchor)
蜡块加速度滑动条 = slider(min=0, max=2, value=0, step=0.1, bind=更新, pos=场景.title_anchor)
蜡块加速度标签 = wtext(text="", pos=场景.title_anchor)

dt = 0.01 
更新()
while True:
    rate(100)

    管.速度 += 管.加速度* dt
    管.pos +=  管.速度* dt
    蜡块.速度 += 蜡块.加速度* dt
    蜡块.pos += 蜡块.速度* dt

    if mag (管.pos-蜡块.pos) > 5:
        更新()