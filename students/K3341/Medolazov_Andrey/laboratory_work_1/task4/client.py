import socket
import threading


def receive(client):
    while True:
        try:
            data = client.recv(1024)
        except OSError:
            break
        if not data:
            break
        print(data.decode())


name = input("Ваше имя: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8080))
client.send(name.encode())
print("Вы в чате. Для выхода напишите /exit")

threading.Thread(target=receive, args=(client,), daemon=True).start()

while True:
    message = input()
    if not message:
        continue
    client.send(message.encode())
    if message == "/exit":
        break

client.close()
