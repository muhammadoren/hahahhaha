import socket
import threading
from datetime import datetime
import requests

# ⚠️ Basic known vulnerable banners
vulnerable_banners = {
    "vsFTPd 2.3.4": "Backdoor vulnerability (CVE-2011-2523)",
    "Apache httpd 2.4.49": "Path traversal (CVE-2021-41773)",
    "OpenSSH 7.2p2": "User enumeration (CVE-2016-6210)"
    "CVE-2023-48795"
    "CVE-2025-32728"
    "CVE-2013-5918"
    "CVE-2012-0896"
    "CVE-2022-3590"
    "CVE-2012-2759"
    "CVE-2008-6811"
    "CVE-2011-4669"
    "CVE-2011-3854"
    "CVE-2012-2913"
    "CVE-2008-4732"
    "CVE-2011-0740"
    "CVE-2009-2396"
    "CVE-2019-6110"
    "CVE-2009-3703"
    "CVE-2020-15778"
    "CVE-2020-14145"
    "CVE-2012-1067"
    "CVE-2009-2852"
    "CVE-2012-1786"
    "CVE-2010-4637"
    "CVE-2019-6111"
    "CVE-2011-3981"
    "CVE-2010-4277"
    "CVE-2007-2768"
    "CVE-2009-4168"
    "CVE-2012-0895"
    "CVE-2009-2144"
    "CVE-2011-3860"
    "CVE-2011-4568"
    "CVE-2011-0759"
    "CVE-2011-3858"
    "CVE-2011-0641"
    "CVE-2011-0760"
    "CVE-2023-51767"
    "CVE-2010-4518"
    "CVE-2008-5752"
    "CVE-2023-38408"
    "CVE-2009-4170"
    "CVE-2008-4625"
    "CVE-2008-7175"
    "CVE-2023-22622"
    "CVE-2012-2920"
    "CVE-2010-1186"
    "CVE-2011-3856"
    "CVE-2023-39999"
    "CVE-2008-1982"
    "CVE-2009-4672"
    "CVE-2009-4169"
    "CVE-2010-4403"
    "CVE-2011-3862"
    "CVE-2012-2912"
    "CVE-2007-5800"
    "CVE-2011-4562"
    "CVE-2011-1047"
    "CVE-2012-1068"
    "CVE-2010-4825"
    "CVE-2025-26465"
    "CVE-2011-3851"
    "CVE-2017-15906"
    "CVE-2011-3864"
    "CVE-2023-38000"
    "CVE-2010-4839"
    "CVE-2011-1669"
    "CVE-2023-51385"
    "CVE-2008-4733"
    "CVE-2011-3865"
    "CVE-2018-20685"
    "CVE-2011-3852"
    "CVE-2010-4747"
    "CVE-2011-3857"
    "CVE-2010-2924"
    "CVE-2009-2122"
    "CVE-2011-3853"
    "CVE-2023-2745"
    "CVE-2011-5051"
    "CVE-2011-3863"
    "CVE-2019-6109"
    "CVE-2010-3977"
    "CVE-2018-15919"
    "CVE-2010-4630"
    "CVE-2009-4424"
    "CVE-2011-4671"
    "CVE-2011-3850"
    "CVE-2012-1010"
    "CVE-2012-0898"
    "CVE-2010-4779"
    "CVE-2009-2383"
    "CVE-2008-7040"
    "CVE-2011-3855"
    "CVE-2011-4673"
    "CVE-2007-2627"
    "CVE-2012-1785"
    "CVE-2011-3861"
    "CVE-2009-2143"
    "CVE-2011-5082"
    "CVE-2012-1205"
    "CVE-2009-4748"
    "CVE-2012-0934"
    "CVE-2011-3859"
    "CVE-2008-4734"
    "CVE-2011-4803"
    "CVE-2021-41617"
    "CVE-2021-36368"
    "CVE-2010-4875"
    "CVE-2016-20012"
    "CVE-2012-2916"
    "CVE-2009-0968"
    "CVE-2008-3844"
    "CVE-2010-0673"
    "CVE-2012-2917"
    "CVE-2011-4646"
    "CVE-2012-1011"
    "CVE-2023-5561"
    "CVE-2018-15473"
}

# Common SQLi payloads
sqli_payloads = [
    "' OR '1'='1",
    "' OR 1=1--",
    "\" OR \"1\"=\"1",
    "' OR '1'='1' -- ",
    "') OR ('1'='1"
]

# SQL error messages to detect
sql_errors = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "odbc microsoft access driver",
    "sqlite error",
    "unknown column"
]

print("""
╔═╗╦ ╦╦╦  ╦╔═╗╔═╗╦╔╗╔╔═╗  ╔═╗╦ ╦╔╗ ╔═╗╦═╗  ╔╦╗╔═╗╔═╗╦╔═╗
╠═╝╠═╣║║  ║╠═╝╠═╝║║║║║╣   ║  ╚╦╝╠╩╗║╣ ╠╦╝  ║║║╠═╣╠╣ ║╠═╣
╩  ╩ ╩╩╩═╝╩╩  ╩  ╩╝╚╝╚═╝  ╚═╝ ╩ ╚═╝╚═╝╩╚═  ╩ ╩╩ ╩╚  ╩╩ ╩
""")

# User Input
target = input("Enter IP or hostname: ")
start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))
save = input("Save report to file? (y/n): ").lower() == 'y'

# Resolve IP
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("[ERROR] Hostname could not be resolved.")
    exit()

print(f"\n[INFO] Scanning {target} ({target_ip}) from port {start_port} to {end_port}")
print("[INFO] Time started:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("-" * 50)

open_ports = []
vuln_results = []
web_ports = []

# Port Scanner + Banner Grabbing + Vulnerability Match
def scan_port(port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            banner = ""
            try:
                s.send(b'HEAD / HTTP/1.1\r\n\r\n')
                banner = s.recv(1024).decode(errors="ignore").strip()
            except:
                pass
            print(f"[OPEN] Port {port}")
            if banner:
                print(f" └─ Banner: {banner[:60]}")
                for vuln_banner, vuln_info in vulnerable_banners.items():
                    if vuln_banner in banner:
                        print(f" ⚠️ [VULNERABLE] {vuln_banner} — {vuln_info}")
                        vuln_results.append((port, vuln_banner, vuln_info))
            open_ports.append((port, banner))
            if port in [80, 443, 8080, 8000]:
                web_ports.append(port)
        s.close()
    except:
        pass

# Threaded Scan
threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n[INFO] Scan completed.")
print("-" * 50)
if not open_ports:
    print("[RESULT] No open ports found.")
else:
    print(f"[RESULT] Found {len(open_ports)} open ports.")

if vuln_results:
    print("\n[!] Possible Vulnerabilities:")
    for port, banner, info in vuln_results:
        print(f"- Port {port}: {banner} — {info}")
else:
    print("\n[✓] No known vulnerable banners detected.")

# Optional SQLi Scan if web port is open
sqli_findings = []
if web_ports:
    print("\n[+] Web service detected on port(s):", web_ports)
    test_url = input("Enter full test URL with parameter (e.g., http://target/page.php?id=1):\n> ")
    print("[INFO] Starting SQL Injection test...")

    for payload in sqli_payloads:
        try:
            url_with_payload = test_url + payload
            response = requests.get(url_with_payload, timeout=5)
            content = response.text.lower()

            if any(error in content for error in sql_errors):
                print(f"⚠️ [SQLi VULNERABLE] Detected with payload: {payload}")
                sqli_findings.append((payload, url_with_payload))
                break
            else:
                print(f"[-] Tested payload: {payload}")
        except:
            print("[ERROR] Could not connect for SQLi test.")
            break

    if not sqli_findings:
        print("[✓] No SQL Injection vulnerability found on that URL.")

# Save report
if save:
    filename = f"scan_report_{target.replace('.', '_')}.txt"
    with open(filename, "w") as f:
        f.write(f"Scan report for {target} ({target_ip})\n")
        f.write(f"Ports scanned: {start_port} - {end_port}\n\n")
        for port, banner in open_ports:
            f.write(f"[OPEN] Port {port}\n")
            if banner:
                f.write(f" └─ Banner: {banner}\n")
        if vuln_results:
            f.write("\n[!] Possible Vulnerabilities:\n")
            for port, banner, info in vuln_results:
                f.write(f"- Port {port}: {banner} — {info}\n")
        if sqli_findings:
            f.write("\n[!] SQL Injection Detected:\n")
            for payload, url in sqli_findings:
                f.write(f"- Payload: {payload}\n  URL: {url}\n")
    print(f"\n[SAVED] Scan report saved as {filename}")
