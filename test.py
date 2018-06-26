import socket

host = '192.168.1.133'
port = 5789
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1)
result = sock.connect_ex((host, port))
if result == 0:
    print("Port is open")
else:
    print("Port is closed")
