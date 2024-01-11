from django.test import TestCase
from celery.utils.log import get_task_logger
from .task_route import TaskManager
import uuid

logger = get_task_logger(__name__)

# Create your tests here.
test_params = {
      "task_uuid": "0f32536057ce4d34acb629db7ebaeb1f",
      "if_crontab": False,
      "params": [
        # {
        #   "subtask_type": "SubdomainScan",
        #   "subparams": {
        #     "target": "www.baidu.com\nwww.google.com"
        #   }
        # },
        # {
        #   "subtask_type": "PortScan",
        #   "subparams": {
        #     "target": "127.0.0.1\n47.100.82.223",
        #     "port": "1-10000"
        #   },
        # },
        # {
        #    "subtask_type": "UrlScan",
        # },
        # {
        #     "subtask_type": "FingerScan",
        # },
        # {
        #     "subtask_type": "WeakPasswordScan",
        # },
        # {
        #     "subtask_type": "PocScan",
        #     "subparams": {
        #         "nuclei_level": ["critical"],
        #         "concurrent_templates": "50",
        #         "bulk_size": "50",
        #         "rate_limit": "300",
        #     }
        # },
        {
            "subtask_type": "MailScan",
            "subparams": {
                "domains": "dbappsecurity.com.cn\ncztv.com",
            }
        }
      ]
    }

test_uuid = uuid.uuid4()

class TaskManagerTest(TestCase):
    def test_pocScan(self):
        self.task = TaskManager(test_uuid, test_params)
        if self.task.create_subtask_group():
            result = self.task.subtask_result.get()
        self.assertEqual(result, None)
