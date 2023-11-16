import ipaddress
import uuid
from fuadmin.celery import app
import subprocess
from .models import Task

@app.task(name="task.tasks.get_task")
def get_task():
  return 'test'

naabu_path = 'utils/tools/naabu'
import json
import subprocess
from .models import Port, Task
from fuadmin.celery import app

naabu_path = 'utils/tools/naabu'

@app.task(name="task.tasks.portScan")
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


   