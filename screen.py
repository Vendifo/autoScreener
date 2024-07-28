import pyautogui
import os
import time
from pynput import keyboard
import threading

# Папка для сохранения скриншотов
SAVE_DIR = 'screenshots'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Интервал между скриншотами (в секундах)
INTERVAL = 5  # Установите интервал между скриншотами в 5 секунд

# Переменные для управления запуском/остановкой
is_running = False
stop_event = threading.Event()
exit_event = threading.Event()

def take_screenshot():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot = pyautogui.screenshot()
    screenshot.save(os.path.join(SAVE_DIR, f'screenshot_{timestamp}.png'))
    print(f'Screenshot taken and saved as screenshot_{timestamp}.png')

def screenshot_thread():
    while not stop_event.is_set():
        take_screenshot()
        time.sleep(INTERVAL)

def on_press(key):
    global is_running
    try:
        if hasattr(key, 'char') and key.char == 'х':  # Если нажата клавиша 'х'
            if not is_running:
                print("Starting screenshot capture.")
                is_running = True
                stop_event.clear()
                thread = threading.Thread(target=screenshot_thread)
                thread.start()
        elif hasattr(key, 'char') and key.char == 'ъ':  # Если нажата клавиша 'ъ'
            if is_running:
                print("Stopping screenshot capture.")
                is_running = False
                stop_event.set()
    except AttributeError:
        pass

def on_release(key):
    if hasattr(key, 'char') and key.char == 'э':  # Если нажата клавиша 'э'
        print("Exiting script.")
        exit_event.set()
        return False  # Остановить прослушивание

# Запуск прослушивания клавиш
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    exit_event.wait()  # Ожидание события выхода
    print("Script has been exited.")
