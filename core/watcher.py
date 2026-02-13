from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.change_count = 0
        self.last_event = time.time()

    def on_any_event(self, event):
        self.change_count += 1
        self.last_event = time.time()
        self.callback(self.change_count)


class RepoWatcher:

    def __init__(self):
        self.observer = Observer()

    def watch(self, path, callback):
        handler = ChangeHandler(callback)
        self.observer.schedule(handler, path, recursive=True)

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()