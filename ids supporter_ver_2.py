import threading
import socket
import json
from datetime import datetime

def log_event(attacker_ip, port_number):
    event_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"),
        "attacker_ip": attacker_ip,
        "target_port": port_number,
        "status": "Incursion Detected"
    }

    with open("ids_log.json", "a") as f:
        f.write(json.dumps(event_data) + "\n")

def watch_doors(port_number):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port_number))
    s.listen(1)
    print(f"[*] Background scan started for port: {port_number}")

    while True:
        client, addr = s.accept()
        attacker_ip = addr[0]
    
        print(f"[!!!] ALERT: Port {port_number} was probed by {attacker_ip}")
       
        log_event(attacker_ip, port_number)

        client.close()

def list_doors():
    doors = [8080, 8888, 9999, 9090, 4444, 21]
    for port in doors:
        worker = threading.Thread(target=watch_doors, args=(port,))
        worker.daemon = True
        worker.start()
if __name__ == "__main__":
    list_doors()
    print("[+] IDS v2.0 is live and logging to JSON...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[!] Shutting down IDS...")
