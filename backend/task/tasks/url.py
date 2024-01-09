from .task_base import logger, system, arch, BaseTaskWithRetry
from fuadmin.celery import app
from celery.exceptions import Reject
import subprocess, os, json, errno
from ..models import Port, Url

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

