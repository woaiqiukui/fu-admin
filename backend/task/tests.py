from django.test import TestCase
from celery.utils.log import get_task_logger
from .tasks import TaskManager
import uuid

logger = get_task_logger(__name__)

# Create your tests here.
test_params = {
      "task_uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "if_crontab": False,
      "params": [
        {
          "subtask_type": "subdomainScan",
          "subparams": {
            "target": "www.baidu.com\nwww.google.com"
          }
        },
        {
          "subtask_type": "portScan",
          "subparams": {
            "target": "www.baidu.com\nwww.google.com"
          }
        }
      ]
    }

test_uuid = uuid.uuid4()

class TaskManagerTest(TestCase):
    def setUp(self):
        logger.debug("setUp")
        self.task = TaskManager(test_uuid, test_params)
        self.task.create_subtask_group()

    def test_get_task_state(self):
        logger.debug("test_get_task_status")
        result = self.task.get_task_state()
        print(result)
        self.assertEqual(result, "PENDING")

    def test_get_completed_count(self):
        logger.debug("test_get_completed_count")
        result = self.task.get_completed_count()
        self.assertEqual(result, 0)

    def test_get_subtask_result(self):
        logger.debug("test_get_subtask_result")
        result = self.task.get_task_result()
        self.assertEqual(result, None)


        
