from uvicorn import run
import signal
import sys

def signal_handler(sig, frame):
    print('Exiting gracefully...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Обработка SIGINT (Ctrl+C)
    signal.signal(signal.SIGTERM, signal_handler)  # Обработка SIGTERM (завершение процесса)
    run("app.main:app", reload=True)

