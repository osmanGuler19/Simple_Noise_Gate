import tkinter  as tk
from multiprocessing.queues import Queue
from tkinter import messagebox
from functools import partial
import pyaudio
import wave
from PIL import Image, ImageTk
import time
import sys
import subprocess
import numpy as np
import sounddevice as sd
import logging
import threading
import trace
import WorkerClass
import multiprocessing
from multiprocessing import Queue
from typing import List, Any
import audioop


"""-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"""
frames = []
global frames2
frames2 = []

is_on = False
q = Queue()
q2 = Queue()
q2.put(True)
q3 = Queue()
q3.put(True)
def main():

    def proc_start():
        p_to_start = multiprocessing.Process(target=Worker.NoiseGate,args=(q,q3))
        p_to_start.start()
        return p_to_start

    def proc_stop(p_to_stop):
        p_to_stop.terminate()
        print
        "after Termination "

    def get_it(q,myframe):
        while not q.empty():
            item = q.get()
            myframe.append(item)


    def Record(myframes):
        print(len(myframes))
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        p = pyaudio.PyAudio()
        wf = wave.open("output.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(myframes))
        wf.close()

    Worker = WorkerClass
    is_gate_on = True
    root = tk.Tk();
    canvas = tk.Canvas(root, width=400, height=200)
    my_label = tk.Label(root,
                        text="Noise gate is Off",
                        fg="Grey",
                        font=("Helvetica", 32))

    my_label.pack(pady=20)


    def switch():
        global is_on
        global p
        if is_on:
            on_button.config(image=off)
            my_label.configure(text="Noise gate is Off", fg="Grey")
            is_on = False
            print("false yapılacak")
            q3.put(False)
            time.sleep(0.5)
            print("false yapıldı")
            get_it(q,frames)
            time.sleep(2)
            proc_stop(p)
            Record(frames)
            print("Bu aşama geçildi")
            z = p.is_alive()
            print("is alive : ",z)

        else:
            is_on = True
            p = proc_start()
            print("isAlive : ", p.is_alive())
            on_button.config(image=on)
            my_label.configure(text="Noise gate is On", fg="Green")
            """p2 = proc_start2()"""


    on = tk.PhotoImage(file="on.png")
    off = tk.PhotoImage(file="off.png")

    on_button = tk.Button(root, image=off, bd=0,
                          command=partial(switch))

    on_button.pack(pady=50)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if is_on:
                p.terminate()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()


def getFrames():
    return frames



"""def switch(is_gate_on):
    global is_on
    global x
    if(not is_on):
        x = threading.Thread(target=WorkerClass.NoiseGate(), args=(1,), daemon=True)
    if is_on:
        on_button.config(image=off)
        my_label.configure(text="Noise gate is Off", fg="Grey")
        is_on = False
        is_gate_on = True;
        print(x.name)
        print(is_gate_on)

        z = x.is_alive()
        print("alive : ",z)
        x.join()
    else:
        on_button.config(image=on)
        my_label.configure(text="Noise gate is On", fg="Green")
        is_on = True
        is_gate_on =False
        print(is_gate_on)
        x.start()
        z = x.is_alive()
        print("alive : ",z)

"""

"""def print_sound(indata, outdata, frames, time, status):
    np.linalg
    volume_norm = np.linalg.norm(indata)*10
    print ("|" * int(volume_norm))

with sd.Stream(callback=print_sound):
    sd.sleep(10000)"""

"""p1 = multiprocessing.Process(target=Worker.NoiseGate, args=(is_gate_on,))"""
