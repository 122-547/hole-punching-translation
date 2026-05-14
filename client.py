# import socket
# import json
# import threading

# def getting_messages():
#     global client, device
#     while True:
#         data, addr = client.recvfrom(4096)
#         if not data:
#             continue
#         print("Anon:", data.decode())

# def sending_messages():
#     global client, device
#     while True:
#         message = input("\r")

# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# device = None
# try:
#     client.bind(("0.0.0.0", 5557))
#     client.sendto(b"<GET>", ("147.45.79.209", 7676))
#     while device is None:
#         data, addr = client.recvfrom(1024)
#         if not data:
#             continue
#         device = json.loads(data.decode())

#     while True:
        


    
        
# finally:

#     client.close()




import socket
import json
import cv2
import threading
import time

def get_frame(cam: cv2.VideoCapture):
    ret, frame = cam.read()
    if not ret:
        return None
    
    # Уменьшаем размер для UDP
    height, width = frame.shape[:2]
    if width > 640:
        scale = 640 / width
        new_width = 640
        new_height = int(height * scale)
        frame = cv2.resize(frame, (new_width, new_height))
    
    # Сжимаем с хорошим качеством
    success, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    
    if success:
        bytes_data = encoded_img.tobytes()
        if len(bytes_data) < 65000:  # Оставляем запас
            return bytes_data
        else:
            # Если всё ещё большой, сжимаем сильнее
            success, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            if success:
                return encoded_img.tobytes()
    return None


accept_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("147.45.79.209", 7676)
device = None
video_port = 5300
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FPS, 15)

time.sleep(2)

DESIRED_FPS = 10
frame_time = 1.0 / DESIRED_FPS
try:
    accept_client.bind(("0.0.0.0", 5400))
    accept_client.sendto(b"<GET>", server_addr)
    print("Запрос <GET> отправлен, ожидаю ответ.")
    while device is None:
        data, addr = accept_client.recvfrom(1024)
        if not data:
            continue
        device = (json.loads(data.decode())[0], video_port)
        print(f"Получен ответ: {device}")

    while True:
        start_time = time.time()
        frame = get_frame(cam)
        
        if frame:
            accept_client.sendto(frame, device)
            frame_count += 1
            if time.time() - last_print > 2:
                print(f"Отправлено кадров: {frame_count}")
                frame_count = 0
                last_print = time.time()
        else:
            print("Ошибка получения кадра", end='\r')

        elapsed_time = time.time() - start_time
        sleep_time = frame_time - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)


finally:
    accept_client.close()
   