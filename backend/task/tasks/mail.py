from .task_base import logger, system, arch, BaseTaskWithRetry
from fuadmin.celery import app
from celery import group
from celery.exceptions import Reject
from fake_useragent import UserAgent
import requests, errno, re
from .config import pb_key

@app.task(bind=True, name="task.tasks.mailScan", queue="mailScan", base=BaseTaskWithRetry)
def MailScan(self, task_uuid, subparams):
    logger.info("Executing Mail Scan task id {0.id}".format(self.request))
    try:
        tasks = []
        for domain in subparams.get('domains').split('\n'):
            tasks.append(MailScan_Emailf.s(domain))
            tasks.append(MailScan_PhoneBook.s(domain))

        scan_group = group(tasks)
        workflow = scan_group()
        # 可以存储 workflow 的 id，以便以后查询状态
        workflow_id = workflow.id
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Finger Scan Failed: {}".format(e))
        raise e

    return "Mail Scan Complete"


@app.task(bind=True, name="task.tasks.mailScan_Emailf", queue="mailScan", base=BaseTaskWithRetry)
def MailScan_Emailf(self, domain):
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
        emails = self.match_emails(domain, resp)
        self.emails.extend(emails)
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as e:
        logger.error("Finger Scan Failed: {}".format(e))
        raise e
    


@app.task(bind=True, name="task.tasks.mailScan_PhoneBook", queue="mailScan", base=BaseTaskWithRetry)
def MailScan_PhoneBook(self, domain):
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
    
    params = {"term": self.domain,
        "maxresults": 10000,
        "media": 0,
        "target": 2,
        "timeout": 20}
    
    url = 'https://public.intelx.io/phonebook/search' + f'?k={pb_key}'
    resp = requests.post(url, headers=request_default_headers, params=params)
    if not resp:
        return set()
    if hasattr(resp, 'json'):
        id = resp.json()["id"]
        if not id:
            logger.log('ALERT', f'Get PhoneBook id fail')
            return
        params = {
            "k": pb_key,
            "id": id,
            "limit": 10000
        }
        header = self.header.update({'TE': 'trailers'})
        resp = requests.get(self.addr + '/result', params=params, headers=request_default_headers)
        if hasattr(resp, 'json'):
            emails = self.match_emails(resp)
            if emails:
                self.emails.extend(emails)
            else:
                pass


def match_emails(domain, resp):
    if not resp:
        return set()

    if hasattr(resp, 'text'):
        html = resp.text

        # 首先，确保域名中的特殊字符被正确转义
        sanitized_domain = re.escape(domain.replace('www.', ''))
        
        # 构建电子邮件匹配的正则表达式
        # 注意：这个正则表达式有所改进，但还是相对简单。电子邮件地址的完整规范非常复杂，很难用单个正则表达式完全覆盖。
        reg_emails = re.compile(
            r'[a-zA-Z0-9._%+-]+@' +  # 用户名部分
            '[a-zA-Z0-9.-]+' +       # 域名部分
            sanitized_domain         # 清理后的域名
        )

        # 查找所有匹配的电子邮件地址
        temp = reg_emails.findall(html)

        # 去重并转换为小写
        emails = set(email.lower().strip() for email in temp)

        # 处理电子邮件地址，如果以mailto:开头，则去除
        true_emails = {email.replace('mailto:', '') for email in emails}

        return true_emails

    else:
        return set()
