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
            "target": "127.0.0.1,10.32.129.178",
            "port": "1-10000"
          },
        }
      ]
    }

test_uuid = uuid.uuid4()

class TaskManagerTest(TestCase):


    def test_portScan(self):
        logger.debug("test_portScan")
        self.task = TaskManager(test_uuid, test_params)
        self.task.create_subtask_group()
        result = self.task.subtask_result.get()
        self.assertEqual(result, None)




        
