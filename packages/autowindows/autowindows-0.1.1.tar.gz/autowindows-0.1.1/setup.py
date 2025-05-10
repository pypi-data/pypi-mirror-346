from setuptools import setup, find_packages

setup(
   name='autowindows',
   version='0.1.1',
   description='Библиотека для управления Windows с помощью Python.',
   author='Georgii Nikishov',
   author_email='timofeynikishov@yandex.ru',
   packages=find_packages(),  # Найти все пакеты в директории
   install_requires=[
       'pyautogui',           # Зависимость от pyautogui
       'pycaw',               # Зависимость от pycaw
       'comtypes',   # Зависимость от speechrecognition
       'wmi'              # Зависимость от pyaudio
   ],
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',  # Лицензия
       'Operating System :: OS Independent',      # Операционная система
   ],
   python_requires='>=3.6',  # Минимальная версия Python
)