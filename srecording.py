import pyautogui
import os
import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
import threading
import time


recording = False


def record_screen(filename, save_path):
    global recording
    recording = True
    frame_count = 0
    frame_rate = 3  
    resolution = (1280, 720)  
    fourcc = cv2.VideoWriter_fourcc(*'VP90')
    out = cv2.VideoWriter(os.path.join(save_path, f"{filename}.webm"), fourcc, frame_rate, resolution)

    while recording:
        img = pyautogui.screenshot(region=(0, 0, resolution[0], resolution[1]))  # Capture screenshot at specified resolution
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)  
        frame_count += 1
        time.sleep(1 / frame_rate)  

    out.release()
    print("Recording saved successfully.")


def stop_recording():
    global recording
    recording = False


def start_recording():
    filename = filename_entry.get()
    save_path = path_entry.get()
    threading.Thread(target=record_screen, args=(filename, save_path), daemon=True).start()


def choose_save_path():
    save_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, save_path)


def main():
    global filename_entry, path_entry, start_stop_button

   
    root = tk.Tk()
    root.title("Screen Recorder")


    filename_label = tk.Label(root, text="Filename:")
    filename_label.grid(row=0, column=0, padx=5, pady=5)
    filename_entry = tk.Entry(root)
    filename_entry.grid(row=0, column=1, padx=5, pady=5)

   
    path_label = tk.Label(root, text="Save Path:")
    path_label.grid(row=1, column=0, padx=5, pady=5)
    path_entry = tk.Entry(root)
    path_entry.grid(row=1, column=1, padx=5, pady=5)
    path_button = tk.Button(root, text="Choose Path", command=choose_save_path)
    path_button.grid(row=1, column=2, padx=5, pady=5)

    start_button = tk.Button(root, text="Start Recording", command=start_recording)
    start_button.grid(row=2, column=0, padx=5, pady=5)

   
    stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
    stop_button.grid(row=2, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
