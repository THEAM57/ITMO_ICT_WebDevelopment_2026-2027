import math
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 8080))
server.listen(1)
print("Сервер запущен")

while True:
    conn, addr = server.accept()
    print(f"Подключился {addr}")
    data = conn.recv(1024).decode()
    try:
        a, b = map(float, data.split())
        if a <= 0 or b <= 0:
            answer = "Катеты должны быть больше нуля"
        else:
            answer = f"Гипотенуза: {math.sqrt(a ** 2 + b ** 2):.4f}"
    except ValueError:
        answer = "Нужно передать два числа"
    print(f"Катеты: {data}, ответ: {answer}")
    conn.send(answer.encode())
    conn.close()
