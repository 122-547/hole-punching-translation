import socket
import cv2
import time
import numpy as np
import json

accept_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("147.45.79.209", 7676)
video_port = 5300
device = None
window_name = "Cam"
try:
    accept_client.bind(("0.0.0.0", 5400))
    video_client.bind(("0.0.0.0", 5300))
    accept_client.sendto(b"<GET>", server_addr)
    while device is None:
        data, addr = accept_client.recvfrom(1024)
        if not data:
            continue
        device = (json.loads(data.decode())[0], video_port)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)
    
    print("Ожидание видео... Нажмите 'q' для выхода")
    
    video_client.settimeout(0.5)
    frame_count = 0
    last_print = time.time()
    while True:
        try:

            data, addr = video_client.recvfrom(65536)

            np_arr = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is not None:
                frame_count += 1
                cv2.imshow(window_name, frame)
                if time.time() - last_print > 2:
                    print(f"Получено кадров: {frame_count}")
                    frame_count = 0
                    last_print = time.time()
  
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

        except socket.timeout:

            print(".", end='', flush=True)
            continue

except KeyboardInterrupt:
    print("\nПрерывание пользователя")
except Exception as e:
    print(f"\nОшибка: {e}")
finally:
    cv2.destroyAllWindows()
    accept_client.close()
    video_client.close()
    print("Админ отключился.")