from django.test import TestCase
from celery.utils.log import get_task_logger
from .tasks import TaskManager
import uuid

logger = get_task_logger(__name__)

# Create your tests here.
test_params = {
      "task_uuid": "0f32536057ce4d34acb629db7ebaeb1f",
      "if_crontab": True,
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
        #         nuclei_level: ["info", "low", "medium", "high", "critical", "unknown"],
        #     }
        # },
        {
            "subtask_type": "CrontabTest",
        }
      ]
    }

test_uuid = uuid.uuid4()

class TaskManagerTest(TestCase):


    def test_portScan(self):
        logger.debug("test_portScan")
        self.task = TaskManager(test_uuid, test_params)
        if test_params["if_crontab"]:
          from django_celery_beat.models import CrontabSchedule, PeriodicTask
          crontab = CrontabSchedule.objects.create(
            minute="*/1",
            hour="*",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*"
          )
          task = PeriodicTask.objects.create(
            crontab=crontab,
            name="test",
            task="task.tasks.crontabTest",
            args="[]",
            kwargs="{}"
          )
        else:
          if self.task.create_subtask_group():
            result = self.task.subtask_result.get()
        self.assertEqual(result, None)




        
