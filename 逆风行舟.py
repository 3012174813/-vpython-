from vpython import *

场景 = canvas(width=800, height=800, background=color.white)

风速 = 10  
船体质量 = 100
dt = 0.01

船体 = box(pos=vector(0,0,-1), size=vector(2,5,1), color=color.blue,速度=vector(0,0,0), opacity=0.2)
船帆 = box(pos=船体.pos + vector(0,0,2.5), size=vector(0.1,4,4), color=color.gray(0.8), opacity=0.5)
船头 = cone(pos=船体.pos + vector(0, 2.5, 0), axis=vector(0, 2.5, 0), radius=1,opacity=0.5)
风向列表 = []
def 发射风向():
    for i in range(20):
        风向箭头 = arrow(pos=vector(-10+i,10,2), axis=vector(0,-1,0)*风速/2, color=color.blue,opacity=0.2,shaftwidth=0.2)
        风向箭头.速度 = vector(0,-10,0)
        风向列表.append(风向箭头)

合力箭头 = arrow(pos=船体.pos, axis=vector(0,0,0), color=color.red, shaftwidth=0.3)
前进力箭头 = arrow(pos=船体.pos+vector(0,-1,0), axis=vector(0,0,0), color=color.magenta, shaftwidth=0.2)
侧向力箭头 = arrow(pos=船体.pos+vector(0,-1,0), axis=vector(0,0,0), color=color.cyan, shaftwidth=0.2)

标签组 = [
    label(pos=vector(-5,10,0), text="总风力: 0 N",box=False),
    label(pos=vector(-5,9,0), text="前进力: 0 N",box=False),
    label(pos=vector(-5,8,0), text="船速: 0 m/s",box=False),
]

def 旋转物体(物体, 滑块):
    新方向 = vector(cos(滑块.value), sin(滑块.value), 0) 
    原始长度 = mag(物体.axis)
    物体.axis = 新方向 * 原始长度
    船体.pos = vector(0,0,-1)
    船体.速度 = vector(0,0,0)
    船帆.pos = 船体.pos + vector(0,0,2.5)
    if 物体 == 船体:
        船方向 = vector(-sin(滑块.value), cos(滑块.value), 0)
        船头.axis = 船方向 * 2.5
    计算受力()

船帆滑块 = slider(min=-1.57, max=1.57, value=0, step=1.57/90, bind=lambda 滑块: 旋转物体(船帆, 滑块), pos=场景.title_anchor)
船体滑块 = slider(min=-1.57, max=1.57, value=0, step=1.57/90, bind=lambda 滑块: 旋转物体(船体, 滑块), pos=场景.title_anchor)

def 计算受力():
    global 船体速度,前进力,风力方向,帆法向量

    风速向量 = vector(0, -风速, 0)
    帆法向量 = vector(cos(船帆滑块.value), sin(船帆滑块.value), 0)
    垂直分量 = proj(-风速向量, 帆法向量)
    风力方向 = norm(-垂直分量)
    风力大小 = mag2(垂直分量)
    总风力 = 风力大小 * 风力方向

    船方向 = vector(-sin(船体滑块.value), cos(船体滑块.value), 0)
    船侧向 = vector(-船方向.y, 船方向.x, 0)
    前进力 = proj(总风力, 船方向)
    侧向力 = proj(总风力, 船侧向)

    更新箭头(总风力, 前进力, 侧向力)
    更新标签(总风力, 前进力, mag(船体.速度))

def 更新箭头(总力, 前进力, 侧向力):

   合力箭头.axis = 总力/5
   前进力箭头.axis = 前进力/5
   侧向力箭头.axis = 侧向力/5

   合力箭头.pos = 船帆.pos
   前进力箭头.pos = 船体.pos 
   侧向力箭头.pos = 船体.pos 

def 更新标签(总力, 前进力, 船速):
    标签组[0].text = f"总风力: {mag(总力):.1f} N"
    标签组[1].text = f"前进力: {mag(前进力):.1f} N"
    标签组[2].text = f"船速: {船速:.1f} m/s"

def 更新运动():
    global 前进力,风速向量,帆法向量
    
    加速度 = 前进力  / 船体质量
    船体.速度 += 加速度 * dt
    船体.pos += 船体.速度 * dt
    船帆.pos = 船体.pos + vector(0,0,2.5)
    船头.pos = 船体.pos + vector(1,0,0)
    船头.axis = norm(船体.速度) 
    船方向 = vector(-sin(船体滑块.value), cos(船体滑块.value), 0)
    船头.pos = 船体.pos + 船方向 * 2.5

    if 船体.pos.mag >10:
        船体.pos = vector(0, 0, 0)
    for 风向箭头 in 风向列表:
        风向箭头.pos += 风向箭头.速度  * dt
        if mag(风向箭头.pos-船帆.pos ) < 1:
            风向箭头.速度 = 风向箭头.速度-2*dot(风向箭头.速度,帆法向量)*帆法向量
            风向箭头.axis = norm(风向箭头.速度) * 风速/2

        if 风向箭头.pos.mag> 15:
            风向箭头.visible = False
            风向列表.remove(风向箭头)

while True:
    rate(100)
    if len(风向列表) < 18:
        发射风向()
    计算受力()
    更新运动()
