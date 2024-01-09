from .task_base import logger, system, arch, BaseTaskWithRetry, cleanUpFile
from fuadmin.celery import app
from celery.exceptions import Reject
from celery import group, chord
import subprocess, os, json, uuid, errno
from ..models import Url, Nuclei, Xray


@app.task(bind=True, name="task.tasks.pocScan", queue="pocScan", base=BaseTaskWithRetry)
def PocScan(self, task_uuid, subparams):
    logger.info("Executing POC Scan task id {0.id}".format(self.request))
    try:
        # 根据操作系统和架构选择对应的 bin 文件
        if system == 'Darwin' and arch == 'x86_64':
            nuclei_path = os.path.join('utils', 'tools', 'nuclei_macOS_amd64', 'nuclei')
            xray_path = os.path.join('utils', 'tools', 'xray_darwin_amd64', 'xray_darwin_amd64')
            xpoc_path = os.path.join('utils', 'tools', 'xpoc_darwin_amd64', 'xpoc_darwin_amd64')
        elif system == 'Darwin' and arch == 'arm64':
            nuclei_path = os.path.join('utils', 'tools', 'nuclei_macOS_arm64', 'nuclei')
            xray_path = os.path.join('utils', 'tools', 'xray_darwin_arm64', 'xray_darwin_arm64')
            xpoc_path = os.path.join('utils', 'tools', 'xpoc_darwin_arm64', 'xpoc_darwin_arm64')
        else:
            raise SystemError('Unsupported system or architecture')
        # Update task status to running
        self.update_state(state='PROGRESS', meta={'current_task': 'Poc Scan', 'status': 'Running'})
        url_objects = Url.objects.filter(task_uuid_id=task_uuid)
        random_uuid = uuid.uuid4()
        tmp_url_path = os.path.join('utils', 'tools', f'{random_uuid}_tmp_url.txt')
        with open(tmp_url_path, 'w') as f:
            for obj in url_objects:
                f.write(f"{obj.url}\n")
        scan_group = group([
                nucleiScan.s(task_uuid, nuclei_path, tmp_url_path, subparams['nuclei_level'], subparams['concurrent_templates'], subparams['bulk_size'], subparams['rate_limit']),
                xrayScan.s(task_uuid, xray_path, f'../{random_uuid}_tmp_url.txt'),
                # xpocScan.s(task_uuid, xpoc_path, f'../{random_uuid}_tmp_url.txt')
                ])
        # 创建清理任务
        cleanup_task = cleanUpFile.s(tmp_url_path)
        
        # 使用 chord 将扫描任务组和清理任务链接起来
        workflow = chord(scan_group)(cleanup_task)
        
        # 可以存储 workflow 的 id，以便以后查询状态
        workflow_id = workflow.id

    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Poc Scan Failed: {}".format(e))
        # 如果在启动工作流程之前发生异常，确保删除临时文件
        if os.path.exists(tmp_url_path):
            os.remove(tmp_url_path)
        raise e

    return "PocScan Complete"

@app.task(bind=True, name="task.tasks.nucleiScan", queue="Vuln", base=BaseTaskWithRetry)
def nucleiScan(self, task_uuid, nuclei_path, tmp_url_path, nuclei_level, concurrent_templates, bulk_size, rate_limit):
    logger.info("Executing Nuclei Scan task id {0.id}".format(self.request))
    self.update_state(state='PROGRESS', meta={'current_task': 'Nuclei Scan', 'status': 'Running'})
    random_uuid = uuid.uuid4()
    try: 
        logger.info("Nuclei Scan: {}".format(nuclei_path))
        result = subprocess.run([nuclei_path, '-l', tmp_url_path, '-nss', '-je', f'utils/tools/{random_uuid}.json', '-duc', '-severity', ','.join(nuclei_level), '-retries', '1', '-project', '-c', concurrent_templates, '-bulk-size', bulk_size, '-rate-limit', rate_limit], stdout=subprocess.PIPE)
        json_result_file = f'utils/tools/{random_uuid}.json'
        if result.stdout:
            # 存入数据库
            with open(json_result_file, 'r') as f:
                results = json.loads(f.read())
                for result in results:
                    nuclei = Nuclei(task_uuid_id=task_uuid, template=result.get('template', 'Unknown'), template_url=result.get('template-url', 'Unknown'), template_id=result.get('template-id', 'Unknown'), template_path=result.get('template-path', 'Unknown'), template_encoded=result.get('template-encoded', 'Unknown'), name=result['info'].get('name', 'Unknown'), author=result['info'].get('author', 'Unknown'), tags=result['info'].get('tags', 'Unknown'), severity=result['info'].get('severity', 'Unknown'), type=result.get('type', 'Unknown'), host=result.get('host', 'Unknown'), port=result.get('port', 'Unknown'), scheme=result.get('scheme', 'Unknown'), url=result.get('url', 'Unknown'), matched_at=result.get('matched-at', 'Unknown'), request=result.get('request', 'Unknown'), response=result.get('response', 'Unknown'), ip=result.get('ip', 'Unknown'), timestamp=result.get('timestamp', 'Unknown'), curl_command=result.get('curl-command', 'Unknown'), matcher_status=result.get('matcher-status', 'Unknown'))
                    nuclei.save()
            # 删除临时文件
            os.remove(json_result_file)
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Nuclei Scan Failed: {}".format(e))
        raise e
    
    return "Nuclei Scan Complete"

@app.task(bind=True, name="task.tasks.xrayScan", queue="Vuln", base=BaseTaskWithRetry)
def xrayScan(self, task_uuid, xray_path, tmp_url_path):
    logger.info("Executing Xray Scan task id {0.id}".format(self.request))
    self.update_state(state='PROGRESS', meta={'current_task': 'Xray Scan', 'status': 'Running'})
    random_uuid = uuid.uuid4()
    try:
        logger.info("Xray Scan: {}".format(xray_path))
        # 使用subprocess.run的cwd参数来设置工作目录
        result = subprocess.run(
            [os.path.join('.', os.path.basename(xray_path)), 'ws', '--uf', tmp_url_path, '--json-output', f'../{random_uuid}.json'],
            stdout=subprocess.PIPE,
            cwd=os.path.dirname(xray_path)  # 设置工作目录为xray的目录
        )
        logger.info("Xray Scan Result: {}".format(result))
        json_result_file = f'utils/tools/{random_uuid}.json'
        if result.stdout:
            # 存入数据库
            with open(json_result_file, 'r') as f:
                results = json.loads(f.read())
                for result in results:
                    xray = Xray(task_uuid_id=task_uuid, create_time=result.get('create_time', 'Unknown'), addr=result['detail'].get('addr', 'Unknown'), payload=result['detail'].get('payload', 'Unknown'), snapshot=result['detail'].get('snapshot', 'Unknown'), extra=result['detail'].get('extra', 'Unknown'), plugin=result.get('plugin', 'Unknown'), url=result['target'].get('url', 'Unknown'))
                    xray.save()
            # 删除临时文件
            os.remove(json_result_file)
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Nuclei Scan Failed: {}".format(e))
        raise e
    
    return "Xray Scan Complete"

