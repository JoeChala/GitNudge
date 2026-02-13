from apscheduler.schedulers.background import BackgroundScheduler
from config import NIGHTLY_CHECK_HOUR


class NightlyScheduler:

    def __init__(self, func):
        self.scheduler = BackgroundScheduler()
        self.func = func

    def start(self):
        self.scheduler.add_job(
            self.func,
            'cron',
            hour=NIGHTLY_CHECK_HOUR,
            minute=0
        )
        self.scheduler.start()