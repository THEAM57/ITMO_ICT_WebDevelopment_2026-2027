import socket
import threading

clients = {}
lock = threading.Lock()


def broadcast(message, sender=None):
    with lock:
        for conn in list(clients):
            if conn != sender:
                try:
                    conn.send(message.encode())
                except OSError:
                    pass


def handle(conn):
    name = conn.recv(1024).decode().strip()
    with lock:
        clients[conn] = name
    print(f"{name} подключился")
    broadcast(f"{name} вошел в чат", conn)

    while True:
        try:
            data = conn.recv(1024)
        except OSError:
            break
        if not data:
            break
        message = data.decode()
        if message == "/exit":
            break
        print(f"{name}: {message}")
        broadcast(f"{name}: {message}", conn)

    with lock:
        del clients[conn]
    conn.close()
    print(f"{name} отключился")
    broadcast(f"{name} вышел из чата")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 8080))
server.listen()
print("Сервер чата запущен")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
