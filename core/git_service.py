from git import Repo, InvalidGitRepositoryError, NoSuchPathError


class GitService:

    @staticmethod
    def is_git_repo(path):
        try:
            Repo(path)
            return True
        except InvalidGitRepositoryError:
            return False
        except NoSuchPathError:
            return False

    @staticmethod
    def get_repo(path):
        return Repo(path)

    @staticmethod
    def get_change_stats(repo: Repo):
        diff = repo.git.diff("--stat")
        return diff

    @staticmethod
    def has_uncommitted_changes(repo: Repo):
        return repo.is_dirty(untracked_files=True)

    @staticmethod
    def commits_ahead(repo: Repo):
        try:
            branch = repo.active_branch
            return sum(1 for _ in repo.iter_commits(f'origin/{branch.name}..HEAD'))
        except:
            return 0

    @staticmethod
    def auto_commit(repo: Repo, message="auto commit"):
        repo.git.add(A=True)
        repo.index.commit(message)

    @staticmethod
    def push(repo: Repo):
        repo.remotes.origin.push()