from fuadmin.celery import app
from celery.exceptions import Reject, Ignore
from celery.utils.log import get_task_logger
from celery.worker.request import Request
from celery import group, states, chord
from celery import Task as CeleryTask
import os
from fake_useragent import UserAgent
import requests
import config

## 公网信息收集模块
logger = get_task_logger(__name__)

class MyRequest(Request):
    'A minimal custom request to log failures and hard time limits.'
    def __init__(self, *args, **kwargs):
        super(MyRequest, self).__init__(*args, **kwargs)
    def on_timeout(self, soft, timeout):
        super(MyRequest, self).on_timeout(soft, timeout)
        if not soft:
           logger.warning(
               'A hard timeout was enforced for task %s',
               self.task.name
           )

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        super().on_failure(
            exc_info,
            send_failed_event=send_failed_event,
            return_ok=return_ok
        )
        logger.warning(
            'Failure detected for task %s',
            self.task.name
        )

# 任务执行失败后重试
class BaseTaskWithRetry(CeleryTask):
    Request = MyRequest
    autoretry_for = (TypeError,)
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = False

# 清理任务
@app.task
def cleanUpFile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


class MailScan:
    def __init__(self, domains):
        self.emails = []
        self.ua = UserAgent()
        self.request_default_headers = {
            'Accept': 'text/html,application/xhtml+xml,'
                    'application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://www.google.com/',
            'User-Agent': self.ua.random,
            'Upgrade-Insecure-Requests': '1',
            'X-Forwarded-For': '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
        }
        self.domains = domains
        
    def match_emails(domain, resp):
        if not resp:
            return set()
        elif hasattr(resp, 'text'):
            html = resp.text
            import re
            # reg_emails = re.compile(r'[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + '[a-zA-Z0-9.-]*' + domain.replace('www.', ''))
            reg_emails = re.compile(r'[a-zA-Z0-9.\-_]+' + '@' + '[a-zA-Z0-9.-]*' + domain.replace('www.', ''))
            temp = reg_emails.findall(html)
            emails = list(set(temp))
            true_emails = {str(email)[1:].lower().strip().replace('mailto:', '') if len(str(email)) > 1 and str(email)[0] == '.'
                        else len(str(email)) > 1 and str(email).lower().strip() for email in emails}
            return true_emails
        else:
            return set() 

    @app.task(bind=True, name="task.tasks.mailScan_Emailf", queue="mailScan", base=BaseTaskWithRetry)
    def MailScan_Emailf(self, domain):
        resp = requests.get(f'https://www.email-format.com/d/{domain}/', headers=self.request_default_headers)
        emails = self.match_emails(domain, resp)
        self.emails.extend(emails)

    @app.task(bind=True, name="task.tasks.mailScan_PhoneBook", queue="mailScan", base=BaseTaskWithRetry)
    def MailScan_PhoneBook(self, domain):
        header = self.header.update({'Referer': 'https://phonebook.cz/',
                            'Origin': 'https://phonebook.cz',
                            'sec-ch-ua-platform': '"Windows"',
                            'Sec-Fetch-Site': 'cross-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                            'Accept': '* / *',
                            'Content-Type': 'application / json',
                            })
        
        params = {"term": self.domain,
            "maxresults": 10000,
            "media": 0,
            "target": 2,
            "timeout": 20}
        
        url = 'https://public.intelx.io/phonebook/search' + f'?k={config.pb_key}'
        resp = requests.post(url, headers=header, params=params)
        if not resp:
            return set()
        if hasattr(resp, 'json'):
            id = resp.json()["id"]
            if not id:
                logger.log('ALERT', f'Get PhoneBook id fail')
                return
            params = {
                "k": self.key,
                "id": id,
                "limit": 10000
            }
            header = self.header.update({'TE': 'trailers'})
            resp = requests.get(self.addr + '/result', params=params, headers=header)
            if hasattr(resp, 'json'):
                emails = self.match_emails(resp)
                if emails:
                    self.emails.extend(emails)
                else:
                    pass

    # @app.task(bind=True, name="task.tasks.mailScan_Snov", queue="mailScan", base=BaseTaskWithRetry)
    # def MailScan_Snov