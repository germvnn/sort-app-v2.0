import subprocess
import os
import logging

logger = logging.getLogger("logger")
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("logs/subprocessing.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def adb_pull_to_safe_path(destination_path):
    # Utwórz bezpieczną ścieżkę do folderu docelowego
    safe_destination_path = os.path.abspath(destination_path)

    # Sprawdź, czy folder docelowy istnieje, jeśli nie, utwórz go
    if not os.path.exists(safe_destination_path):
        os.makedirs(safe_destination_path)
        logger.info(f"Created directory: {safe_destination_path}")

    # Utwórz komendę adb pull
    command = 'adb shell "ls /sdcard/DCIM/Camera/"'  # Załóżmy, że chcesz wypisać zawartość tej ścieżki
    # Wykonaj polecenie za pomocą subprocess
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

    # Wypisz wynik komendy
    if result.returncode == 0:
        print("Wynik polecenia:\n" + result.stdout)
    else:
        print(f"Błąd podczas wykonania polecenia: {result.stderr}")


# Użyj funkcji z bezpieczną ścieżką
adb_pull_to_safe_path("C:/Users/Daniel/Desktop/test")
