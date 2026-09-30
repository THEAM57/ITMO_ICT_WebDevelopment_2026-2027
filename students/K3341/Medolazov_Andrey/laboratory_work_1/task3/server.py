import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 8080))
server.listen(1)
print("Сервер запущен на http://localhost:8080")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()
    print(request.split("\r\n")[0])

    with open("index.html", "rb") as f:
        body = f.read()

    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    conn.sendall(headers.encode() + body)
    conn.close()
