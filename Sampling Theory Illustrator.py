from matplotlib import axes, cbook
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import matplotlib
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import os
from matplotlib.widgets import Slider
import time
from tkinter import ttk
import tkinter as tk 
import numpy.fft as fft
import scipy
from scipy.interpolate import interp1d
from matplotlib import gridspec
from scipy import signal
import tkinter.font as font

root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab1.grid(row=0, column=0, sticky="nsew")
tab2 = ttk.Frame(tabControl)
Grid.rowconfigure(tab1, 0, weight=1)
Grid.rowconfigure(tab2, 0, weight=1)
Grid.columnconfigure(tab1, 0, weight=1)
Grid.columnconfigure(tab2, 0, weight=1)
tabControl.add(tab1, text ='Signal sampler')
tabControl.add(tab2, text ='Signal composer')
tabControl.grid(row=0, column=0, columnspan=6, sticky=N+S+W+E)


#Variables declarations
  
w = 2. * np.pi * 1
amplitude=20
phase_shift=0
time_interval=1
samples=1000
summation=0
list1=["select sinusoidal"]
list2=["select sinusoidal"]
y=0
t = np.linspace(0, time_interval, samples)
visible = True

sinusoidal1 = np.sin((w* 2 *t)-phase_shift ) * amplitude
sinusoidal2 = np.sin((w *6 *t)-phase_shift ) * amplitude
sinusoidal3 = np.sin((w *t)- 0.5*np.pi ) * 25
sinusoidal4 = np.sin((w *3 *t)-np.pi ) * 30
sinusoidal5 = np.sin((w *4 *t)-phase_shift ) * 15
sinusoidal6 = np.sin((w *8 *t)- np.pi ) * 40



#Creating plots & adding labels

fig = plt.figure(figsize=(10, 6))
left, width = 0.1, 0.8
rect1 = [left, 0.65, width, 0.25]  # left, bottom, width, height
rect2 = [left, 0.4, width, 0.25]

ax1 = fig.add_axes(rect1) 
ax2 = fig.add_axes(rect2, sharex=ax1)

ax1.set_xlabel("time")
ax1.set_ylabel("amplitude")
ax2.set_xlabel("time")
ax2.set_ylabel("frequency")

fig2= plt.figure(figsize=(10,6))

gs = gridspec.GridSpec(2, 1, height_ratios=[5,5])
gs2 = gridspec.GridSpec(1, 1, height_ratios=[5])

ax3 = fig2.add_subplot(gs[0])
ax4 = fig2.add_subplot(gs[1], sharex=ax1)

visible = True

#* Sliders **

frequencySlider = Scale(tab2, from_= 1, to=100, tickinterval=9,orient=HORIZONTAL,length=500,label="frequancy")
frequencySlider.grid(row=0, column=0, sticky="nsew")
tab2.grid_rowconfigure(0, weight=1)

phase_shiftSlider = Scale(tab2, from_= 0, to=2*np.pi, tickinterval=(0.5*np.pi),orient=HORIZONTAL,length=500,label="phase shift")
phase_shiftSlider.grid(row=1, column=0, sticky="nsew")
tab2.grid_rowconfigure(1, weight=1)

amplitudeSlider = Scale(tab2, from_= 1, to=50, tickinterval=1,orient=HORIZONTAL,length=500,label="amplitude")
amplitudeSlider.grid(row=2, column=0, sticky="nsew")
tab2.grid_rowconfigure(2, weight=1)

freqInput = Scale(tab1, from_=0, to=3, tickinterval=1,orient=HORIZONTAL,length=200)
freqInput.grid(row=0, column=0, sticky="NSEW")
tab1.grid_rowconfigure(0, weight=1)

tab2.grid_columnconfigure(0, weight=1)
tab1.grid_columnconfigure(0, weight=1)

#* Functions **

def changes():
    global w
    global phase_shift
    global amplitude
    w = 2*np.pi*frequencySlider.get()
    phase_shift = phase_shiftSlider.get()
    amplitude = amplitudeSlider.get()
    sine_wave()
    


def sine_wave():
    global w
    global phase_shift
    global amplitude
    global y
    global t
    y = np.sin((w * t)-phase_shift ) * amplitude
    ax1.cla()
    ax1.plot(t, y)
    ax1.set_xlim(0,max(t))
    ax1.set_ylim(-max(y)-1,max(y)+1)
    fig.canvas.draw_idle()

sine_wave()


def addToSum():
    global summation
    global t
    global list1
    global list2
    list1.append(y)
    list2.append(str(amplitude) + " sin " + str(w) + "t + " + str(phase_shift))
    #update drop menu
    dropupdater()
    plotting()

def plotting():
    global summation
    summation = sum(list1[1:])

    sine_wave()
    ax2.cla()
    ax2.plot(t,summation)
    ax2.set_xlim(0,max(t))
    ax2.set_ylim(-max(summation)-1,max(summation)+1)
    fig.canvas.draw_idle()

def dropupdater():
    question_menu['menu'].delete(0, "end")
    for item in list2:
        question_menu['menu'].add_command(
            label=item,
            command=lambda value=item: value_inside.set(value)
        )



def my_remove_sel():
    z=list2.index(value_inside.get())
    list1.pop(z)
    list2.pop(z)
    r_index=question_menu['menu'].index(value_inside.get())
    question_menu['menu'].delete(r_index)
    value_inside.set(question_menu['menu'].entrycget(0,"label")) # select the first one 
    dropupdater()
    plotting()
    




def first_sin(y1, y2):
    global w
    global phase_shift
    global amplitude
    global y
    global t
    global summation
    summation=y1+y2
    ax3.cla()
    ax3.plot(t, summation)
    ax3.set_ylim(-max(summation)-1,max(summation)+1)
    fig2.canvas.draw_idle()

def toggle_ax4():
    global visible
    visible = not visible
    ax4.set_visible(visible)
    if visible:
        ax3.set_position(gs[0].get_position(fig2))
        ax4.set_position(gs[1].get_position(fig2))
    else:
        ax3.set_position(gs2[0].get_position(fig2))
    plt.draw()
    


def getMax():
    global maxFreq
    spec = fft.fft(summation)
    freqs = fft.fftfreq(len(spec))
    threshold = 0.5 * max(abs(spec))
    mask = abs(spec) > threshold
    peaks = freqs[mask]
    peaks = abs(peaks)
    maxFreq = max(peaks *100*100)

def sample(freq):
    if freq==0:
        ax3.cla()
        ax4.cla()
        canvas.draw()

    ax3.cla()
    ax4.cla()
    sampledFreq=int(freq*maxFreq)
    f = signal.resample(summation, sampledFreq)
    xnew = np.linspace(0, time_interval, sampledFreq, endpoint=False)
    ax3.set_xlim(0,max(t))
    ax3.set_ylim(-max(summation)-1,max(summation)+1)
    ax4.set_xlim(0,max(t))
    ax4.set_ylim(-max(summation)-1,max(summation)+1)
    ax3.plot(t, summation, '-', xnew, f, '.')
    ax3.legend(['data', 'resampled'], loc='best')

    f2 = interp1d(xnew, f, kind='cubic',bounds_error=False)
    recoverData= np.linspace(0, time_interval, samples , endpoint=True)
    ax4.plot( recoverData, f2(recoverData))

def addFreq():
    freqNum=freqInput.get()
    getMax()
    sample(freqNum)
    canvas.draw()

def moveGraph():

    ax3.cla()
    ax4.cla()
    ax3.plot(t,summation)
    ax3.set_xlim(0,max(t))
    ax3.set_ylim(-max(summation)-1,max(summation)+1)
    ax4.set_xlim(0,max(t))
    ax4.set_ylim(-max(summation)-1,max(summation)+1)
    fig2.canvas.draw_idle()

#* Menus, dropdown menus and buttons***

my_menu = Menu(tab2)
signal_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="choose signal",menu=signal_menu)
signal_menu.add_command(label="First wave",command=lambda: first_sin(sinusoidal1, sinusoidal2))
signal_menu.add_command(label="Second wave",command=lambda: first_sin(sinusoidal3, sinusoidal5))
signal_menu.add_command(label="Third wave",command=lambda: first_sin(sinusoidal4, sinusoidal6))
signal_menu.add_command(label="Fourth wave",command=lambda: first_sin(sinusoidal2, sinusoidal4))

Grid.columnconfigure(root,0,weight=1)

Grid.rowconfigure(tab2,4,weight=1)
Grid.rowconfigure(tab2, 5, weight=1)
Grid.rowconfigure(tab2, 6, weight=1)

Grid.rowconfigure(tab1, 1, weight=1)
Grid.rowconfigure(tab1, 2, weight=1)



myFont = font.Font( size=15)

buttonDelete = tk.Button(tab2,  text='Remove Selectd', command=lambda: my_remove_sel())  
buttonDelete.grid(row=3, column=0, sticky="nsew",padx=600)

changesButton=tkinter.Button(master=tab2, text='apply changes', command=changes)
changesButton.grid(row=4,column=0, sticky="nsew",padx=600)

addSumButton = tkinter.Button(master=tab2, text='Add sinusoidal to summation', command= addToSum)
addSumButton.grid(row=5, column=0, sticky="nsew",padx=600)

buttonMove = tkinter.Button(master=tab2, text="move to sampler " ,command=moveGraph)
buttonMove.grid(row=6, column=0, sticky="nsew",padx=600)

buttonFreq=tkinter.Button(master=tab1, text='apply fmax', command=addFreq)
buttonFreq.grid(row=1, column=0, sticky="nsew",padx=600)


buttonClose = tkinter.Button(master=tab1, text="open/close secondary graph " ,command=toggle_ax4)
buttonClose.grid(row=2, column=0, sticky="nsew",padx=600)



buttonClose['font'] = myFont
buttonFreq['font'] = myFont
buttonClose['font'] = myFont
addSumButton['font'] = myFont
changesButton['font'] = myFont
buttonMove['font'] = myFont
buttonDelete['font'] = myFont


# Variable to keep track of the option
# selected in OptionMenu
value_inside = tkinter.StringVar(root)
  
# Set the default value of the variable
value_inside.set(list2[0])

# Create the optionmenu widget and passing 
# the options_list and value_inside to it.
question_menu = tkinter.OptionMenu(tab2, value_inside, *list2)
question_menu.grid(row=7,column=0,pady=5)
Grid.rowconfigure(tab2, 7, weight=1)
question_menu['font']=myFont


Grid.rowconfigure(tab1, 3, weight=1)
Grid.rowconfigure(tab2, 8, weight=1)

canvas = FigureCanvasTkAgg(fig, master=tab2)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(row=8, column=0, sticky="nsew")

canvas = FigureCanvasTkAgg(fig2, master=tab1)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(row=3, column=0, sticky="nsew",pady=50)

root.config(menu=my_menu)  
tkinter.mainloop()
