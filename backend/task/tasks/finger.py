from .task_base import logger, system, arch, BaseTaskWithRetry
from fuadmin.celery import app
from celery.exceptions import Reject
import subprocess, os, json, uuid, errno
from ..models import Finger, Url


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

