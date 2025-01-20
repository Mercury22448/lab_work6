# ЕРШОВА ЮЛИЯ ДМИТРИЕВНА, ДПИ22-1, 2025 г.
# Сервер

import socket
import threading

# задаем хост и порт
host = ''
port = 57369
# создаем переменную для определения названия потока
k = 0
# список текущих подключений
active = []
# переменная для остановки сервера
event = threading.Event()


def handle_client(client_socket, client_address):
    global k
    with threading.Lock():
        k += 1
        print(f"Клиент {client_address} подключился к серверу.")
    while not event.is_set():
        # принимаем клиентское сообщение
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        with threading.Lock():
            print(f"Полученные от клиента {client_address} данные: {data}")
        # видоизменяем возвращаемые данные
        up_data = data.upper()  # переводим буквы в строке в верхний регистр
        repl_data = up_data.replace(' ', '__')  # делаем замену
        # отправляем видоизмененные данные клиенту
        client_socket.send(repl_data.encode('utf-8'))
        with threading.Lock():
            print(f"Данные отправлены обратно клиенту {client_address}.")
    with threading.Lock():
        print(f"Отключение клиента {client_address} от сервера.")
    # закрываем соединение
    client_socket.close()


def server():
    global active
    print("Запуск сервера....")
    # создаем сокет
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # привязываем сокет к хосту и порту
    s.bind((host, port))
    # прослушивание соединений
    s.listen(5)
    with threading.Lock():
        print(f"Сервер запустился на порту {port}....")
        print(f"Начало прослушивания входящих соединений на порту {port}....")

    try:
        while not event.is_set():
            # принимаем подключение
            client_socket, client_address = s.accept()
            # добавляем новое соединение в список
            active.append(client_socket)
            name = f"thread_{k + 1} "
            # создаем новый поток для клиента
            t = threading.Thread(target=handle_client, name=name, args=(client_socket, client_address))
            t.start()
            with threading.Lock():
                print(f" Запустился новый поток {name} для клиента {client_address}.")
    # в случае, если сервер был остановлен, обрабатываем  ошибки
    except KeyboardInterrupt:
        print("Сервер прерван пользователем. Закрытие соединений и выход.")
        for client_socket in active:
            # закрываем каждое соединение
            client_socket.close()
        # останавливаем сервер
        s.close()


if __name__ == "__main__":
    server()