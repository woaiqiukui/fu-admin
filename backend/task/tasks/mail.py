from .task_base import logger, system, arch, BaseTaskWithRetry
from fuadmin.celery import app
from celery import group
from celery.exceptions import Reject
from fake_useragent import UserAgent
import requests, errno
from bs4 import BeautifulSoup
from .config import pb_key
from ..models import Mail


@app.task(bind=True, name="task.tasks.mailScan", queue="mailScan", base=BaseTaskWithRetry)
def MailScan(self, task_uuid, subparams):
    logger.info("Executing Mail Scan task id {0.id}".format(self.request))
    try:
        tasks = []
        for domain in subparams.get('domains').split('\n'):
            tasks.append(MailScan_Emailf.s(task_uuid, domain))
            tasks.append(MailScan_PhoneBook.s(task_uuid, domain))

        scan_group = group(tasks)
        result = scan_group.apply_async()

    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Finger Scan Failed: {}".format(e))
        raise e

    return "Mail Scan Start"


@app.task(bind=True, name="task.tasks.mailScan_Emailf", queue="mailScan", base=BaseTaskWithRetry)
def MailScan_Emailf(self, task_uuid, domain):
    request_default_headers = {
            'Accept': 'text/html,application/xhtml+xml,'
                    'application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://www.google.com/',
            'User-Agent': UserAgent().random,
            'Upgrade-Insecure-Requests': '1',
            'X-Forwarded-For': '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
        }
    logger.info("Executing Emailf Scan task id {0.id}".format(self.request))
    try:
        resp = requests.get(f'https://www.email-format.com/d/{domain}/', headers=request_default_headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        email_divs = soup.find_all('div', class_='fl')
        emails = set(div.get_text().strip() for div in email_divs if '@' in div.get_text())
        # 存入数据库
        for email in emails:
            mail = Mail(task_uuid_id=task_uuid, domain=domain, email=email)
            mail.save()
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Emailf Scan Failed: {}".format(e))
        raise e
    
    return "Emailf Scan Complete"

@app.task(bind=True, name="task.tasks.mailScan_PhoneBook", queue="mailScan", base=BaseTaskWithRetry)
def MailScan_PhoneBook(self, task_uuid, domain):
    request_default_headers = {
                        'Referer': 'https://phonebook.cz/',
                        'Origin': 'https://phonebook.cz',
                        'sec-ch-ua-platform': '"Windows"',
                        'Sec-Fetch-Site': 'cross-site',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Dest': 'empty',
                        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                        'Accept': '* / *',
                        'Content-Type': 'application / json',
                        }
    
    params = {"term": domain,
        "maxresults": 10000,
        "media": 0,
        "target": 2,
        "terminate":"[null]",
        "timeout": 20}
    
    url = 'https://2.intelx.io/phonebook/search' + f'?k={pb_key}'
    resp = requests.post(url=url, headers=request_default_headers, json=params)
    if resp.status_code == 402:
        logger.error(f"PhoneBook Daily limit reached.")
        return "PhoneBook Scan Failed"
    elif resp.status_code == 200:
        id = resp.json().get('id')
        logger.info(f"PhoneBook Scan id: {id}")
        params = {
            "k": pb_key,
            "id": id,
            "limit": 10000
        }
        resp = requests.get(self.addr + '/result', params=params, headers=request_default_headers,
                            verify=False,
                            proxies={'https': 'http://127.0.0.1:8080'})
        logger.info(f"PhoneBook Scan result: {resp.text}")
        try:
            json_data = resp.json()
        except ValueError:  # 包括简单的json解码失败
            return "PhoneBook Scan Failed"
        
        # 提取电子邮件地址
        emails = [selector['selectorvalue'] for selector in json_data.get('selectors', []) if selector.get('selectortypeh') == 'Email Address']
        logger.info(f"PhoneBook Scan emails: {emails}")
        # 存入数据库
        for email in emails:
            mail = Mail(task_uuid_id=task_uuid, domain=domain, email=email)
            mail.save()
    else:
        logger.error(f"PhoneBook Scan Failed: {resp.status_code}")
        return "PhoneBook Scan Failed"

    return "PhoneBook Scan Complete"
