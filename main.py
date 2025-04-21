import os
import subprocess
import platform
import sys
import tkinter as tk
from tkinter import filedialog

PYTHON_EXECUTABLE = sys.executable  # путь к текущему интерпретатору Python

ENCODER_SCRIPT = "encoder.py"  # или "encoder.exe"
DECODER_SCRIPT = "decoder.py"  # или "decoder.exe"

def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def select_file_for_encoding():
    """Открывает диалог выбора файла только для текстовых файлов (.txt)."""
    root = tk.Tk()
    root.withdraw()
    root.update()  # предотвращает "мелькание" окна
    path = filedialog.askopenfilename(
        title="Выберите текстовый файл для кодирования",
        filetypes=[("Текстовые файлы", "*.txt")]
    )
    root.destroy()
    return path

def select_file_for_decoding():
    root = tk.Tk()
    root.withdraw()
    root.update()  # предотвращает "мелькание" окна
    path = filedialog.askopenfilename(
        title="Выберите сжатый файл (.aaa) для декодирования",
        filetypes=[("Текст MorseZip", "*.mztf")]
    )
    root.destroy()
    return path

def save_file_dialog(default_name="output.mztf"):
    """Открывает диалог сохранения файла и возвращает путь или пустую строку."""
    root = tk.Tk()
    root.withdraw()
    root.update()  # предотвращает "мелькание" окна
    path = filedialog.asksaveasfilename(
        defaultextension=".aaa",
        initialfile=default_name,
        filetypes=[("Текст MorseZip", "*.mztf")]
    )
    root.destroy()
    return path

def encode_file(path, output_path):
    """Вызывает внешний encoder‑скрипт с параметрами для пути сохранения."""
    subprocess.run([PYTHON_EXECUTABLE, ENCODER_SCRIPT, path, output_path])

def decode_file(path):
    """Вызывает внешний decoder‑скрипт."""
    subprocess.run([PYTHON_EXECUTABLE, DECODER_SCRIPT, path])

def main():
    while True:
        clear()
        print("=== Главное меню ===")
        print("1 – Кодировать и сжать")
        print("2 – Распаковать и декодировать")
        print("3 – Выход")
        choice = input("> ").strip()

        if choice == '1':
            file_path = select_file_for_encoding()  # Выбираем только текстовый файл для кодирования
            if file_path:
                output_path = save_file_dialog()
                if output_path:
                    encode_file(file_path, output_path)
                else:
                    print("Отменено сохранение.")
            else:
                print("Файл не выбран.")
            input("\nНажмите Enter для возврата в меню...")

        elif choice == '2':
            file_path = select_file_for_decoding()  # Выбираем только .aaa файл для декодирования
            if file_path:
                decode_file(file_path)
            else:
                print("Файл не выбран.")
            input("\nНажмите Enter для возврата в меню...")

        elif choice == '3':
            print("Выход...")
            break

        else:
            print("Неверный выбор.")
            input("Нажмите Enter для возврата в меню...")

if __name__ == "__main__":
    main()
