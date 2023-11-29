from django.http import JsonResponse
from ninja import Router
from .models import SecurityIntelligence  # Import the SecurityIntelligence model

router = Router()

@router.get("/webhook")
def get_webhook_events(request):
    try:
        # Retrieve all webhook events from the security_intelligence table
        security_events = SecurityIntelligence.objects.all()

        # Customize the response format based on your needs
        response_data = []
        for event in security_events:
            event_data = {
                "timestamp": event.timestamp,
                "label": event.label,
                "subject": event.subject,
                "content": event.content,
                "url": event.url,
                # Add other fields as needed
            }
            response_data.append(event_data)

        return response_data
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
