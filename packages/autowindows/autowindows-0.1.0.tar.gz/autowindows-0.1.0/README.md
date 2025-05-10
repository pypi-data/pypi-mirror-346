# autowindows

Простая библиотека для управления
компьютером с помощью Python

# Установка

pip install autowindows

# Пример использования

import autowindows as aw

function = str(input("Что вы хотите сделать? > "))

if function.lower() == "выключить компьютер":
    aw.off()  # Выключаем компьютер
elif function.lower() == "перезагрузить компьютер":
    aw.reboot()  # Перезагружаем компьютер