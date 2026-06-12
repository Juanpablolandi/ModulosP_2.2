import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from etl.config import BRONZE_RPA_DIR
from etl.pipeline import process_file
from etl.db import refresh_gold_views


class RPAFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith((".csv", ".xlsx", ".xls")):
            return
        time.sleep(2)  # Espera breve para evitar leer un archivo mientras RPA aún lo copia.
        process_file(BRONZE_RPA_DIR / event.src_path.split("/")[-1])
        refresh_gold_views()


def watch_rpa_folder():
    observer = Observer()
    observer.schedule(RPAFileHandler(), str(BRONZE_RPA_DIR), recursive=False)
    observer.start()
    print(f"Escuchando archivos nuevos en: {BRONZE_RPA_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch_rpa_folder()
