import threading
import socket
file = open("logs.txt","a")
def watch_doors(port_number):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(("0.0.0.0",port_number))
  s.listen(1)
  print(f"background scan started for port:{port_number}")
  while True:
    client,addr=s.accept()
    attacker_ip = addr[0]
    log=f"[!!!] ALERT: Port {port_number} was probed by {attacker_ip}"
    file.append(log)
    client.close()

def list_doors():
  doors=[8080,8888,9999,9090]
  for port in doors:
    worker=threading.Thread(target = watch_doors,args=(port,))
    worker.start()
list_doors()

