import sys
import os
import py7zr
from tempfile import NamedTemporaryFile

MORSE_CODE = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..',
    'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
    'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
    'q': '--.-', 'r': '.-.', 's': '...', 't': '-',
    'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    ' ': '/',             # пробел между словами
    '.': '.-.-.-', ',': '--..--', ':': '---...',
    '?': '..--..', "'": '.----.', '-': '-....-',
    '/': '-.-.-',         # нестандартный код
    '(': '-.--.', ')': '-.--.-', '"': '.-..-.',
    '@': '.--.-.', '=': '-...-', '!': '-.-.--',
    ';': '-.-.-.', '_': '..--.-', '+': '.-.-.',
    '$': '...-..-', '&': '.-...',
    os.linesep: '--..--..'  # символ новой строки (условный код)
}

RU_TRANS = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
}

def transliterate(text):
    return ''.join(RU_TRANS.get(c, c) for c in text.lower())

def encode_to_custom(text):
    text = transliterate(text)
    
    # Обрабатываем все символы, которые не поддерживаются
    unsupported = sorted(set(c for c in text if c not in MORSE_CODE and c != '|'))
    if unsupported:
        print("\n[!] Предупреждение: Эти символы пропущены:", ' '.join(unsupported))

    # Создаем морзе-последовательность
    morse = ' '.join(MORSE_CODE.get(c, '') for c in text if c in MORSE_CODE)

    # Объединяем все замены в одну строку
    morse = morse.replace('.', 'E').replace('-', 'T').replace(' ', 'A').replace('/', 'O')

    return morse

def read_file_with_fallback(file_path):
    """Функция для чтения файла с несколькими попытками кодировок."""
    encodings = ['utf-8', 'windows-1251', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError("Не удалось прочитать файл с использованием доступных кодировок")

def main():
    if len(sys.argv) < 3:
        print("Использование: encoder.exe путь_к_файлу путь_сохранения")
        return

    input_file = sys.argv[1]
    output_path = sys.argv[2]

    # Чтение текста из файла
    text = read_file_with_fallback(input_file)

    encoded = encode_to_custom(text)

    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(encoded)
        temp_file_path = temp_file.name

    # Создание архива
    compressed_path = output_path.replace(".mztf", ".7z")
    with py7zr.SevenZipFile(compressed_path, 'w', filters=[{
        'id': py7zr.FILTER_LZMA2,
        'preset': 9
    }]) as archive:
        archive.write(temp_file_path, arcname="encoded.txt")

    # Получаем размер оригинального файла и сжатого архива
    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_path)

    # Вычисляем степень сжатия
    if original_size > 0:
        compression_percentage = (1 - compressed_size / original_size) * 100
        print(f"Текст сжат на {compression_percentage:.2f}%")
    else:
        print("Ошибка: исходный файл пуст.")

    os.remove(temp_file_path)

    # Переименование архива с .7z на .mztf
    os.rename(compressed_path, output_path)
    print("Готово! Создан архив:", output_path)

if __name__ == "__main__":
    main()
