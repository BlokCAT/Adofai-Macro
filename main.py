import json
import tkinter as tk
import pygetwindow as gw
import time
import keyboard
from tkinter import messagebox
from tkinter import filedialog


cor={
    ', }': '}',
    ',  }': '}',
    ']\n\t"decorations"': '],\n\t"decorations"',
    '],\n}': ']\n}',
    ',,': ',',
    '}\n\t\t{':'},\n\t\t{',
    '},\n\t]':'}\n\t]',
    '\n\\n':'\\n'
}

# 创建主窗口
window = tk.Tk()
window.title("DeleteEffect 1.0.1")
window.geometry("400x280")


path = None
click_time = []

def browse_file():

    global path
    filepath = filedialog.askopenfilename()  # 弹出文件选择对话框
    entry_path.delete(0, tk.END)  # 清除输入框当前内容
    entry_path.insert(0, filepath)  # 将选择的文件路径插入到输入框中
    path = filepath

contents = []
def count_click_time ():
    global path
    global click_time
    global wuliang
    global contents
    if path != None:

        with open(path, encoding="utf-8-sig") as f:
            info = f.read()
            for i in cor: info = info.replace(i, cor[i])
            contents = json.loads(info)

        pre = 0.0
        i = 0
        click_ag = []
        f = 0
        for angle in contents['angleData']:
            if angle == 999:
                f = 1
                click_ag.append(-1)
                continue
            if f == 0:
                inn = (180 + pre - angle) % 360
                click_ag.append(inn)
            else:
                if angle - pre > 0:
                    inn = 360 - (angle - pre)
                else:
                    inn = pre - angle
                click_ag.append(inn)
                f = 0
            pre = angle
            i += 1
        print("原始的：", click_ag)


        for action in contents['actions']:
            if action['eventType'] == 'Twirl':
                idx = action['floor']
                while idx < len(click_ag):
                    if click_ag[idx] != -1: click_ag[idx] = 360 - click_ag[idx]
                    idx += 1

        j = 0
        for i in click_ag:
            if i == 0:
                click_ag[j] = 360
            j += 1

        print("ag:", click_ag)

        BPM = []
        i = 0
        while i < len(click_ag):
            BPM.append(contents['settings']['bpm'])
            i += 1

        for i in contents['actions']:
            if i['eventType'] == 'SetSpeed':
                if i['speedType'] == 'Multiplier':
                    idx = i['floor']
                    while idx < len(BPM):
                        BPM[idx] =  BPM[idx] * i['bpmMultiplier']
                        idx += 1
                elif i['speedType'] == 'Bpm':
                    idx = i['floor']
                    while idx < len(BPM):
                        BPM[idx] = i['beatsPerMinute']
                        idx += 1

        print("BPM:", BPM)
        click_time = []
        for i, j in zip(BPM, click_ag):
            if j != -1:
                click_time.append((j / 360) * (120 / i))
            else:
                click_time.append(-1)

        for action in contents['actions']:
            if action['eventType'] == 'Pause':
                click_time[action['floor']] += (60/BPM[action['floor']])*action['duration']

        click_time.pop(0)
        print("click_time:", click_time)
        print()
    else:
        messagebox.showinfo("A dance of fire and ice", "请选择adofai文件！")


def autoPlay():  # auto算法
    global click_time
    global contents
    global Pause
    target_window_title = 'A Dance of Fire and Ice'
    window = gw.getWindowsWithTitle(target_window_title)[0]  # 获取窗口列表中的第一个匹配项
    window.activate()  # 激活窗口


    keyboard.press('[')
    keyboard.release('[')
    list = ['W','E' , '[' , ']' , '\\' , 'PgUp']
    i = 1
    now_time = time.perf_counter()  # 设置初始时间


    Pause = 1
    def fff(event):
        global Pause
        Pause = 0
    keyboard.on_press_key('space', fff)

    for cd in click_time:
        if Pause == 0:
            Pause = 1
            break
        if cd == -1:continue
        if cd <0.1:
            while time.perf_counter() - now_time < cd - 0.0003 :
                pass  # 未到预计时间阻塞进程
        else :
            while time.perf_counter() - now_time < cd:
                pass  # 未到预计时间阻塞进程
        now_time = now_time + cd
        keyboard.release(list[i%6])
        i += 1
        print(f"click time ：{cd}" )
        keyboard.press(list[i%6])




label1 = tk.Label(window,text="运行时点几下空格可以暂停",font=('黑体',12) , fg = 'red')
label1.pack(pady=8)

button = tk.Button(window, text='GO!', font=('黑体', 12 ), width=10, height=1, command= autoPlay )
button.pack(pady=9)
button = tk.Button(window, text='确定', font=('黑体', 12 ), width=10, height=1, command= count_click_time )
button.pack(pady=9)

center_frame = tk.Frame(window)
center_frame.pack(expand=True, anchor=tk.CENTER)

entry_path = tk.Entry(center_frame, width=30 )
entry_path.pack(side=tk.LEFT, padx=(0, 5))

button_browse = tk.Button(center_frame, text="浏览", command=browse_file )
button_browse.pack(side=tk.LEFT, padx=(5, 0))

window.mainloop()
