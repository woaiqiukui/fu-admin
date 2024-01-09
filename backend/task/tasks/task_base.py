from celery.worker.request import Request
from celery import Task as CeleryTask
from fuadmin.celery import app
import os,platform
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
# 检测当前的操作系统和架构
system = platform.system()
arch = platform.machine()

class MyRequest(Request):
    'A minimal custom request to log failures and hard time limits.'
    def __init__(self, *args, **kwargs):
        super(MyRequest, self).__init__(*args, **kwargs)
    def on_timeout(self, soft, timeout):
        super(MyRequest, self).on_timeout(soft, timeout)
        if not soft:
           logger.warning(
               'A hard timeout was enforced for task %s',
               self.task.name
           )

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        super().on_failure(
            exc_info,
            send_failed_event=send_failed_event,
            return_ok=return_ok
        )
        logger.warning(
            'Failure detected for task %s',
            self.task.name
        )

# 任务执行失败后重试
class BaseTaskWithRetry(CeleryTask):
    Request = MyRequest
    autoretry_for = (TypeError,)
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = False

# 清理任务
@app.task
def cleanUpFile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)