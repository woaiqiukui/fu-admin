from celery import group
from .tasks.finger import FingerScan
from .tasks.mail import MailScan
from .tasks.person import PersonScan
from .tasks.poc import PocScan
from .tasks.port import PortScan
from .tasks.url import UrlScan
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

class TaskManager:
    def __init__(self, task_params):
        self.task_uuid = task_params['task_uuid']
        self.task_params = task_params
        self.task_list = []
        self.subtask_result = None
        self.task_mapping = {
            # 公网任务
            # 'COMPANY_SCAN': lambda subparams: CompanyScan.s(self.task_uuid, subparams),
            'MailScan': lambda subparams: MailScan.s(self.task_uuid, subparams),
            'PersonScan': lambda subparams: PersonScan.s(self.task_uuid, subparams),
            # 'SubdomainScan': lambda subparams: SubdomainScan.s(subparams, self.task_uuid),
            # 'CdnScan': lambda subparams: CdnScan.s(self.task_uuid, subparams),

            # 内网任务
            'FingerScan': lambda subparams: FingerScan.s(self.task_uuid, subparams),
            'PortScan': lambda subparams: PortScan.s(self.task_uuid, subparams),
            'UrlScan': lambda subparams: UrlScan.s(self.task_uuid, subparams),
            'PocScan': lambda subparams: PocScan.s(self.task_uuid, subparams),
            # 'WeakPasswordScan': lambda subparams: WeakPasswordScan.s(self.task_uuid, subparams),
        }

    def create_subtask_group(self):
        try:
            for param in self.task_params['params']:
                subtask_type = param['subtask_type']
                subparams = param.get('subparams')
                if subtask_type in self.task_mapping:
                    task_func = self.task_mapping[subtask_type]
                    task = task_func(subparams)
                    self.task_list.append(task)

            job = group(*self.task_list)
            self.subtask_result = job.apply_async()
            return self.subtask_result
        except Exception as e:
            # 这里你可以记录异常，或者根据你的需求进行处理
            logger.error(f"Error creating subtask group: {e}")
            return None  # 或者抛出异常

    def get_task_state(self):
        # 确保在获取状态和结果之前，任务组已经创建并且有结果对象
        if not self.subtask_result:
            raise ValueError("Subtask group has not been created or no result available")
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
    
    # 同样，确保在获取结果之前任务组已经创建
    def get_completed_count(self):
        if not self.subtask_result:
            raise ValueError("Subtask group has not been created or no result available")
        return self.subtask_result.completed_count()

    def get_task_result(self):
        if not self.subtask_result:
            raise ValueError("Subtask group has not been created or no result available")
        return self.subtask_result.get()

    def revoke_task(self):
        if not self.subtask_result:
            raise ValueError("Subtask group has not been created or no result available")
        self.subtask_result.revoke()
        return 'SUCCESS'

    def revoke_subtask(self, subtask_id):
        if not self.subtask_result:
            raise ValueError("Subtask group has not been created or no result available")
        self.subtask_result.revoke(subtask_id)
        return 'SUCCESS'
    

