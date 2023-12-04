import ipaddress
import uuid
from fuadmin.celery import app
import subprocess
from .models import Port, Task
from enum import Enum
import errno
from celery.exceptions import Reject, Ignore
from celery.utils.log import get_task_logger
from celery.worker.request import Request
from celery import group, states
from celery import Task as CeleryTask


logger = get_task_logger(__name__)


class SubTaskType(Enum):
    SUBDOMAIN_SCAN = "subdomainScan"
    # 用于识别 CDN 
    CDN_SCAN = "cdnScan"
    FINGER_SCAN = "fingerScan"
    PORT_SCAN = "portScan"
    POC_SCAN = "pocScan"
    # 在这里添加其他任务类型

class TaskManager:
    def __init__(self, task_uuid, task_params):
        self.task_uuid = task_uuid
        self.task_params = task_params
        self.task_list = []
        self.subtask_result = None

    ### task_params 格式
    # {
    #   "task_uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    #   "if_crontab": False,
    #   "params": [
    #     {
    #       "subtask_type": "subdomainScan",
    #       "subparams": {
    #         "target": "www.baidu.com\nwww.google.com"
    #       }
    #     },
    #     {
    #       "subtask_type": "portScan",
    #       "subparams": {
    #         "target": "www.baidu.com\nwww.google.com"
    #       }
    #     }
    #   ]
    # }

    def create_subtask_group(self):
        for param in self.task_params['params']:
            subtask_type = param['subtask_type']
            subparams = param['subparams']
            if subtask_type == 'subdomainScan':
                self.task_list.append(subdomainScan.s(subparams))
            elif subtask_type == 'portScan':
                self.task_list.append(portScan.s(subparams))
        job = group(*self.task_list)
        self.subtask_result = job.apply_async()
        return self.subtask_result

    def get_task_state(self):
        # 所有子任务成功完成
        if self.subtask_result.successful():
            return "SUCCESS"
        # 子任务中有失败
        elif self.subtask_result.failed():
            return "FAILURE"
        # 子任务尚未准备好
        elif self.subtask_result.waiting():
            return "WAITING"
        # 所有子任务都准备就绪
        elif self.subtask_result.ready():
            return "READY"
        else:
            return "PENDING"
    
    def get_completed_count(self):
        return self.subtask_result.completed_count()
    
    def get_task_result(self):
        return self.subtask_result.get()
    

    def revoke_task(self):
        self.subtask_result.revoke()
        return 'SUCCESS'
    
    def revoke_subtask(self, subtask_id):
        self.subtask_result.revoke(subtask_id)
        return 'SUCCESS'
    


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


@app.task(bind=True, name="task.tasks.subdomainScan", queue="subdomainScan")
def subdomainScan(self, params):
    logger.info("Executing Subdomain Scan task id {0.id}".format(self.request))
    try:
        # Update task status to running
        self.update_state(state='PROGRESS', meta={'current': 50, 'total': 100})
        pass
        # if redis.ismember('tasks.revoked', self.request.id):
        #     raise Ignore()
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Subdomain Scan Failed")

    return "Subdomain Scan Complete"


# portScan params
# {
#   "port": "3306\n6379\n1433",
#   "target": "10.30.2.2\n10.30.2.3\n10.30.2.4"
# }
@app.task(bind=True, name="task.tasks.portScan", queue="portScan", base=BaseTaskWithRetry)
def portScan(self, params):
    logger.info("Executing Port Scan task id {0.id}".format(self.request))
    try:
        naabu_path = 'utils/tools/naabu'
        # Update task status to running
        self.update_state(state='PROGRESS')
        result = subprocess.run([naabu_path, '-p', params['port'], '-host', params['target']], stdout=subprocess.PIPE)
        # save result into database
        result = result.stdout.decode('utf-8')
        result = result.split('\n')
        for line in result:
            if line:
                line = line.split(':')
                ip = line[0]
                port = line[1]
                port_type = line[2]
                port = Port(ip=ip, port=port, port_type=port_type)
                port.save()
        # if redis.ismember('tasks.revoked', self.request.id):
        #     raise Ignore()
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Port Scan Failed")
        return e

    return "Port Scan Complete"

   