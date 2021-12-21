import tkinter
import tkinter.font
from tkinter.ttk import *
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import socket

# socket 통신
HOST = '192.168.0.114'
PORT = 7779

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()
client_socket, addr = server_socket.accept()

print('Connected by', addr)

def receive_data():
    global total_in, total_out, CT, WIP, error1, error2
    global bb_in, bb_out, CT_2, WIP_2
    global sb_in, sb_out, CT_3, WIP_3
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

    bb_in = int(SM[6])
    bb_out = int(SM[7])
    if float(SM[8]) != 0:
        CT_2 = float(SM[8])
    WIP_2 = int(SM[9])

    sb_in = int(SM[10])
    sb_out = int(SM[11])
    if float(SM[12]) != 0:
        CT_3 = float(SM[12])
    WIP_3 = int(SM[13])

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

update_time = 1000  # 1000 = 1sec
graph_interval = 1000

total_in = 0

def ball_in():
    global total_in
    ball_in_text = "            {0:03d}           EA".format(total_in)  # {}안에는 숫자 자리수 표현
    label6 = tkinter.Label(frame4, text=ball_in_text, font=normal_font, height=2, bg="white", fg="red")
    label6.grid(row=0, column=1)
    frame4.after(update_time, ball_in)


label7 = tkinter.Label(frame4, text="               Ball out:", font=normal_font, height=2, bg="white")
label7.grid(row=0, column=2)

total_out = 0

def ball_out():
    global total_out
    ball_out_text = "             {0:03d}           EA                         ".format(total_out)  # {}안에는 숫자 자리수 표현
    label8 = tkinter.Label(frame4, text=ball_out_text, font=normal_font, height=2, bg="white", fg="red")
    label8.grid(row=0, column=3)
    frame4.after(update_time, ball_out)


label9 = tkinter.Label(frame1, text=" Productivity", font=title_font, width=13)
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

CT = 0
CT_list = []

def cycle_time():
    global CT
    global t_run1
    cycle_time_text = "       {0:06.3f}     sec  ".format(CT)  # {}안에는 숫자 자리수 표현
    label12 = tkinter.Label(frame5, text=cycle_time_text, font=normal_font, height=2, bg="white", fg="red")
    label12.grid(row=0, column=0)
    CT_list.append(CT)
    frame5.after(update_time, cycle_time)


WIP = 0
WIP_list = []

def work_in_process():
    global WIP
    work_in_process_text = "          {0:02d}        EA  ".format(WIP)  # {}안에는 숫자 자리수 표현
    label13 = tkinter.Label(frame6, text=work_in_process_text, font=normal_font, height=2, bg="white", fg="red")
    label13.grid(row=0, column=0)
    WIP_list.append(WIP)
    frame6.after(update_time, work_in_process)


TH = 0
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


t_run = 0
time_list = []

def run_time():
    lap_end_time = time.time()
    t_run = lap_end_time - start_time
    time_list.append(t_run)
    frame5.after(update_time, run_time)


fig = plt.figure(figsize=(8.8, 6.1))  # figure(도표) 생성 및 크기 조절 (가로, 세로)

interval1 = 100
interval2 = 300
min_x = 0
change_x = 0
change_x2 = 0
max_x = interval1
max_x2 = interval2
WIP_ylim = 20

CT_graph = plt.subplot(231, xlim=(min_x, max_x), ylim=(0, 200))
CT_graph.set_title('CT(sec)                                         ')
WIP_graph = plt.subplot(232, xlim=(min_x, max_x), ylim=(0, WIP_ylim))
WIP_graph.set_title('WIP(ea)                                       ')
TH_graph = plt.subplot(233, xlim=(min_x, max_x), ylim=(0, 25))
TH_graph.set_title('TH(ea/min)                                   ')
CT_graph2 = plt.subplot(234, xlim=(min_x, max_x2), ylim=(0, 200))
WIP_graph2 = plt.subplot(235, xlim=(min_x, max_x2), ylim=(0, WIP_ylim))
WIP_graph2.set_xlabel('time(sec)')
TH_graph2 = plt.subplot(236, xlim=(min_x, max_x2), ylim=(0, 25))

line_1, = CT_graph.plot(time_list, CT_list, lw=2, c='limegreen')  # lw = 선 두께, c = 색상
line_2, = WIP_graph.plot(time_list, WIP_list, lw=2, c='violet')
line_3, = TH_graph.plot(time_list, TH_list, lw=2, c='dodgerblue')
line_4, = CT_graph2.plot(time_list, CT_list, lw=2, c='limegreen')
line_5, = WIP_graph2.plot(time_list, WIP_list, lw=2, c='violet')
line_6, = TH_graph2.plot(time_list, TH_list, lw=2, c='dodgerblue')


def update_graph():
    global line_1, line_2, line_3, line_4, line_5, line_6
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

    CT_graph = plt.subplot(231, xlim=(change_x, max_x), ylim=(0, 200))
    CT_graph.set_title('CT(sec)                                         ')
    WIP_graph = plt.subplot(232, xlim=(change_x, max_x), ylim=(0, WIP_ylim))
    WIP_graph.set_title('WIP(ea)                                       ')
    TH_graph = plt.subplot(233, xlim=(change_x, max_x), ylim=(0, 25))
    TH_graph.set_title('TH(ea/min)                                   ')
    CT_graph2 = plt.subplot(234, xlim=(change_x2, max_x2), ylim=(0, 200))
    WIP_graph2 = plt.subplot(235, xlim=(change_x2, max_x2), ylim=(0, WIP_ylim))
    WIP_graph2.set_xlabel('time(sec)')
    TH_graph2 = plt.subplot(236, xlim=(change_x2, max_x2), ylim=(0, 25))

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

########################################################################################################################
# page 2
frame1_2 = tkinter.Frame(window)
notebook.add(frame1_2, text="Basket ball")

label1_2 = tkinter.Label(frame1_2, text="Basket ball         \n \n ", font=title_font, width=0, height=0)
label1_2.grid(row=0, column=0)

frame4_2 = tkinter.Frame(frame1_2, relief="solid", bd=2, width=900, height=50)
frame4_2.place(x=50, y=52.5)

label5_2 = tkinter.Label(frame4_2, text="                      Ball in:", font=normal_font, height=2, bg="white")
label5_2.grid(row=0, column=0)

bb_in = 0

def basketball_in():
    global bb_in
    ball_in_text_2 = "            {0:03d}           EA".format(bb_in)  # {}안에는 숫자 자리수 표현
    label6_2 = tkinter.Label(frame4_2, text=ball_in_text_2, font=normal_font, height=2, bg="white", fg="red")
    label6_2.grid(row=0, column=1)
    frame4_2.after(update_time, basketball_in)


label7_2 = tkinter.Label(frame4_2, text="               Ball out:", font=normal_font, height=2, bg="white")
label7_2.grid(row=0, column=2)

bb_out = 0

def basketball_out():
    global bb_out
    ball_out_text_2 = "             {0:03d}           EA                         ".format(bb_out)  # {}안에는 숫자 자리수 표현
    label8_2 = tkinter.Label(frame4_2, text=ball_out_text_2, font=normal_font, height=2, bg="white", fg="red")
    label8_2.grid(row=0, column=3)
    frame4_2.after(update_time, basketball_out)


label9_2 = tkinter.Label(frame1_2, text=" Productivity", font=title_font, width=13)
label9_2.grid(row=1, column=0)

label10_2 = tkinter.Label(frame1_2, text="                Cycle Time(CT)", font=subtitle_font, width=23, height=1)
label10_2.grid(row=2, column=0)

label11_2 = tkinter.Label(frame1_2, text="", font=subtitle_font, width=6, height=1)  # 여백
label11_2.grid(row=2, column=1)

label12_2 = tkinter.Label(frame1_2, text="Work In Process(WIP)", font=subtitle_font, width=17, height=1)
label12_2.grid(row=2, column=2)

label13_2 = tkinter.Label(frame1_2, text="", font=subtitle_font, width=1, height=1)  # 여백
label13_2.grid(row=2, column=3)

label14_2 = tkinter.Label(frame1_2, text="Throughput(TH)", font=subtitle_font, width=16, height=1)
label14_2.grid(row=2, column=4)

frame5_2 = tkinter.Frame(frame1_2, relief="solid", bd=2, width=165, height=50)
frame5_2.place(x=125, y=209)

frame6_2 = tkinter.Frame(frame1_2, relief="solid", bd=2, width=239, height=50)
frame6_2.place(x=367, y=209)

frame7_2 = tkinter.Frame(frame1_2, relief="solid", bd=2, width=174, height=50)
frame7_2.place(x=607, y=209)

frame8_2 = tkinter.Frame(frame1_2, relief="solid", bd=2)
frame8_2.place(x=50, y=290)

CT_2 = 0
CT_list_2 = []
def cycle_time_2():
    global CT_2
    cycle_time_text_2 = "       {0:06.3f}     sec  ".format(CT_2)  # {}안에는 숫자 자리수 표현
    label12_2 = tkinter.Label(frame5_2, text=cycle_time_text_2, font=normal_font, height=2, bg="white", fg="red")
    label12_2.grid(row=0, column=0)
    CT_list_2.append(CT_2)
    frame5_2.after(update_time, cycle_time_2)


WIP_2 = 0
WIP_list_2 = []

def work_in_process_2():
    global WIP_2
    work_in_process_text_2 = "          {0:02d}        EA  ".format(WIP_2)  # {}안에는 숫자 자리수 표현
    label13_2 = tkinter.Label(frame6_2, text=work_in_process_text_2, font=normal_font, height=2, bg="white", fg="red")
    label13_2.grid(row=0, column=0)
    WIP_list_2.append(WIP_2)
    frame6_2.after(update_time, work_in_process_2)


TH_2 = 0
TH_list_2 = []

def throughput_2():
    global TH_2
    work_in_process_text_2 = "     {0:03.3f}    EA/min ".format(TH_2)  # {}안에는 숫자 자리수 표현
    label14_2 = tkinter.Label(frame7_2, text=work_in_process_text_2, font=normal_font, height=2, bg="white", fg="red")
    label14_2.grid(row=0, column=0)
    TH_list_2.append(TH_2)
    if CT_2 == 0:
        TH_2 == 0
    else:
        TH_2 = WIP_2 / CT_2 * 60
    frame7_2.after(update_time, throughput_2)

t_run_2 = 0
time_list_2 = []
def run_time_2():
    lap_end_time_2 = time.time()
    t_run_2 = lap_end_time_2 - start_time
    time_list_2.append(t_run_2)
    frame5_2.after(update_time, run_time_2)

fig_2 = plt.figure(figsize=(8.8, 6.1))  # figure(도표) 생성 및 크기 조절 (가로, 세로)

min_x_2 = 0
change_x_2 = 0
change_x_22 = 0
max_x_2 = interval1
max_x_22 = interval2

CT_graph_2 = plt.subplot(231, xlim=(min_x_2, max_x_2), ylim=(0, 200))
CT_graph_2.set_title('CT(sec)                                         ')
WIP_graph_2 = plt.subplot(232, xlim=(min_x_2, max_x_2), ylim=(0, WIP_ylim))
WIP_graph_2.set_title('WIP(ea)                                       ')
TH_graph_2 = plt.subplot(233, xlim=(min_x_2, max_x_2), ylim=(0, 25))
TH_graph_2.set_title('TH(ea/min)                                   ')
CT_graph2_2 = plt.subplot(234, xlim=(min_x_2, max_x_22), ylim=(0, 200))
WIP_graph2_2 = plt.subplot(235, xlim=(min_x_2, max_x_22), ylim=(0, WIP_ylim))
WIP_graph2_2.set_xlabel('time(sec)')
TH_graph2_2 = plt.subplot(236, xlim=(min_x_2, max_x_22), ylim=(0, 25))

line_1_2, = CT_graph_2.plot(time_list_2, CT_list_2, lw=2, c='limegreen')  # lw = 선 두께, c = 색상
line_2_2, = WIP_graph_2.plot(time_list_2, WIP_list_2, lw=2, c='violet')
line_3_2, = TH_graph_2.plot(time_list_2, TH_list_2, lw=2, c='dodgerblue')
line_4_2, = CT_graph2_2.plot(time_list_2, CT_list_2, lw=2, c='limegreen')
line_5_2, = WIP_graph2_2.plot(time_list_2, WIP_list_2, lw=2, c='violet')
line_6_2, = TH_graph2_2.plot(time_list_2, TH_list_2, lw=2, c='dodgerblue')


def update_graph_2():
    global line_1_2, line_2_2, line_3_2, line_4_2, line_5_2, line_6_2
    global change_x_2, max_x_2, change_x_22, max_x_22
    global anim_1_2, anim_2_2, anim_3_2, graph_interval

    fig_2 = plt.figure(figsize=(8.8, 6.1))

    change_x_2 += interval1
    max_x_2 += interval1
    if change_x_2 % interval2 == 0:
       change_x_22 += interval2
       max_x_22 += interval2
       time_list_2.clear()
       CT_list_2.clear()
       WIP_list_2.clear()
       TH_list_2.clear()

    CT_graph_2 = plt.subplot(231, xlim=(change_x_2, max_x_2), ylim=(0, 200))
    CT_graph_2.set_title('CT(sec)                                         ')
    WIP_graph_2 = plt.subplot(232, xlim=(change_x_2, max_x_2), ylim=(0, WIP_ylim))
    WIP_graph_2.set_title('WIP(ea)                                       ')
    TH_graph_2 = plt.subplot(233, xlim=(change_x_2, max_x_2), ylim=(0, 25))
    TH_graph_2.set_title('TH(ea/min)                                   ')
    CT_graph2_2 = plt.subplot(234, xlim=(change_x_22, max_x_22), ylim=(0, 200))
    WIP_graph2_2 = plt.subplot(235, xlim=(change_x_22, max_x_22), ylim=(0, WIP_ylim))
    WIP_graph2_2.set_xlabel('time(sec)')
    TH_graph2_2 = plt.subplot(236, xlim=(change_x_22, max_x_22), ylim=(0, 25))

    line_1_2, = CT_graph_2.plot(time_list_2, CT_list_2, lw=2, c='limegreen')  # lw = 선 두께, c = 색상
    line_2_2, = WIP_graph_2.plot(time_list_2, WIP_list_2, lw=2, c='violet')
    line_3_2, = TH_graph_2.plot(time_list_2, TH_list_2, lw=2, c='dodgerblue')
    line_4_2, = CT_graph2_2.plot(time_list_2, CT_list_2, lw=2, c='limegreen')
    line_5_2, = WIP_graph2_2.plot(time_list_2, WIP_list_2, lw=2, c='violet')
    line_6_2, = TH_graph2_2.plot(time_list_2, TH_list_2, lw=2, c='dodgerblue')

    canvas_2 = FigureCanvasTkAgg(fig_2, master=frame8_2)
    canvas_2.get_tk_widget().grid(column=0, row=0)

    anim_1_2 = FuncAnimation(fig_2, update_CT_graph_2, frames=200, interval=graph_interval)
    anim_2_2 = FuncAnimation(fig_2, update_WIP_graph_2, frames=200, interval=graph_interval)
    anim_3_2 = FuncAnimation(fig_2, update_TH_graph_2, frames=200, interval=graph_interval)

    frame8_2.after(interval1*1000, update_graph_2)


def update_CT_graph_2(i):
    line_1_2.set_data(time_list_2, CT_list_2)
    line_4_2.set_data(time_list_2, CT_list_2)


def update_WIP_graph_2(i):
    line_2_2.set_data(time_list_2, WIP_list_2)
    line_5_2.set_data(time_list_2, WIP_list_2)


def update_TH_graph_2(i):
    line_3_2.set_data(time_list_2, TH_list_2)
    line_6_2.set_data(time_list_2, TH_list_2)

frame5_2.after(0, run_time_2)
frame4_2.after(0, basketball_in)
frame4_2.after(0, basketball_out)
frame5_2.after(0, cycle_time_2)
frame6_2.after(0, work_in_process_2)
frame7_2.after(0, throughput_2)
frame8_2.after(interval1*1000, update_graph_2)

canvas_2 = FigureCanvasTkAgg(fig_2, master=frame8_2)
canvas_2.get_tk_widget().grid(column=0, row=0)

anim_1_2 = FuncAnimation(fig_2, update_CT_graph_2, frames=200, interval=graph_interval)
anim_2_2 = FuncAnimation(fig_2, update_WIP_graph_2, frames=200, interval=graph_interval)
anim_3_2 = FuncAnimation(fig_2, update_TH_graph_2, frames=200, interval=graph_interval)

########################################################################################################################
# page 3
frame1_3 = tkinter.Frame(window)
notebook.add(frame1_3, text="Soccer ball")

label1_3 = tkinter.Label(frame1_3, text="Soccer ball         \n \n ", font=title_font, width=0, height=0)
label1_3.grid(row=0, column=0)

frame4_3 = tkinter.Frame(frame1_3, relief="solid", bd=2, width=900, height=50)
frame4_3.place(x=50, y=52.5)

label5_3 = tkinter.Label(frame4_3, text="                      Ball in:", font=normal_font, height=2, bg="white")
label5_3.grid(row=0, column=0)

sb_in = 0

def soccerball_in():
    global sb_in
    ball_in_text_3 = "            {0:03d}           EA".format(sb_in)  # {}안에는 숫자 자리수 표현
    label6_3 = tkinter.Label(frame4_3, text=ball_in_text_3, font=normal_font, height=2, bg="white", fg="red")
    label6_3.grid(row=0, column=1)
    frame4_3.after(update_time, soccerball_in)


label7_3 = tkinter.Label(frame4_3, text="               Ball out:", font=normal_font, height=2, bg="white")
label7_3.grid(row=0, column=2)

sb_out = 0

def soccerball_out():
    global sb_out
    ball_out_text_3 = "             {0:03d}           EA                         ".format(sb_out)  # {}안에는 숫자 자리수 표현
    label8_3 = tkinter.Label(frame4_3, text=ball_out_text_3, font=normal_font, height=2, bg="white", fg="red")
    label8_3.grid(row=0, column=3)
    frame4_3.after(update_time, soccerball_out)


label9_3 = tkinter.Label(frame1_3, text=" Productivity", font=title_font, width=13)
label9_3.grid(row=1, column=0)

label10_3 = tkinter.Label(frame1_3, text="                Cycle Time(CT)", font=subtitle_font, width=23, height=1)
label10_3.grid(row=2, column=0)

label11_3 = tkinter.Label(frame1_3, text="", font=subtitle_font, width=6, height=1)  # 여백
label11_3.grid(row=2, column=1)

label12_3 = tkinter.Label(frame1_3, text="Work In Process(WIP)", font=subtitle_font, width=17, height=1)
label12_3.grid(row=2, column=2)

label13_3 = tkinter.Label(frame1_3, text="", font=subtitle_font, width=1, height=1)  # 여백
label13_3.grid(row=2, column=3)

label14_3 = tkinter.Label(frame1_3, text="Throughput(TH)", font=subtitle_font, width=16, height=1)
label14_3.grid(row=2, column=4)

frame5_3 = tkinter.Frame(frame1_3, relief="solid", bd=2, width=165, height=50)
frame5_3.place(x=125, y=209)

frame6_3 = tkinter.Frame(frame1_3, relief="solid", bd=2, width=239, height=50)
frame6_3.place(x=367, y=209)

frame7_3 = tkinter.Frame(frame1_3, relief="solid", bd=2, width=174, height=50)
frame7_3.place(x=607, y=209)

frame8_3 = tkinter.Frame(frame1_3, relief="solid", bd=2)
frame8_3.place(x=50, y=290)

CT_3 = 0
CT_list_3 = []

def cycle_time_3():
    global CT_3
    cycle_time_text_3 = "       {0:06.3f}     sec  ".format(CT_3)  # {}안에는 숫자 자리수 표현
    label12_3 = tkinter.Label(frame5_3, text=cycle_time_text_3, font=normal_font, height=2, bg="white", fg="red")
    label12_3.grid(row=0, column=0)
    CT_list_3.append(CT_3)
    frame5_3.after(update_time, cycle_time_3)


WIP_3 = 0
WIP_list_3 = []

def work_in_process_3():
    global WIP_3
    work_in_process_text_3 = "          {0:02d}        EA  ".format(WIP_3)  # {}안에는 숫자 자리수 표현
    label13_3 = tkinter.Label(frame6_3, text=work_in_process_text_3, font=normal_font, height=2, bg="white", fg="red")
    label13_3.grid(row=0, column=0)
    WIP_list_3.append(WIP_3)
    frame6_3.after(update_time, work_in_process_3)


TH_3 = 0
TH_list_3 = []

def throughput_3():
    global TH_3
    work_in_process_text_3 = "     {0:03.3f}    EA/min ".format(TH_3)  # {}안에는 숫자 자리수 표현
    label14_3 = tkinter.Label(frame7_3, text=work_in_process_text_3, font=normal_font, height=2, bg="white", fg="red")
    label14_3.grid(row=0, column=0)
    TH_list_3.append(TH_3)
    if CT_3 == 0:
        TH_3 == 0
    else:
        TH_3 = WIP_3 / CT_3 * 60
    frame7_3.after(update_time, throughput_3)

t_run_3 = 0
time_list_3 = []

def run_time_3():
    lap_end_time_3 = time.time()
    t_run_3 = lap_end_time_3 - start_time
    time_list_3.append(t_run_3)
    frame5_3.after(update_time, run_time_3)


fig_3 = plt.figure(figsize=(8.8, 6.1))  # figure(도표) 생성 및 크기 조절 (가로, 세로)

min_x_3 = 0
change_x_3 = 0
change_x_32 = 0
max_x_3 = 100
max_x_32 = 100

CT_graph_3 = plt.subplot(231, xlim=(min_x_3, max_x_3), ylim=(0, 200))
CT_graph_3.set_title('CT(sec)                                         ')
WIP_graph_3 = plt.subplot(232, xlim=(min_x_3, max_x_3), ylim=(0, WIP_ylim))
WIP_graph_3.set_title('WIP(ea)                                       ')
TH_graph_3 = plt.subplot(233, xlim=(min_x_3, max_x_3), ylim=(0, 25))
TH_graph_3.set_title('TH(ea/min)                                   ')
CT_graph2_3 = plt.subplot(234, xlim=(min_x_3, max_x_32), ylim=(0, 200))
WIP_graph2_3 = plt.subplot(235, xlim=(min_x_3, max_x_32), ylim=(0, WIP_ylim))
WIP_graph2_3.set_xlabel('time(sec)')
TH_graph2_3 = plt.subplot(236, xlim=(min_x_3, max_x_32), ylim=(0, 25))

line_1_3, = CT_graph_3.plot(time_list_3, CT_list_3, lw=2, c='limegreen')  # lw = 선 두께, c = 색상
line_2_3, = WIP_graph_3.plot(time_list_3, WIP_list_3, lw=2, c='violet')
line_3_3, = TH_graph_3.plot(time_list_3, TH_list_3, lw=2, c='dodgerblue')
line_4_3, = CT_graph2_3.plot(time_list_3, CT_list_3, lw=2, c='limegreen')
line_5_3, = WIP_graph2_3.plot(time_list_3, WIP_list_3, lw=2, c='violet')
line_6_3, = TH_graph2_3.plot(time_list_3, TH_list_3, lw=2, c='dodgerblue')


def update_graph_3():
    global line_1_3, line_2_3, line_3_3, line_4_3, line_5_3, line_6_3
    global change_x_3, max_x_3, change_x_32, max_x_32
    global anim_1_3, anim_2_3, anim_3_3, graph_interval

    fig_3 = plt.figure(figsize=(8.8, 6.1))

    change_x_3 += interval1
    max_x_3 += interval1
    if change_x_3 % interval2 == 0:
       change_x_32 += interval2
       max_x_32 += interval2
       time_list_3.clear()
       CT_list_3.clear()
       WIP_list_3.clear()
       TH_list_3.clear()

    CT_graph_3 = plt.subplot(231, xlim=(change_x_3, max_x_3), ylim=(0, 200))
    CT_graph_3.set_title('CT(sec)                                         ')
    WIP_graph_3 = plt.subplot(232, xlim=(change_x_3, max_x_3), ylim=(0, WIP_ylim))
    WIP_graph_3.set_title('WIP(ea)                                       ')
    TH_graph_3 = plt.subplot(233, xlim=(change_x_3, max_x_3), ylim=(0, 25))
    TH_graph_3.set_title('TH(ea/min)                                   ')
    CT_graph2_3 = plt.subplot(234, xlim=(change_x_32, max_x_32), ylim=(0, 200))
    WIP_graph2_3 = plt.subplot(235, xlim=(change_x_32, max_x_32), ylim=(0, WIP_ylim))
    WIP_graph2_3.set_xlabel('time(sec)')
    TH_graph2_3 = plt.subplot(236, xlim=(change_x_32, max_x_32), ylim=(0, 25))

    line_1_3, = CT_graph_3.plot(time_list_3, CT_list_3, lw=2, c='limegreen')  # lw = 선 두께, c = 색상
    line_2_3, = WIP_graph_3.plot(time_list_3, WIP_list_3, lw=2, c='violet')
    line_3_3, = TH_graph_3.plot(time_list_3, TH_list_3, lw=2, c='dodgerblue')
    line_4_3, = CT_graph2_3.plot(time_list_3, CT_list_3, lw=2, c='limegreen')
    line_5_3, = WIP_graph2_3.plot(time_list_3, WIP_list_3, lw=2, c='violet')
    line_6_3, = TH_graph2_3.plot(time_list_3, TH_list_3, lw=2, c='dodgerblue')

    canvas_3 = FigureCanvasTkAgg(fig_3, master=frame8_3)
    canvas_3.get_tk_widget().grid(column=0, row=0)

    anim_1_3 = FuncAnimation(fig_3, update_CT_graph_3, frames=200, interval=graph_interval)
    anim_2_3 = FuncAnimation(fig_3, update_WIP_graph_3, frames=200, interval=graph_interval)
    anim_3_3 = FuncAnimation(fig_3, update_TH_graph_3, frames=200, interval=graph_interval)

    frame8_3.after(interval1*1000, update_graph_3)


def update_CT_graph_3(i):
    line_1_3.set_data(time_list_3, CT_list_3)
    line_4_3.set_data(time_list_3, CT_list_3)


def update_WIP_graph_3(i):
    line_2_3.set_data(time_list_3, WIP_list_3)
    line_5_3.set_data(time_list_3, WIP_list_3)


def update_TH_graph_3(i):
    line_3_3.set_data(time_list_3, TH_list_3)
    line_6_3.set_data(time_list_3, TH_list_3)

frame5_3.after(0, run_time_3)
frame4_3.after(0, soccerball_in)
frame4_3.after(0, soccerball_out)
frame5_3.after(0, cycle_time_3)
frame6_3.after(0, work_in_process_3)
frame7_3.after(0, throughput_3)
frame8_3.after(interval1*1000, update_graph_3)

canvas_3 = FigureCanvasTkAgg(fig_3, master=frame8_3)
canvas_3.get_tk_widget().grid(column=0, row=0)

anim_1_3 = FuncAnimation(fig_3, update_CT_graph_3, frames=200, interval=graph_interval)
anim_2_3 = FuncAnimation(fig_3, update_WIP_graph_3, frames=200, interval=graph_interval)
anim_3_3 = FuncAnimation(fig_3, update_TH_graph_3, frames=200, interval=graph_interval)

window.mainloop()
client_socket.close()
server_socket.close()
