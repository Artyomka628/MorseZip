import sys
import os
import py7zr

REVERSE_MORSE_CODE = {
    '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd',
    '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h',
    '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l',
    '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
    '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
    '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
    '-.--': 'y', '--..': 'z', '-----': '0', '.----': '1',
    '..---': '2', '...--': '3', '....-': '4', '.....': '5',
    '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '/': ' ', '.-.-.-': '.', '--..--': ',', '---...': ':',
    '..--..': '?', '.----.': "'", '-....-': '-', '-.-.-': '/',  # обновлённый слэш
    '-.--.': '(', '-.--.-': ')', '.-..-.': '"', '.--.-.': '@',
    '-...-': '=', '-.-.--': '!', '-.-.-.': ';', '..--.-': '_',
    '.-.-.': '+', '...-..-': '$', '.-...': '&',
    '--..--..': os.linesep  # символ новой строки
}

REVERSE_RU_TRANS = {
    'ya': 'я', 'yu': 'ю', 'sch': 'щ', 'sh': 'ш', 'ch': 'ч', 'zh': 'ж',
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'z': 'з',
    'i': 'и', 'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
    'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х',
    'c': 'ц', 'y': 'ы'
}

REVERSE_RU_KEYS = sorted(REVERSE_RU_TRANS.keys(), key=lambda x: -len(x))

def decode_from_custom(custom):
    morse = custom.replace('E', '.').replace('T', '-').replace('A', ' ').replace('O', '/').replace('ZZZ', '|')
    parts = morse.strip().split(' ')
    return ''.join(REVERSE_MORSE_CODE.get(p, '?') for p in parts)

def detransliterate(text):
    i = 0
    result = ''
    while i < len(text):
        for key in REVERSE_RU_KEYS:
            if text[i:i+len(key)] == key:
                result += REVERSE_RU_TRANS[key]
                i += len(key)
                break
        else:
            result += text[i]
            i += 1
    return result

def main():
    if len(sys.argv) < 2:
        print("Использование: decoder.exe архив.mztf")
        return

    archive = sys.argv[1]
    temp_dir = "_temp_extract"

    with py7zr.SevenZipFile(archive, mode='r') as archive:
        archive.extractall(path=temp_dir)

    file_name = os.listdir(temp_dir)[0]
    with open(os.path.join(temp_dir, file_name), 'r', encoding='utf-8') as f:
        encoded = f.read()

    decoded = decode_from_custom(encoded)
    final = detransliterate(decoded)
    print("\n" + final)

    os.remove(os.path.join(temp_dir, file_name))
    os.rmdir(temp_dir)

if __name__ == "__main__":
    main()
