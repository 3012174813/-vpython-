from vpython import *

场景 = canvas(width=800, height=600, title="竖直上抛和自由落体模拟\n", background=color.white)

地面 = box(pos=vector(0, -1, 0), size=vector(4, 0.1, 4), color=color.yellow)
天花板 = box(pos=vector(0, 11, 0), size=vector(4, 0.1, 4), color=color.blue)
上抛球 = sphere(pos=vector(0, 0, 0), radius=1, color=color.red)
落体球 = sphere(pos=vector(0, 10, 0), radius=1, color=color.blue)
重力加速度 = 10

def 更新位置():
    global 时间
    天花板.pos = vector(0, 自由落体初高度.value+1, 0)
    上抛初速度文本.text = f"上抛初速度：{上抛初速度.value}"
    自由落体初高度文本.text = f"自由落体初高度：{自由落体初高度.value}"
    上抛球.pos =vector(0, 0, 0)
    落体球.pos = vector(0, 自由落体初高度.value, 0)
    上抛球.速度 = vector(0, 上抛初速度.value, 0)
    落体球.速度 = vector(0, 0, 0)
    相遇时间.text = "相遇时间：未相遇" 
    时间 = 0

上抛初速度 = slider(min=0, max=20, value=10, step=1, bind=更新位置,pos = 场景.title_anchor)
上抛初速度文本 = wtext(text=f"上抛初速度：{上抛初速度.value}", pos=场景.title_anchor)
自由落体初高度 = slider(min=0, max=20, value=10, step=1, bind=更新位置,pos = 场景.title_anchor)
自由落体初高度文本 = wtext(text=f"自由落体初高度：{自由落体初高度.value}", pos=场景.title_anchor)
相遇时间 = label(pos=vector(5, 5, 0), text="相遇时间：")

时间 = 0
dt = 0.01

while True:
    rate(100)
    时间 += dt
    上抛球.速度 = vector(0,上抛初速度.value - 重力加速度 * 时间,0)
    上抛球.pos += 上抛球.速度*dt
    落体球.速度 = vector(0, -重力加速度 * 时间, 0)
    落体球.pos += 落体球.速度*dt
    if mag(上抛球.pos - 落体球.pos )<= 0.1:
        相遇时间.text = f"相遇时间：{时间:.2f}秒"
    if 上抛球.pos.y <= 0 or 落体球.pos.y <= 0:
        更新位置()

        