import tkinter as tk
from tkinter import ttk, filedialog
import psutil
import time
import threading
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

running = False
log_data = []

def monitor_network():
    global running, log_data
    old_stats = psutil.net_io_counters()
    while running:
        time.sleep(1)
        new_stats = psutil.net_io_counters()
        upload = new_stats.bytes_sent - old_stats.bytes_sent
        download = new_stats.bytes_recv - old_stats.bytes_recv
        old_stats = new_stats

        timestamp = datetime.now().strftime("%H:%M:%S")
        log_data.append((timestamp, upload, download))

        upload_label.config(text=f"Upload: {upload:.2f} B/s")
        download_label.config(text=f"Download: {download:.2f} B/s")

        if upload > 100000 or download > 100000:
            alert_label.config(text="⚠️ High network usage", foreground="red")
        else:
            alert_label.config(text="✅ Normal", foreground="green")

        update_plot()

def start_monitoring():
    global running
    if not running:
        running = True
        threading.Thread(target=monitor_network, daemon=True).start()

def stop_monitoring():
    global running
    running = False

def save_logs():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Upload (B/s)", "Download (B/s)"])
            writer.writerows(log_data)

def update_plot():
    if len(log_data) > 20:
        display_data = log_data[-20:]
    else:
        display_data = log_data

    timestamps = [row[0] for row in display_data]
    uploads = [row[1] for row in display_data]
    downloads = [row[2] for row in display_data]

    ax.clear()
    ax.plot(timestamps, uploads, label='Upload', color='blue')
    ax.plot(timestamps, downloads, label='Download', color='green')
    ax.set_title("Network Usage (Last 20 sec)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Bytes per second")
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    canvas.draw()

# GUI Setup
root = tk.Tk()
root.title("Network Monitor with Chart")

upload_label = ttk.Label(root, text="Upload: 0 B/s", font=("Arial", 12))
upload_label.pack(pady=5)

download_label = ttk.Label(root, text="Download: 0 B/s", font=("Arial", 12))
download_label.pack(pady=5)

alert_label = ttk.Label(root, text="Status: ✅ Normal", font=("Arial", 12))
alert_label.pack(pady=10)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Start", command=start_monitoring).pack(side=tk.LEFT, padx=10)
ttk.Button(button_frame, text="Stop", command=stop_monitoring).pack(side=tk.LEFT, padx=10)
ttk.Button(button_frame, text="Save Logs", command=save_logs).pack(side=tk.LEFT, padx=10)

# Matplotlib Chart
fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

root.mainloop()
