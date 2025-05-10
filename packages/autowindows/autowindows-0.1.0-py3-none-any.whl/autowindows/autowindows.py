# autowindows/autowindows.py
import os
import pyautogui
import subprocess
import ctypes
from comtypes import CLSCTX_ALL  # Импортируем CLSCTX_ALL из comtypes

def off():
    os.system("shutdown /s /t 1")

def reboot():
    os.system("shutdown /r /t 1")

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def click_mouse(times=1, button='left'):
    """Кликает по экрану указанной кнопкой мыши заданное количество раз."""
    x, y = pyautogui.position()
    for _ in range(times):
        if button == 'left':
            pyautogui.click(x, y)  # Клик левой кнопкой мыши
        elif button == 'right':
            pyautogui.click(x, y, button='right')  # Клик правой кнопкой мыши
        else:
            raise ValueError("Неправильная кнопка. Используйте 'left' или 'right'.")

def move_mouse(x_offset, y_offset):
    x, y = pyautogui.position()
    pyautogui.moveTo(x + x_offset, y + y_offset)

def type_text(text):
    pyautogui.write(text)

def erase(count):
    """Стирает заданное количество символов с клавиатуры."""
    for _ in range(count):
        pyautogui.press('backspace')

def start(file_path):
    """Открывает файл или приложение по указанному пути."""
    subprocess.Popen(file_path, shell=True)

def close_window(window_title):
    """Закрывает окно с заданным заголовком."""
    user32 = ctypes.windll.User32
    hWnd = user32.FindWindowW(None, window_title)
    if hWnd:
        user32.SendMessageW(hWnd, 0x0010, 0, 0)

def set_volume(volume_level):
    """Устанавливает уровень громкости от 0 до 100."""
    import pycaw
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    volume_level = max(0, min(volume_level, 100))  # Ограничиваем уровень от 0 до 100
    volume.SetMasterVolumeLevelScalar(volume_level / 100.0, None)

def newfile(directory, filename):
    """Создает новый файл в указанной директории с заданным именем."""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Директория {directory} не существует.")

    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as f:
        f.write("")  # Создаем пустой файл

def newdirectory(directory, folder_name):
    """Создает новую папку в указанной директории."""
    new_path = os.path.join(directory, folder_name)
    os.makedirs(new_path, exist_ok=True)  # Создаем папку, если она не существует

def deletefile(directory, filename):
    """Удаляет файл из указанной директории по имени."""
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        os.remove(file_path)  # Удаляем файл
    else:
        raise FileNotFoundError(f"Файл {file_path} не существует.")

def deletedirectory(directory, folder_name):
    """Удаляет папку из указанной директории по имени."""
    folder_path = os.path.join(directory, folder_name)
    if os.path.exists(folder_path):
        os.rmdir(folder_path)  # Удаляет пустую папку
    else:
        raise FileNotFoundError(f"Папка {folder_path} не существует.")