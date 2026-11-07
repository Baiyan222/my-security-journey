import socket
def scan_port(ip,port):
      s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.settimeout(1)
      try :
          result=s.connect_ex((ip,port))
          if result==0:
              print(f"端口{port}开放")
      except Exception as e:
          pass
      finally:
            s.close()
target_ip='127.0.0.1'
for p in range(1,1024):
    scan_port(target_ip,p)

        
