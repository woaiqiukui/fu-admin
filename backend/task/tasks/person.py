from .task_base import logger, system, arch, BaseTaskWithRetry
from fuadmin.celery import app
from celery import group
from celery.exceptions import Reject
import errno, requests
from fake_useragent import UserAgent
from .config import maimai_cookie
from urllib.parse import quote
from ..models import Person

@app.task(bind=True, name="task.tasks.personScan", queue="personScan", base=BaseTaskWithRetry)
def PersonScan(self, task_uuid, subparams):
    logger.info("Executing Person Scan task id {0.id}".format(self.request))
    try:
        tasks = []
        tasks.append(personScan_Maimai.s(task_uuid, subparams.get('title')))

        scan_group = group(tasks)
        result = scan_group.apply_async()

    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Poc Scan Failed: {}".format(e))
        raise e
    
    return "PersonScan Complete"


@app.task(bind=True, name="task.tasks.personScan_Maimai", queue="personScan", base=BaseTaskWithRetry)
def personScan_Maimai(self, task_uuid, title):
    request_default_headers = {
            'Cookie': maimai_cookie,
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': UserAgent().random,
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://maimai.cn/web/search_center?type=contact&query=%E6%96%B0%E8%93%9D%E7%BD%91&highlight=true',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7'
        }
    logger.info("Executing Maimai Scan task id {0.id}".format(self.request))
    try:
        url_encoded_title = quote(title)
        for page in range(6):
            logger.info(f"Executing Maimai Scan page {page}".format(self.request))
            url = f'https://maimai.cn/search/contacts?&query={url_encoded_title}&count=20&page={page}&dist=0&searchTokens=&highlight=true&jsononly=1&pc=1'
            resp = requests.get(url=url, headers=request_default_headers)
            if resp.status_code == 200:
                contacts = resp.json().get('data').get('contacts')
                for contact in contacts:
                    person = Person(task_uuid_id=task_uuid, title=title, contact=contact)
                    person.save()
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Maimai Scan Failed: {}".format(e))
        raise e
    
    return "Maimai Scan Complete"