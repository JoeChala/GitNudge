from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QListWidget, QFileDialog,
    QMessageBox, QLabel
)

from db.storage import Storage
from core.repo_manager import RepoManager
from core.git_service import GitService


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PushPilot")

        self.storage = Storage()
        self.manager = RepoManager(self.storage)

        layout = QVBoxLayout()

        self.repo_list = QListWidget()
        layout.addWidget(QLabel("Tracked Repositories"))
        layout.addWidget(self.repo_list)

        add_btn = QPushButton("Add Repo")
        add_btn.clicked.connect(self.add_repo)
        layout.addWidget(add_btn)

        push_btn = QPushButton("Push Selected")
        push_btn.clicked.connect(self.push_selected)
        layout.addWidget(push_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.refresh()

    def refresh(self):
        self.repo_list.clear()
        for repo in self.storage.get_repos():
            self.repo_list.addItem(repo)

    def add_repo(self):
        path = QFileDialog.getExistingDirectory(self)
        if path:
            if GitService.is_git_repo(path):
                self.storage.add_repo(path)
                self.refresh()
            else:
                QMessageBox.warning(self, "Error", "Not a git repo")

    def push_selected(self):
        item = self.repo_list.currentItem()
        if not item:
            return

        repo = GitService.get_repo(item.text())

        if GitService.has_uncommitted_changes(repo):
            GitService.auto_commit(repo)

        GitService.push(repo)
        QMessageBox.information(self, "Done", "Pushed!")