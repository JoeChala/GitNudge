from core.git_service import GitService
from config import MASSIVE_CHANGE_FILE_THRESHOLD


class RepoManager:

    def __init__(self, storage):
        self.storage = storage

    def analyze_repo(self, path):
        if not GitService.is_git_repo(path):
            return None

        repo = GitService.get_repo(path)

        return {
            "dirty": GitService.has_uncommitted_changes(repo),
            "ahead": GitService.commits_ahead(repo),
            "stats": GitService.get_change_stats(repo)
        }

    def should_suggest_push(self, change_count):
        return change_count > MASSIVE_CHANGE_FILE_THRESHOLD