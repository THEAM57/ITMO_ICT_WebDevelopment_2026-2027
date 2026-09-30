import socket

a = input("Введите первый катет: ")
b = input("Введите второй катет: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8080))
client.send(f"{a} {b}".encode())

print(client.recv(1024).decode())
client.close()
