import time
import socket


def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=""):
    data = data.encode("utf-8")
    conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    conn.send(b"Server: simplehttp\r\n")
    conn.send(b"Connection: close\r\n")
    conn.send(b"Content-type " + typ.encode("utf-8") + b"\r\n")
    conn.send(b"Content-length " + bytes(len(data)) + b"\r\n")
    conn.send(b"\r\n")  # после пустой строки в http идут данные
    conn.send(data)



def parse(conn, addr):
    """
    Обработка соединения в отдельной функции
    :param conn:
    :param addr:
    :return:
    """

    data = b""
    while not b"\r\n" in data:  # ждем первую строчку
        tmp = conn.recv(1024)
        if not tmp:  # закрываем сокет, т.к. данных нет, пустой объект
            break
        else:
            data += tmp

    if not data:  # данные не пришли, не производим обработку
        return

    udata = data.decode("utf-8")

    # берем первую строку данных
    udata = udata.split("\r\n", 1)[0]

    # разбиваем строку по пробелам
    method, address, protocol = udata.split(" ", 2)

    if method != "GET" or address != "/time.html":
        send_answer(conn, "404 not found", data=" Не найдено")
        return

    answer = """<!DOCTYPE html>"""
    answer += """<html><head><title>Время</head></title><body><h1>"""
    answer += time.strftime("%H:%M:%S %d.%m.%Y")
    answer += """</h1></body></html>"""

    send_answer(conn, typ="text/html; charset=utf-8", data=answer)


sock = socket.socket()
sock.bind(("127.0.0.1", 8084))
sock.listen(5)

try:
    while 1:
        conn, addr = sock.accept()
        print("New connection from " + addr[0])
        try:
            parse(conn, addr)
        except:
            send_answer(conn, "500 Internal Server Error", data="Внимание, ошибка!")
        finally:
            conn.close()
finally:
    sock.close()
