import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello, server".encode(), ("localhost", 8080))

data = client.recv(1024)
print(f"Ответ сервера: {data.decode()}")
client.close()
