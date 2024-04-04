import pyautogui
import os
import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
import threading
import time

# Global variables
recording = False

# Function to record the screen by saving frames as images and then convert to WebM
def record_screen(filename, save_path):
    global recording
    recording = True
    frame_count = 0
    frame_rate = 3  # Adjust frame rate as needed for slower video
    resolution = (1280, 720)  # Adjust resolution as needed
    fourcc = cv2.VideoWriter_fourcc(*'VP90')
    out = cv2.VideoWriter(os.path.join(save_path, f"{filename}.webm"), fourcc, frame_rate, resolution)

    while recording:
        img = pyautogui.screenshot(region=(0, 0, resolution[0], resolution[1]))  # Capture screenshot at specified resolution
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)  # Write frame to video file
        frame_count += 1
        time.sleep(1 / frame_rate)  # Adjust frame rate

    out.release()
    print("Recording saved successfully.")

# Function to stop recording
def stop_recording():
    global recording
    recording = False

# Function to start recording
def start_recording():
    filename = filename_entry.get()
    save_path = path_entry.get()
    threading.Thread(target=record_screen, args=(filename, save_path), daemon=True).start()

# Function to open file dialog and get save path
def choose_save_path():
    save_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, save_path)

# Main function
def main():
    global filename_entry, path_entry, start_stop_button

    # Create GUI window
    root = tk.Tk()
    root.title("Screen Recorder")

    # Label and entry for filename
    filename_label = tk.Label(root, text="Filename:")
    filename_label.grid(row=0, column=0, padx=5, pady=5)
    filename_entry = tk.Entry(root)
    filename_entry.grid(row=0, column=1, padx=5, pady=5)

    # Label and entry for save path
    path_label = tk.Label(root, text="Save Path:")
    path_label.grid(row=1, column=0, padx=5, pady=5)
    path_entry = tk.Entry(root)
    path_entry.grid(row=1, column=1, padx=5, pady=5)
    path_button = tk.Button(root, text="Choose Path", command=choose_save_path)
    path_button.grid(row=1, column=2, padx=5, pady=5)

    # Start button
    start_button = tk.Button(root, text="Start Recording", command=start_recording)
    start_button.grid(row=2, column=0, padx=5, pady=5)

    # Stop button
    stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
    stop_button.grid(row=2, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
