import ipaddress
import uuid
from fuadmin.celery import app
import subprocess
from .models import Task
from enum import Enum
import errno
from celery.exceptions import Reject, Ignore
from celery.utils.log import get_task_logger
from celery.worker.request import Request
from celery import group


logger = get_task_logger(__name__)


class SubTaskType(Enum):
    SUBDOMAIN_SCAN = "subdomainScan"
    # 用于识别 CDN 
    CDN_SCAN = "cdnScan"
    FINGER_SCAN = "fingerScan"
    PORT_SCAN = "portScan"
    POC_SCAN = "pocScan"
    # 在这里添加其他任务类型

class SubTask():
    def __init__(self, subtask_type, subtask_params):
        self.subtask_type = subtask_type
        self.subtask_params = subtask_params
        self.subtask_result = None
        self.celery_task_id = None  # To store Celery task ID

    def on_raw_message(body):
        print(body)

    def execute(self):
        if self.task_type == SubTaskType.SUBDOMAIN_SCAN:
            # Execute subdomain scan task and update result
            result = portScan.delay(args=self.subtask_params)
            print(result.get(on_message=self.on_raw_message, propagate=False))
        elif self.task_type == SubTaskType.CDN_SCAN:
            # Execute CDN scan task and update result
            result = "CDN scan result"
        # Add other task types here
        self.task_status = SubTaskStatus.FINISHED
        return result


class TaskManager:
    def __init__(self, task_uuid, task_params):
        self.task_uuid = task_uuid
        self.task_params = task_params
        self.task_list = []

    ### task_params 格式
    # {
    #   "task_uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    #   "if_crontab": false,
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

        for subtask_info in task_params.get("params", []):
            subtask = SubTask(subtask_info["task_type"], subtask_info.get("params", {}))
            self.task_list.append(subtask)

    def resume_subtask(self, subtask: SubTask):
        # Resume a subtask by UUID
        pass

    def pause_subtask(self, subtask: SubTask):
        # Pause a subtask by UUID
        pass

    def cancel_subtask(self, subtask: SubTask):
        # Cancel a subtask by UUID
        pass

    def execute_subtasks(self):
        g = group(subtask.execute() for subtask in self.task_list).apply_async()
        result = g()
        return result

class MyRequest(Request):
    'A minimal custom request to log failures and hard time limits.'

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
class BaseTaskWithRetry(Task):
    Request = MyRequest
    autoretry_for = (TypeError,)
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = False

@app.task(name="task.tasks.subdomainScan", queue="subdomainScan",base=BaseTaskWithRetry)
def subdomainScan(self, params):
    logger.info("Executing Subdomain Scan task id {0.id}".format(self.request))
    try:
        # Update task status to running
        self.update_state(state='PROGRESS', meta={'current': 50, 'total': 100})
        pass
        if redis.ismember('tasks.revoked', self.request.id):
            raise Ignore()
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Subdomain Scan Failed")

    return "Subdomain Scan Complete"

naabu_path = 'utils/tools/naabu'

@app.task(name="task.tasks.portScan", queue="portScan")
def portScan(target: str, port: str, task_uuid: uuid.UUID):
    # 分割输入的 IP 地址
    targets = target.split("\n")

    for ip in targets:
        # 验证 IP 地址是否合法
        try:
            ipaddress.ip_address(ip)  # 这将抛出 ValueError 如果 IP 不是有效的 IPv4 地址
        except ValueError:
            continue  # 如果 IP 地址不合法，跳过此 IP

        # 对每个合法的 IP 地址执行扫描
        process = subprocess.Popen(
            ["naabu", "-host", ip, "-p", port, "-json", "-stats", "-debug", "-v"],
            stdout=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            try:
                scan_result = json.loads(line)
                Port.objects.create(
                    task_uuid=Task.objects.get(uuid=task_uuid),
                    ip=scan_result.get("ip", ""),
                    port=str(scan_result.get("port", "")),
                    tag=scan_result.get("protocol", "")
                )
            except json.JSONDecodeError:
                # Handle possible JSON decode error
                continue

    return "Port Scan Complete"


   