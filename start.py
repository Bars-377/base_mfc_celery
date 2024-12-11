import subprocess
import time

# Функция для запуска процесса с автоматическим перезапуском
def restartable_process(command):
    while True:
        try:
            print(f"Запускаем: {' '.join(command)}")
            process = subprocess.Popen(command)
            process.wait()  # Ожидание завершения процесса
            print(f"Процесс {' '.join(command)} завершился. Перезапуск через 5 секунд...")
            time.sleep(5)  # Небольшая задержка перед перезапуском
        except KeyboardInterrupt:
            print(f"Процесс {' '.join(command)} остановлен вручную.")
            process.terminate()
            break

# Основной запуск процессов
if __name__ == "__main__":
    try:
        # Запускаем процессы в отдельных потоках
        import threading
        threads = [
            threading.Thread(target=restartable_process, args=(["python", "gunicorn -w 10 -k eventlet app:app"],)),
            threading.Thread(target=restartable_process, args=(["python", "app_files.py"],))
        ]

        for thread in threads:
            thread.start()

        # Ожидаем завершения всех потоков
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Скрипт остановлен.")
