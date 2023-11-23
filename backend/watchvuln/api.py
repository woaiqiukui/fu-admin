# watchvuln/api.py

from django.http import JsonResponse
import json
from ninja import Router

router = Router()

@router.post("/webhook")
def webhook_receiver(request):
    try:
        # 获取POST请求中的JSON数据
        data = json.loads(request.body)
        
        # 在这里进行您的数据处理逻辑，例如筛选、存储等
        
        # 返回成功响应
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError as e:
        # JSON解析错误
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
