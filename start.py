import time
import threading
import subprocess

def run_command(command):
    subprocess.run(command)

if __name__ == "__main__":
    # создание и запуск потоков для каждого процесса
    t1 = threading.Thread(target=run_command, args=(["python", "-m", "celery", "-A", "app:celery", "worker", "--concurrency=20", "--loglevel=INFO", "--pool=solo"],))
    t1.start()
    time.sleep(2)

    t2 = threading.Thread(target=run_command, args=(["python", "-m", "celery", "-A", "app:celery", "flower"],))
    t2.start()
    time.sleep(2)

    # t3 = threading.Thread(target=run_command, args=(['gunicorn', '--access-logfile', '-', '--error-logfile', '-', '-w', '10', '-k', 'eventlet', '-b', '0.0.0.0:5000', 'app:app'],))
    # t3.start()
    # time.sleep(2)

    t3 = threading.Thread(target=run_command, args=(['python', 'app:app'],))
    t3.start()
    time.sleep(2)

    t4 = threading.Thread(target=run_command, args=(["python", "app_files.py"],))
    t4.start()

    # ожидание завершения всех потоков
    t1.join()
    t2.join()
    t3.join()
    t4.join()
