# ЕРШОВА ЮЛИЯ ДМИТРИЕВНА, ДПИ22-1, 2024 г.
# Сканер


import socket
import threading


def scanner_sequential(host):
    # Список открытых портов при обычном сканировании
    ports_seq = []
    try:
        ip_address = socket.gethostbyname(host)
        print(f"\nПОСЛЕДОВАТЕЛЬНОЕ СКАНИРОВАНИЕ ПОРТОВ {host}.")
        print(f"Начинаем подключение к портам ...")
        # Создаём список всех портов
        all_ports = list(range(1, 65536))
        # Сканирование
        for port in all_ports:
            # Создаем сокет
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Устанавливаем таймаут на соединение
            sock.settimeout(3)
            # Соединение с портом
            result = sock.connect_ex((ip_address, port))
            # Если подключение успешно - добавляем порт в список и выводим сообщение
            ports_seq.append(port) if result == 0 else None
            print(f"Порт {port} открыт.") if result == 0 else None
            # Закрытие сокета
            sock.close()
    # В случае ошибки выводим сообщение
    except socket.error as error:
        print(f"Во время сканирования портов произошла ошибка: {error}")
    # Возвращаем список открытых портов
    return ports_seq


def scanner_threading(host):
    # Список открытых портов при параллельном сканировании
    ports_thread = []
    try:
        ip_address = socket.gethostbyname(host)
        print(f"\nПАРАЛЛЕЛЬНОЕ СКАНИРОВАНИЕ ПОРТОВ {host}.")
        print(f"Начинаем подключение к портам ...")
        # Сканируем порт
        def scan_port(port):
            try:
                # Создаём сокет
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Устанавливаем таймаут
                sock.settimeout(3)
                # Соединение с портом
                result = sock.connect_ex((ip_address, port))
                # Если подключение успешно - добавляем порт в список и выводим сообщение
                ports_thread.append(port) if result == 0 else None
                print(f"Порт {port} открыт.") if result == 0 else None
                # Закрываем сокет
                sock.close()
            except:
                pass
        # Список всех портов
        all_ports = list(range(1, 65536))
        # Список всех потоков сканирования портов
        all_threads = []
        # Параллельное сканирование портов
        for port in all_ports:
            # Создаём новый поток
            thread = threading.Thread(target=scan_port, args=(port,))
            # Добавляем в список всех потоков
            all_threads.append(thread)
            # Запускаем поток
            thread.start()
        # Завершаем потоки
        for thread in all_threads:
            thread.join()
    # В случае ошибки выводим сообщение
    except socket.error as error:
        print(f"Error: {error}")
    # Возвращаем список портов
    return ports_thread


# Проверяем корректность хоста
def host_validation(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False


if __name__ == "__main__":
    while True:
        host = input("Введите IP-адрес/имя хоста, порты которого Вы хотите просканировать: ")
        if host_validation(host):
            break
        else:
            print("Вы ввели некорректный IP-адрес/имя хоста. Проверьте корректность ввода или попробуйте другой.")
    scanner_sequential = scanner_sequential(host)
    print("Открытые порты:", scanner_sequential)
    scanner_threading = scanner_threading(host)
    print("Открытые порты:", scanner_threading)
