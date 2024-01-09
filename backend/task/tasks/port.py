from .task_base import logger, system, arch, BaseTaskWithRetry, cleanUpFile
from fuadmin.celery import app
from celery.exceptions import Reject, Ignore
import subprocess, os, uuid, xml.etree.ElementTree as ET, errno
from ..models import Port

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

