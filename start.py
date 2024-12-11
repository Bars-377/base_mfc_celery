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
        except Exception as e:
            print(f"Ошибка при выполнении команды {' '.join(command)}: {e}")
            print("Перезапуск процесса через 5 секунд...")
            time.sleep(5)

# Основной запуск процессов
if __name__ == "__main__":
    try:
        # Список команд для запуска процессов
        commands = [
            ["python", "-m", "celery", "-A", "app:celery", "worker", "--concurrency=20", "--loglevel=INFO", "--pool=solo"],
            ["python", "-m", "celery", "-A", "app:celery", "flower"],
            ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-w", "10", "-k", "eventlet", "-b", "0.0.0.0:5000", "app:app"],
            ["python", "app_files.py"]
        ]

        while True:
            for command in commands:
                try:
                    # Запуск процесса
                    restartable_process(command)
                    print(f"Процесс {' '.join(command)} завершён успешно.")
                except Exception as e:
                    print(f"Ошибка при выполнении команды {' '.join(command)}: {e}")
                    print("Перезапуск всех процессов через 5 секунд...")
                    time.sleep(5)  # Задержка перед перезапуском всех процессов

    except KeyboardInterrupt:
        print("Скрипт остановлен.")
