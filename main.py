import cv2
import numpy as np
import datetime
import os

# Узнаем папку, в которой лежит сам скрипт, чтобы пути работали всегда
script_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Запрашиваем имя файла у пользователя
filename = input("Введите имя файла (например, image1.jpg или image2.png): ").strip()

# 2. Формируем пути к файлам
input_path = os.path.join(script_dir, "data", "input", filename)
output_path = os.path.join(script_dir, "data", "output", "result.jpg")
log_path = os.path.join(script_dir, "logs", "history.txt")

# Переменные для лога
status = "Успешно"
filter_name = "Медианный фильтр + Робастная коррекция"

# 3. Пытаемся открыть файл и обработать ошибки
try:
    # Открываем файл на чтение
    with open(input_path, 'rb') as f:
        img_bytes = f.read()

    # Превращаем байты обратно в картинку
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Если картинка не считалась (например, это текстовый файл)
    if img is None:
        raise ValueError("Файл не является изображением")

    # 4. Обработка (Задание 1: Медианный фильтр, ядро 5х5)
    img = cv2.medianBlur(img, 5)

    # 4. Обработка (Задание 2: Робастная коррекция через нормализацию)
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

    # 5. Сохраняем результат
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
    status = "Ошибка доступа"
    print(f"Ошибка: {e}")
    filter_name = "Н/Д"

# 6. Логирование
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"[{now}] Файл: {filename} | Фильтр: {filter_name} | Статус: {status}\n"

try:
    # Открываем файл лога в режиме добавления ('a') и с кодировкой UTF-8
    with open(log_path, 'a', encoding='UTF-8') as log_file:
        log_file.write(log_entry)
except Exception as e:
    print(f"Не удалось записать лог: {e}")