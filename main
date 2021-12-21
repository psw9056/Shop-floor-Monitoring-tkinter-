import tkinter
import tkinter.font
from tkinter.ttk import *
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import socket

# socket 통신
HOST = '192.168.0.106'
PORT = 9056

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()
client_socket, addr = server_socket.accept()

print('Connected by', addr)

def receive_data():
    global total_in, total_out, CT, WIP, error1, error2
    data = client_socket.recv(1024)
    tmp = data.decode()
    SM = tmp.split()
    total_in = int(SM[0])
    total_out = int(SM[1])
    if float(SM[2]) != 0:
        CT = float(SM[2])
    WIP = int(SM[3])
    error1 = int(SM[4])
    error2 = int(SM[5])

    window.after(update_time, receive_data)

# GUI
window = tkinter.Tk()
window.title("Shop-floor Monitoring")
window.geometry("1000x950")
window.resizable(False, False)
title_font = tkinter.font.Font(family="맑은 고딕", size=20, weight="bold")  # 글꼴
subtitle_font = tkinter.font.Font(family="맑은 고딕", size=15, weight="bold")
normal_font = tkinter.font.Font(family="맑은 고딕", size=13)
error_font = tkinter.font.Font(family="맑은 고딕", size=35, weight="bold")
window.configure(bg='white')  # 배경색

# 변수 값
update_time = 1000  # 1000 = 1sec
graph_interval = 1000

total_in = 0
total_out = 0
CT = 0
WIP = 0
TH = 0
t_run = 0 # x축 값

interval1 = 100 # 위의 그래프 x축 범위
interval2 = 300 # 아래 그래프 x축 범위
min_x = 0 # x축 최소값
change_x = 0 # 시간 흐름에 따라 변화할 위의 그래프의 x축 최소값
change_x2 = 0 # 시간 흐름에 따라 변화할 아래 그래프의 x축 최소값
max_x = interval1 # 시간 흐름에 따라 변화할 위의 그래프의 x축 최소값
max_x2 = interval2 # 시간 흐름에 따라 변화할 위의 그래프의 x축 최소값
CT_ylim = 200 # CT 그래프 y축 범위
WIP_ylim = 20 # WIP 그래프 y축 범위
TH_ylim = 25 # TH 그래프 y축 범위

notebook = tkinter.ttk.Notebook(window, width=980, height=918)
notebook.pack()

start_time = time.time()

frame1 = tkinter.Frame(window)
notebook.add(frame1, text="Main")

label1 = tkinter.Label(frame1, text="Total         \n \n ", font=title_font, width=0, height=0)
label1.grid(row=0, column=0)

frame4 = tkinter.Frame(frame1, relief="solid", bd=2, width=900, height=50)
frame4.place(x=50, y=52.5)

label5 = tkinter.Label(frame4, text="                      Ball in:", font=normal_font, height=2, bg="white")
label5.grid(row=0, column=0)


def ball_in():
    global total_in
    ball_in_text = "            {0:03d}           EA".format(total_in)  # {}안에는 숫자 자리수 표현
    label6 = tkinter.Label(frame4, text=ball_in_text, font=normal_font, height=2, bg="white", fg="red")
    label6.grid(row=0, column=1)
    frame4.after(update_time, ball_in)


label7 = tkinter.Label(frame4, text="               Ball out:", font=normal_font, height=2, bg="white")
label7.grid(row=0, column=2)

def ball_out():
    global total_out
    ball_out_text = "             {0:03d}           EA                         ".format(total_out)  # {}안에는 숫자 자리수 표현
    label8 = tkinter.Label(frame4, text=ball_out_text, font=normal_font, height=2, bg="white", fg="red")
    label8.grid(row=0, column=3)
    frame4.after(update_time, ball_out)


label9 = tkinter.Label(frame1, text="", font=title_font, width=13)
label9.grid(row=1, column=0)

label10 = tkinter.Label(frame1, text="                Cycle Time(CT)", font=subtitle_font, width=23, height=1)
label10.grid(row=2, column=0)

label11 = tkinter.Label(frame1, text="", font=subtitle_font, width=6, height=1)  # 여백
label11.grid(row=2, column=1)

label12 = tkinter.Label(frame1, text="Work In Process(WIP)", font=subtitle_font, width=17, height=1)
label12.grid(row=2, column=2)

label13 = tkinter.Label(frame1, text="", font=subtitle_font, width=1, height=1)  # 여백
label13.grid(row=2, column=3)

label14 = tkinter.Label(frame1, text="Throughput(TH)", font=subtitle_font, width=16, height=1)
label14.grid(row=2, column=4)

frame5 = tkinter.Frame(frame1, relief="solid", bd=2, width=165, height=50)
frame5.place(x=125, y=209)

frame6 = tkinter.Frame(frame1, relief="solid", bd=2, width=239, height=50)
frame6.place(x=367, y=209)

frame7 = tkinter.Frame(frame1, relief="solid", bd=2, width=174, height=50)
frame7.place(x=607, y=209)

frame8 = tkinter.Frame(frame1, relief="solid", bd=2)
frame8.place(x=50, y=290)

CT_list = []
def cycle_time():
    global CT
    global t_run1
    cycle_time_text = "       {0:06.3f}     sec  ".format(CT)  # {}안에는 숫자 자리수 표현
    label12 = tkinter.Label(frame5, text=cycle_time_text, font=normal_font, height=2, bg="white", fg="red")
    label12.grid(row=0, column=0)
    CT_list.append(CT)
    frame5.after(update_time, cycle_time)


WIP_list = []
def work_in_process():
    global WIP
    work_in_process_text = "          {0:02d}        EA  ".format(WIP)  # {}안에는 숫자 자리수 표현
    label13 = tkinter.Label(frame6, text=work_in_process_text, font=normal_font, height=2, bg="white", fg="red")
    label13.grid(row=0, column=0)
    WIP_list.append(WIP)
    frame6.after(update_time, work_in_process)

TH_list = []
def throughput():
    global TH
    work_in_process_text = "     {0:03.3f}    EA/min ".format(TH)  # {}안에는 숫자 자리수 표현
    label14 = tkinter.Label(frame7, text=work_in_process_text, font=normal_font, height=2, bg="white", fg="red")
    label14.grid(row=0, column=0)
    TH_list.append(TH)
    if CT == 0:
       TH == 0
    else:
        TH = WIP / CT * 60
    frame7.after(update_time, throughput)


time_list = []
def run_time():
    lap_end_time = time.time()
    t_run = lap_end_time - start_time
    time_list.append(t_run)
    frame5.after(update_time, run_time)


fig = plt.figure(figsize=(8.8, 6.1))  # figure(도표) 생성 및 크기 조절 (가로, 세로)

CT_graph = plt.subplot(231, xlim=(min_x, max_x), ylim=(0, CT_ylim))
CT_graph.set_title('CT(sec)                                         ')
WIP_graph = plt.subplot(232, xlim=(min_x, max_x), ylim=(0, WIP_ylim))
WIP_graph.set_title('WIP(ea)                                       ')
TH_graph = plt.subplot(233, xlim=(min_x, max_x), ylim=(0, TH_ylim))
TH_graph.set_title('TH(ea/min)                                   ')
CT_graph2 = plt.subplot(234, xlim=(min_x, max_x2), ylim=(0, CT_ylim))
WIP_graph2 = plt.subplot(235, xlim=(min_x, max_x2), ylim=(0, WIP_ylim))
WIP_graph2.set_xlabel('time(sec)')
TH_graph2 = plt.subplot(236, xlim=(min_x, max_x2), ylim=(0, TH_ylim))

line_1, = CT_graph.plot(time_list, CT_list, lw=2, c='limegreen')  # lw = 선 두께, c = 색상
line_2, = WIP_graph.plot(time_list, WIP_list, lw=2, c='violet')
line_3, = TH_graph.plot(time_list, TH_list, lw=2, c='dodgerblue')
line_4, = CT_graph2.plot(time_list, CT_list, lw=2, c='limegreen')
line_5, = WIP_graph2.plot(time_list, WIP_list, lw=2, c='violet')
line_6, = TH_graph2.plot(time_list, TH_list, lw=2, c='dodgerblue')


def update_graph():
    global line_1, line_2, line_3, line_4, line_5, line_6
    # global CT_ylim, WIP_ylim, TH_ylim
    global change_x, max_x, change_x2, max_x2
    global anim_1, anim_2, anim_3, graph_interval

    fig = plt.figure(figsize=(8.8, 6.1))

    change_x += interval1
    max_x += interval1
    if change_x % interval2 == 0:
       change_x2 += interval2
       max_x2 += interval2
       time_list.clear()
       CT_list.clear()
       WIP_list.clear()
       TH_list.clear()

    CT_graph = plt.subplot(231, xlim=(change_x, max_x), ylim=(0, CT_ylim))
    CT_graph.set_title('CT(sec)                                         ')
    WIP_graph = plt.subplot(232, xlim=(change_x, max_x), ylim=(0, WIP_ylim))
    WIP_graph.set_title('WIP(ea)                                       ')
    TH_graph = plt.subplot(233, xlim=(change_x, max_x), ylim=(0, TH_ylim))
    TH_graph.set_title('TH(ea/min)                                   ')
    CT_graph2 = plt.subplot(234, xlim=(change_x2, max_x2), ylim=(0, CT_ylim))
    WIP_graph2 = plt.subplot(235, xlim=(change_x2, max_x2), ylim=(0, WIP_ylim))
    WIP_graph2.set_xlabel('time(sec)')
    TH_graph2 = plt.subplot(236, xlim=(change_x2, max_x2), ylim=(0, TH_ylim))

    line_1, = CT_graph.plot(time_list, CT_list, lw=2, c='limegreen')  # lw = 선 두께, c = 색상
    line_2, = WIP_graph.plot(time_list, WIP_list, lw=2, c='violet')
    line_3, = TH_graph.plot(time_list, TH_list, lw=2, c='dodgerblue')
    line_4, = CT_graph2.plot(time_list, CT_list, lw=2, c='limegreen')
    line_5, = WIP_graph2.plot(time_list, WIP_list, lw=2, c='violet')
    line_6, = TH_graph2.plot(time_list, TH_list, lw=2, c='dodgerblue')

    canvas = FigureCanvasTkAgg(fig, master=frame8)
    canvas.get_tk_widget().grid(column=0, row=0)

    anim_1 = FuncAnimation(fig, update_CT_graph, frames=200, interval=graph_interval)
    anim_2 = FuncAnimation(fig, update_WIP_graph, frames=200, interval=graph_interval)
    anim_3 = FuncAnimation(fig, update_TH_graph, frames=200, interval=graph_interval)

    frame8.after(interval1*1000, update_graph)


def update_CT_graph(i):
    line_1.set_data(time_list, CT_list)
    line_4.set_data(time_list, CT_list)


def update_WIP_graph(i):
    line_2.set_data(time_list, WIP_list)
    line_5.set_data(time_list, WIP_list)


def update_TH_graph(i):
    line_3.set_data(time_list, TH_list)
    line_6.set_data(time_list, TH_list)

error1 = 0
error1_2 = 0
error2 = 0
error2_2 = 0


def warning1():
    global error1, error1_2, toplevel1
    if error1 - error1_2 == 1:
        toplevel1 = tkinter.Toplevel(window)
        toplevel1.geometry("320x200")
        label15 = tkinter.Label(toplevel1, text="ERROR 1", font=error_font, fg="red2")
        label15.pack(pady=30)
        button1 = tkinter.Button(toplevel1, text="close", command=close_w1, width=4, height=1, font=normal_font)
        button1.pack(pady=10)
        error1_2 = error1
    if error1 - error1_2 == -1:
        error1_2 = 0
    window.after(update_time, warning1)


def warning2():
    global error2, error2_2, toplevel2
    if error2 - error2_2 == 1:
        toplevel2 = tkinter.Toplevel(window)
        toplevel2.geometry("320x200")
        label16 = tkinter.Label(toplevel2, text="ERROR 2", font=error_font, fg="red4")
        label16.pack(pady=30)
        button2 = tkinter.Button(toplevel2, text="close", command=close_w2, width=4, height=1, font=normal_font)
        button2.pack(pady=10)
        error2_2 = error2
    if error2 - error2_2 == -1:
        error2_2 = 0
    window.after(update_time, warning2)


def close_w1():
    global toplevel1
    toplevel1.withdraw()


def close_w2():
    global toplevel2
    toplevel2.withdraw()


window.after(0, receive_data)
frame5.after(0, run_time)
frame1.after(0, warning1)
frame1.after(0, warning2)
frame4.after(0, ball_in)
frame4.after(0, ball_out)
frame5.after(0, cycle_time)
frame6.after(0, work_in_process)
frame7.after(0, throughput)
frame8.after(interval1*1000, update_graph)

canvas = FigureCanvasTkAgg(fig, master=frame8)
canvas.get_tk_widget().grid(column=0, row=0)

anim_1 = FuncAnimation(fig, update_CT_graph, frames=200, interval=graph_interval)
anim_2 = FuncAnimation(fig, update_WIP_graph, frames=200, interval=graph_interval)
anim_3 = FuncAnimation(fig, update_TH_graph, frames=200, interval=graph_interval)

window.mainloop()
client_socket.close()
server_socket.close()
