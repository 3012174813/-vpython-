from vpython import *

场景 = canvas(title="板块与木块堆叠模拟", width=1000, height=600, background=color.white)

参数 = {
    "板块长度": 5,
    "木块力大小": 1,
    "板块力大小": 2,
    "木块质量": 1,
    "板块质量": 5,
    "木块摩擦系数": 0.3,
    "板块摩擦系数": 0.2
}

地板 = box(pos=vector(0, 0, 0), size=vector(30, 0.1, 10), color=color.green)
板块 = box(pos=vector(0, 1, 0), size=vector(参数["板块长度"], 1, 2), color=color.blue)
木块 = box(pos=vector(-板块.size.x/2+0.5, 2, 0), size=vector(1, 1, 1), color=color.orange)

木块力箭头 = arrow(pos=vector(0,0,0), axis=vector(0,0,0), color=color.red, shaftwidth=0.1)
板块力箭头 = arrow(pos=vector(0,0,0), axis=vector(0,0,0), color=color.red, shaftwidth=0.1)
木块摩擦箭头 = arrow(pos=vector(0,0,0), axis=vector(0,0,0), color=color.purple, shaftwidth=0.1)
板块摩擦箭头 = arrow(pos=vector(0,0,0), axis=vector(0,0,0), color=color.purple, shaftwidth=0.1)

滑块配置 = [
    {"名称": "板块长度", "最小值": 2, "最大值": 20, "步长": 1},
    {"名称": "木块力大小", "最小值": 0, "最大值": 10, "步长": 0.5},
    {"名称": "板块力大小", "最小值": 0, "最大值": 10, "步长": 0.5},
    {"名称": "木块质量", "最小值": 0.1, "最大值": 5, "步长": 0.1},
    {"名称": "板块质量", "最小值": 1, "最大值": 10, "步长": 0.5},
    {"名称": "木块摩擦系数", "最小值": 0, "最大值": 1, "步长": 0.05},
    {"名称": "板块摩擦系数", "最小值": 0, "最大值": 1, "步长": 0.05}
]

def 更新参数(s, 参数名称):

    global 参数
    参数[参数名称] = s.value

    if 参数名称 == "板块长度":
        板块.size.x = 参数["板块长度"]
        木块.pos.x = -板块.size.x/2 + 0.5

    for 配置 in 滑块配置:
        if 配置["名称"] == 参数名称:
            globals()[f"{参数名称}标签"].text = f"{参数[参数名称]:}"
            break

    更新显示()

def 更新显示():

    木块力箭头.pos = vector(木块.pos.x + 0.5, 木块.pos.y, 0)
    木块力箭头.axis = vector(参数["木块力大小"]*0.5, 0, 0)
    板块力箭头.pos = vector(板块.pos.x + 板块.size.x/2, 板块.pos.y, 0)
    板块力箭头.axis = vector(参数["板块力大小"]*0.5, 0, 0)

    木块摩擦箭头.pos = vector(木块.pos.x, 木块.pos.y-0.5, 0)
    木块摩擦箭头.axis = vector(-参数["木块摩擦系数"]*10, 0, 0)
    板块摩擦箭头.pos = vector(板块.pos.x, 板块.pos.y-0.7, 0)
    板块摩擦箭头.axis = vector(-参数["板块摩擦系数"]*10, 0, 0)

for 配置 in 滑块配置:
    滑块 = slider(
        min=配置["最小值"], max=配置["最大值"], 
        value=参数[配置["名称"]], step=配置["步长"],
        bind=lambda s, n=配置["名称"]: 更新参数(s, n),
        pos=场景.title_anchor ,vertical=True,
        length=200, width=10
    )
    
    label(pos=vector(-3, 4, 0), 
         text=f"{配置['名称']}:", 
         color=color.black, box=False, height=16)
    
    globals()[f"{配置['名称']}标签"] = label(
        pos=vector(11, 4, 0),
        text=f"{参数[配置['名称']]:}",
        color=color.black, box=False, height=16
    )

while True:
    rate(100)