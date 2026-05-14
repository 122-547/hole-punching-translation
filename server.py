import socket
import json

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
devices = []
try:
    server.bind(("0.0.0.0", 7676))
    print("Сервер запущен и ждет подключения клиентов.")
    while True:
        data, addr = server.recvfrom(1024)
        if not data:
            continue
        if data == b"<GET>":
            devices.append(addr)
            print(f"Адрес {addr} добавлен в массив. Устройств: {len(devices)}")

        if len(devices) == 2:
            # for i in range(1, 0, -1):
            #     server.sendto(json.dumps(devices[i-1]).encode(), devices[i])
            #     print(f"Адрес {devices[i-1]} отправлен на {devices[i]}")
            server.sendto(json.dumps(devices[0]).encode(), devices[1])
            print(f"Адрес {devices[0]} отправлен на {devices[1]}")
            server.sendto(json.dumps(devices[1]).encode(), devices[0])
            print(f"Адрес {devices[1]} отправлен на {devices[0]}")
            devices.clear()

            
finally:
    print("Сервер остановлен.")
    server.close()




