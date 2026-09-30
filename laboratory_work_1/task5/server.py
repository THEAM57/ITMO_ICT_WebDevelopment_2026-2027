import socket
from urllib.parse import parse_qs

grades = {}


def make_page():
    rows = ""
    for subject, marks in grades.items():
        rows += f"<tr><td>{subject}</td><td>{', '.join(marks)}</td></tr>"
    return f"""<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Журнал оценок</title></head>
<body>
<h1>Журнал оценок</h1>
<table border="1">
<tr><th>Дисциплина</th><th>Оценки</th></tr>
{rows}
</table>
<h2>Добавить оценку</h2>
<form method="POST" action="/">
<input name="subject" placeholder="Дисциплина" required>
<input name="grade" placeholder="Оценка" required>
<button type="submit">Отправить</button>
</form>
</body>
</html>"""


def send_response(conn, status, body=""):
    body = body.encode()
    headers = f"HTTP/1.1 {status}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(body)}\r\n"
    if status.startswith("303"):
        headers += "Location: /\r\n"
    conn.sendall((headers + "\r\n").encode() + body)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 8080))
server.listen()
print("Сервер запущен на http://localhost:8080")

while True:
    conn, addr = server.accept()
    data = conn.recv(4096)
    if not data:
        conn.close()
        continue

    head, _, body = data.partition(b"\r\n\r\n")
    lines = head.decode().split("\r\n")
    method, path = lines[0].split()[:2]
    print(method, path)

    headers = {}
    for line in lines[1:]:
        key, _, value = line.partition(":")
        headers[key.lower()] = value.strip()

    length = int(headers.get("content-length", 0))
    while len(body) < length:
        body += conn.recv(4096)

    if method == "GET" and path == "/":
        send_response(conn, "200 OK", make_page())
    elif method == "POST" and path == "/":
        params = parse_qs(body.decode())
        subject = params.get("subject", [""])[0].strip()
        grade = params.get("grade", [""])[0].strip()
        if subject and grade:
            grades.setdefault(subject, []).append(grade)
            send_response(conn, "303 See Other")
        else:
            send_response(conn, "400 Bad Request", "<h1>Нужно указать дисциплину и оценку</h1>")
    else:
        send_response(conn, "404 Not Found", "<h1>Страница не найдена</h1>")

    conn.close()
