import os, platform
import uuid
import json
from fuadmin.celery import app
import subprocess
from .models import Port, Task, Url, Finger
from enum import Enum
import errno
from celery.exceptions import Reject, Ignore
from celery.utils.log import get_task_logger
from celery.worker.request import Request
from celery import group, states
from celery import Task as CeleryTask
import xml.etree.ElementTree as ET


logger = get_task_logger(__name__)
# 检测当前的操作系统和架构
system = platform.system()
arch = platform.machine()

class SubTaskType(Enum):
    SUBDOMAIN_SCAN = "SubdomainScan"
    # 用于识别 CDN 
    CDN_SCAN = "CDNScan"
    FINGER_SCAN = "FingerScan"
    PORT_SCAN = "PortScan"
    URL_SCAN = "UrlScan"
    POC_SCAN = "PocScan"
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
            if 'subparams' in param:
                subparams = param['subparams']
            if subtask_type == 'SubdomainScan':
                self.task_list.append(SubdomainScan.s(subparams, self.task_params['task_uuid']))
            elif subtask_type == 'PortScan':
                for target in subparams['target'].split('\n'):
                    self.task_list.append(PortScan.s(target, subparams['port'], self.task_params['task_uuid']))
            elif subtask_type == 'UrlScan':
                self.task_list.append(UrlScan.s(self.task_params['task_uuid']))
            elif subtask_type == 'FingerScan':
                self.task_list.append(FingerScan.s(self.task_params['task_uuid']))

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
def SubdomainScan(self, params, task_uuid):
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


def HostCollisionScan():
    pass

def CDNScan():
    pass

def DnsBruteForceScan():
    pass

def HistoricalDomainQuery():
    pass

def FofaScan():
    pass

def HunterScan():
    pass

def QuakeScan():
    pass




# portScan params
# test_params = {
#       "task_uuid": "0f32536057ce4d34acb629db7ebaeb1f",
#       "if_crontab": False,
#       "params": [
#         {
#           "subtask_type": "portScan",
#           "subparams": {
#             "target": "127.0.0.1\n47.100.82.223",
#             "port": "1-10000"
#           },
#         }
#       ]
#     }
@app.task(bind=True, name="task.tasks.portScan", queue="portScan", base=BaseTaskWithRetry)
def PortScan(self, target, port, task_uuid):
    logger.info("Executing Port Scan task id {0.id}".format(self.request))
    try:
        # 根据操作系统和架构选择对应的 bin 文件
        if system == 'Darwin' and arch == 'x86_64':
            naabu_path = os.path.join('utils', 'tools', 'naabu_macOS_amd64', 'naabu')
        elif system == 'Darwin' and arch == 'arm64':
            naabu_path = os.path.join('utils', 'tools', 'naabu_macOS_arm64', 'naabu')
        else:
            raise SystemError('Unsupported system or architecture')
        # Update task status to running
        self.update_state(state='PROGRESS', meta={'current_task': 'Port Scan', 'status': 'Running'})
        random_uuid = uuid.uuid4()
        result = subprocess.run([naabu_path, '-p', port, '-host', target, '-nmap-cli', 'nmap -sS -sV -oX utils/tools/{}.xml'.format(random_uuid)], stdout=subprocess.PIPE)
        # 解析XML文件
        tree = ET.parse('utils/tools/{}.xml'.format(random_uuid))
        logger.info("Port Scan Result: {}".format(tree))
        root = tree.getroot()
        for host in root.findall('host'):
            address = host.find('address').attrib.get('addr', 'Unknown')
            for port in host.find('ports').findall('port'):
                port_id = port.attrib.get('portid', 'Unknown')
                protocol = port.attrib.get('protocol', 'Unknown')
                state = port.find('state').attrib.get('state', 'Unknown')
                service_element = port.find('service')
                if service_element is not None:
                    service = port.find('service').attrib.get('name', 'Unknown')
                    product = port.find('service').attrib.get('product', 'Unknown')
                    version = port.find('service').attrib.get('version', 'Unknown')
                else:
                    service = 'Unknown'
                    product = 'Unknown'
                    version = 'Unknown'
                # 插入数据库
                port = Port(task_uuid_id=task_uuid, address=address, port=port_id, protocol=protocol, state=state, service=service, product=product, version=version)
                port.save()
        # 删除 xml
        os.remove('utils/tools/{}.xml'.format(random_uuid))
        # if redis.ismember('tasks.revoked', self.request.id):
        #     raise Ignore()
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Port Scan Failed: {}".format(e))
        raise e

    return "Port Scan Complete"


@app.task(bind=True, name="task.tasks.urlScan", queue="urlScan", base=BaseTaskWithRetry)
def UrlScan(self, task_uuid):
    logger.info("Executing Url Scan task id {0.id}".format(self.request))
    try:
        # 根据操作系统和架构选择对应的 bin 文件
        if system == 'Darwin' and arch == 'x86_64':
            httpx_path = os.path.join('utils', 'tools', 'httpx_macOS_amd64', 'httpx')
        elif system == 'Darwin' and arch == 'arm64':
            httpx_path = os.path.join('utils', 'tools', 'httpx_macOS_arm64', 'httpx')
        else:
            raise SystemError('Unsupported system or architecture')
        # Update task status to running
        self.update_state(state='PROGRESS', meta={'current_task': 'Url Scan', 'status': 'Running'})
        port_objects = Port.objects.filter(task_uuid_id=task_uuid)
        address_port_list = []
        for obj in port_objects:
            address_port = obj.address + ':' + obj.port
            address_port_list.append(address_port)
        address_port_str = ','.join(address_port_list)
        result = subprocess.run([httpx_path, '-json', '-u', address_port_str, '-fl', '0', '-mc' ,'200,302,403,404,204,303,400,401,405'], stdout=subprocess.PIPE)
        if result.stdout:
            # 存入数据库
            result_lines = result.stdout.decode().splitlines()
            json_results = [json.loads(line) for line in result_lines]
            for json_result in json_results:
                url = Url(task_uuid_id=task_uuid, port=json_result.get('port', 'Unknown'), url=json_result.get('url', 'Unknown'), title=json_result.get('title', 'Unknown'), scheme=json_result.get('scheme', 'Unknown'), webserver=json_result.get('webserver', 'Unknown'), content_type=json_result.get('content_type', 'Unknown'), method=json_result.get('method', 'Unknown'), host=json_result.get('host', 'Unknown'), path=json_result.get('path', 'Unknown'), time=json_result.get('time', 'Unknown'), status_code=json_result.get('status_code', 'Unknown'))
                url.save()
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Port Scan Failed: {}".format(e))
        raise e

    return "Url Scan Complete"


@app.task(bind=True, name="task.tasks.fingerScan", queue="fingerScan", base=BaseTaskWithRetry)
def FingerScan(self, task_uuid):
    logger.info("Executing Finger Scan task id {0.id}".format(self.request))
    try:
        random_uuid = uuid.uuid4()
        # 根据操作系统和架构选择对应的 bin 文件
        if system == 'Darwin' and arch == 'x86_64':
            observer_ward_path = os.path.join('utils', 'tools', 'observer_ward_apple-darwin', 'observer_ward')
        elif system == 'Darwin' and arch == 'arm64':
            observer_ward_path = os.path.join('utils', 'tools', 'observer_ward_aarch64-apple-darwin', 'observer_ward')
        else:
            raise SystemError('Unsupported system or architecture')
        # Update task status to running
        self.update_state(state='PROGRESS', meta={'current_task': 'Finger Scan', 'status': 'Running'})
        url_objects = Url.objects.filter(task_uuid_id=task_uuid)
        # Create file path
        if system == 'Darwin' and arch == 'x86_64':
            file_path = os.path.join('utils', 'tools', 'observer_ward_apple-darwin', f"{random_uuid}.txt")
            result_path = os.path.join('utils', 'tools', 'observer_ward_apple-darwin', f"{random_uuid}.json")
        elif system == 'Darwin' and arch == 'arm64':
            file_path = os.path.join('utils', 'tools', 'observer_ward_aarch64-apple-darwin', f"{random_uuid}.txt")
            result_path = os.path.join('utils', 'tools', 'observer_ward_aarch64-apple-darwin', f"{random_uuid}.json")

        # Open file in write mode
        with open(file_path, "w") as file:
            # Write each API to a new line
            for obj in url_objects:
                file.write(f"{obj.url}\n")

        result = subprocess.run([observer_ward_path, '-f', file_path, '-j', result_path], stdout=subprocess.PIPE)
        if result.stdout:
            # 存入数据库
            with open(result_path, 'r') as f:
                results = json.loads(f.read())
                for result in results:
                    url = Finger(task_uuid_id=task_uuid, url=result.get('url', 'Unknown'), name=result.get('name', 'Unknown'), priority=result.get('priority', 0), length=result.get('length', 0), title=result.get('title', 'Unknown'), status_code=result.get('status_code', 0), is_web=result.get('is_web', False))
                    url.save()

        # 删除临时文件
        os.remove(file_path)
        os.remove(result_path)
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Finger Scan Failed: {}".format(e))
        raise e

    return "Finger Scan Complete"


def weakpassScan():
    pass

def pocScan():
    pass

