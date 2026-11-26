import cv2
import numpy as np
import datetime
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
filename = input("Введите имя файла (например, image1.jpg или image2.png): ").strip()

# 2. Формируем пути к файлам
input_path = os.path.join(script_dir, "data", "input", filename)
output_path = os.path.join(script_dir, "data", "output", "result.jpg")
log_path = os.path.join(script_dir, "logs", "history.txt")
status = "Успешно"
filter_name = "Медианный фильтр + Робастная коррекция"
try:
    with open(input_path, 'rb') as f:
        img_bytes = f.read()

    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Файл не является изображением")

    img = cv2.medianBlur(img, 5) #медианный фильтр

    lo, hi = np.percentile(img, (1, 99)) #робастная коррекция
    if hi > lo:
        img = np.clip(
            (img.astype(np.float32) - lo) / (hi - lo) * 255, 0, 255
        ).astype(np.uint8)

    cv2.imwrite(output_path, img)
    print(f"Успех! Результат сохранен в: {output_path}")

except FileNotFoundError:
    status = "Ошибка: Файл не найден"
    print(status)
    filter_name = "Н/Д"
except PermissionError:
    status = "Ошибка доступа"
    print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
    filter_name = "Н/Д"
except Exception as e:
    status = f"Ошибка {e}"
    print(f"Ошибка: {e}")
    filter_name = "Н/Д"

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    with open(log_path, 'a', encoding='UTF-8') as log_file:
        log_file.write(f"[{now}] Файл: {filename} | Фильтр: {filter_name} | Статус: {status}\n")
except Exception as e:
    print(f"Не удалось записать лог: {e}")