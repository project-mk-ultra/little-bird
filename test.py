import socket

host = '192.168.1.112'
port = 9789

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.settimeout(1)

try:
    s.connect((host, port))
    print("connected")
except Exception as e:
    print(e)
