import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 8080))
print("Сервер запущен")

while True:
    data, addr = server.recvfrom(1024)
    print(f"Сообщение от {addr}: {data.decode()}")
    server.sendto("Hello, client".encode(), addr)
