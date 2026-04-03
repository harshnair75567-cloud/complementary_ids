import socket
import time
target_ip = "127.0.0.1" 
target_ports = [7777, 8888, 21]

def launch_test():
    print(f"[*] Starting NIDS test on {target_ip}...")

    for port in target_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            print(f"[!] Probing Port: {port}")
            s.connect((target_ip, port))
            hex_payload = bytes.fromhex("00000000000000000000000000030000")
            s.send(hex_payload)
            
            print(f"[+] Payload sent to {port}")
            s.close()

            time.sleep(1) 
            
        except Exception as e:
            print(f"[?] Port {port} might be closed or filtered: {e}")

if __name__ == "__main__":
    launch_test()
    print("[*] Test complete. Check your NIDS terminal and 'ids_log.json'!")
