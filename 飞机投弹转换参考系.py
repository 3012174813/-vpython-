from vpython import *

场景 = canvas(title="飞机投弹模拟", width=800, height=600, background=color.white)

for i in range(20):
        地面 = box(pos=vector(-20 + i*2, 0, 0), size=vector(2, 1, 10), color=vector(0.3+0.02 * i, 0.2+0.05 * i, 0))

机体 = box(size=vector(4, 0.5, 1), color=color.blue)
机翼 = box(size=vector(2, 0.3, 3), color=color.red)
飞机 = compound([机体 ,机翼])
飞机.pos = vector(-15, 10, 0)
飞机.速度 = vector(10, 0, 0)  

炸弹 = sphere(pos=飞机.pos, radius=0.5, color=color.red, make_trail=True)
炸弹.速度 = 飞机.速度 

重力加速度 = vector(0, -10, 0)  
时间步长 = 0.01  

炸弹信息标签 = label(pos=vector(0, -6, 0), text="",  box=False)
飞机信息标签 = label(pos=vector(0, -2, 0), text="",  box=False)

菜单选项 = ['固定视角', '跟随炸弹', '跟随飞机']
摄像机模式 = menu(choices=菜单选项, bind=None, selected='固定视角', pos = 场景.title_anchor)

def 重置模拟():
    global 模拟时间
    飞机.pos = vector(-15, 10, 0)
    飞机.速度 = vector(10, 0, 0)
    炸弹.clear_trail()
    炸弹.color = color.red
    炸弹.pos = 飞机.pos
    炸弹.速度 = 飞机.速度

重置按钮 = button(bind=重置模拟, text="重置模拟",pos = 场景.title_anchor)
def 更新摄像机():
    if 摄像机模式.selected == '跟随炸弹' :
        场景.camera.pos = 炸弹.pos - norm(炸弹.速度) * 3  + vector(0, 0.5, 0)
        场景.camera.axis = 炸弹.速度  
    elif 摄像机模式.selected == '跟随飞机':
        场景.camera.pos = 飞机.pos 
        场景.camera.axis = vector(10, -100,0 ) 
    else:  
        场景.camera.pos = vector(0, 15, 30)
        场景.camera.axis = -vector(0, 15, 30)

while True:
    rate(30)  
    
    飞机.pos = 飞机.pos + 飞机.速度 * 时间步长
    
    炸弹.速度 = 炸弹.速度 + 重力加速度 * 时间步长
    炸弹.pos = 炸弹.pos + 炸弹.速度 * 时间步长
    更新摄像机()

    if 炸弹.pos.y  <= 1:
        炸弹.速度 = vector(0, 0, 0)
        炸弹.color = color.gray(0.5) 
    if 飞机.pos.x > 20:
         重置模拟()

    炸弹信息标签.text = f"炸弹位置: {炸弹.pos}\n炸弹速度: {炸弹.速度}\n"
    飞机信息标签.text = f"飞机位置: {飞机.pos}\n飞机速度: {飞机.速度}"