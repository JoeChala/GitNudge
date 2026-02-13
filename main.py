import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QAction, QIcon

from ui.main_window import MainWindow
from core.scheduler import NightlyScheduler
from db.storage import Storage
from core.repo_manager import RepoManager


def nightly_check():
    storage = Storage()
    manager = RepoManager(storage)

    for repo in storage.get_repos():
        info = manager.analyze_repo(repo)
        if info and info["ahead"] > 0:
            print(f"[REMINDER] {repo} has unpushed commits")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

tray = QSystemTrayIcon(QIcon(), parent=app)
menu = QMenu()

open_action = QAction("Open")
open_action.triggered.connect(window.show)

quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)

menu.addAction(open_action)
menu.addAction(quit_action)

tray.setContextMenu(menu)
tray.show()

scheduler = NightlyScheduler(nightly_check)
scheduler.start()

sys.exit(app.exec())