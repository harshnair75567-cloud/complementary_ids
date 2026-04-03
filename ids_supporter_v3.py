import threading
import socket
import json
import time
from datetime import datetime
file_lock = threading.Lock()
attacker_cache = {}
with open('signatures.json') as rules:
    rule_data = json.load(rules)

def log_event(attacker_ip, port_number):
    """V2 Heuristics: Detects if a single IP is hitting multiple ports."""
    if attacker_ip not in attacker_cache:
        attacker_cache[attacker_ip] = set()
    
    attacker_cache[attacker_ip].add(port_number)
    unique_ports = len(attacker_cache[attacker_ip])
    is_scan = unique_ports >= 3
    
    event_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "attacker_ip": attacker_ip,
        "target_port": port_number,
        "event_type": "PORT SCAN" if is_scan else "SINGLE PROBE",
        "severity": "HIGH" if is_scan else "LOW"
    }
    
    with file_lock:
        with open("ids_log.json", "a") as f:
            f.write(json.dumps(event_data) + "\n")

def anal_pack(hex_data):
    """V3 Engine: Deep Packet Inspection using bitwise flag matching."""
    try:
        packet = bytes.fromhex(hex_data)
        if len(packet) < 14: return 
        
        pac_flags = packet[13]
        
        for sig in rule_data['signatures']:

            if sig['flags'] == 0 and pac_flags == 0:
                print(f"[!] ALERT: {sig['name']} detected from hex stream!")

            elif (pac_flags & sig['flags']) == sig['flags']:
                print(f"[!] ALERT: {sig['name']} detected!")
    except Exception as e:
        print(f"[ERROR] Logic failure in anal_pack: {e}")

def watch_doors(port_number):
    """The Worker: Listens, Captures, and Routes to the Engine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(("0.0.0.0", port_number))
        s.listen(5)
        print(f"[*] Worker started on port: {port_number}")
        
        while True:
            client, addr = s.accept()
            attacker_ip = addr[0]

            try:
                raw_payload = client.recv(1024).hex()
                if raw_payload:
                    anal_pack(raw_payload)
                
                log_event(attacker_ip, port_number)
                print(f"[!!!] Connection from {attacker_ip} on port {port_number}")
                
            except Exception as e:
                print(f"[-] Worker Error on port {port_number}: {e}")
            finally:
                client.close()
    except Exception as e:
        print(f"[!] Could not bind to port {port_number}: {e}")

def list_doors():
    doors = [7777, 8888, 9999, 9090, 4444, 21]
    for port in doors:
        worker = threading.Thread(target=watch_doors, args=(port,))
        worker.daemon = True
        worker.start()

if __name__ == "__main__":
    print("[*] NIDS V3.1 Integrated Engine Active...")
    print("[*] Sensors deployed. Logging to ids_log.json.")
    list_doors()
    
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\n[!] Shutting down NIDS Engine...")
