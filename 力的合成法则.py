from vpython import *

场景 = canvas(width=800, height=600,title='力的合成',background=color.white)
场景.autoscale = False

方法 = "平行四边形"
def 更新方法():
    global 方法
    if 方法 == "平行四边形":
        方法 = "三角形"
    else:
        方法 = "平行四边形"
    更新力()

切换按钮 = button(text='切换方法', bind=更新方法, pos=场景.title_anchor)
场景.append_to_title('\n')

原点 = vector(0, 0, 0)
力1箭头 = arrow(pos=原点, color=color.blue, shaftwidth=0.2)
力2箭头 = arrow(pos=原点, color=color.green, shaftwidth=0.2)
合力箭头 = arrow(pos=原点, color=color.red, shaftwidth=0.2)

移动的力箭头 = arrow(color=color.green, shaftwidth=0.2, visible=False)
平行线1 = curve(radius=0.05, opacity=0.3, color=color.green)
平行线2 = curve(radius=0.05, opacity=0.3, color=color.blue)

def 更新力():
   
    力1 = vector(力1大小滑块.value * cos(力1角度滑块.value), 力1大小滑块.value * sin(力1角度滑块.value), 0)
    力2 = vector(力2大小滑块.value * cos(力2角度滑块.value), 力2大小滑块.value * sin(力2角度滑块.value), 0)

    力1标签.text = f'力1大小：{力1大小滑块.value:.1f} N'
    力1角度标签.text = f'力1角度：{degrees(力1角度滑块.value):.0f} °\n'
    力2标签.text = f'力2大小：{力2大小滑块.value:.1f} N'
    力2角度标签.text = f'力2角度：{degrees(力2角度滑块.value):.0f} °\n'
    合力标签.text = f'合力大小：{mag(力1 + 力2):.1f} N'
    合力标签.pos = (力1 + 力2) /2

    力1箭头.axis = 力1
    力2箭头.axis = 力2
    合力箭头.axis = 力1 + 力2

    if 方法 == "平行四边形":
        平行线1.visible = 平行线2.visible = True
        移动的力箭头.visible = False
        平行线1.clear()
        平行线1.append([原点 + 力1, 原点 + 力1 + 力2])
        平行线2.clear()
        平行线2.append([原点 + 力2, 原点 + 力1 + 力2])
    else:
        移动的力箭头.visible = True
        平行线1.visible = 平行线2.visible = False
        移动的力箭头.pos = 原点 + 力1
        移动的力箭头.axis = 力2

力1大小滑块 = slider(min=0, max=10, value=5, bind=更新力, pos=场景.title_anchor)
力1标签 = wtext(text=f'', pos=场景.title_anchor)
力1角度滑块 = slider(min=0, max=6.28, value=3.14,step=3.14/180, bind=更新力,pos=场景.title_anchor)
力1角度标签 = wtext(text=f'\n', pos=场景.title_anchor)
力2大小滑块 = slider(min=0, max=10, value=5, bind=更新力,pos=场景.title_anchor)
力2标签 = wtext(text=f'', pos=场景.title_anchor)
力2角度滑块 = slider(min=0, max=6.28, value=6.28, step=3.14/180,bind=更新力,pos=场景.title_anchor)
力2角度标签 = wtext(text=f'\n', pos=场景.title_anchor)
合力标签 = label(text=f'')

更新力()

while True: rate(30)