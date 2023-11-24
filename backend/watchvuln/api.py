# watchvuln/api.py

from django.http import JsonResponse
from ninja import Router
import json
from .models import WebhookEvent  # Import the WebhookEvent model

router = Router()

@router.get("/webhook")
def get_webhook_events(request):
    try:
        # Retrieve all webhook events from the database
        webhook_events = WebhookEvent.objects.all()

        # Customize the response format based on your needs
        response_data = []
        for event in webhook_events:
            event_data = {
                "event_type": event.event_type,
                "unique_key": event.unique_key,
                "title": event.title,
                "description": event.description,
                "severity": event.severity,
                "cve": event.cve,
                "disclosure": event.disclosure,
                "solutions": event.solutions,
                "references": event.references,
                "tags": event.tags,
                "from_source": event.from_source,
                "reason": event.reason,
                # Add other fields as needed
            }
            response_data.append(event_data)

        return response_data
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@router.post("/webhook", auth=None)
def webhook_receiver(request):
    try:
        # Get POST request JSON data
        data = json.loads(request.body)

        # Extract type and content from the received data
        event_type = data.get("type")
        content = data.get("content")

        # Store the received data in the database
        if event_type == "watchvuln-vulninfo":
            webhook_event = WebhookEvent.objects.create(
                event_type=event_type,
                unique_key=content.get("unique_key"),
                title=content.get("title"),
                description=content.get("description"),
                severity=content.get("severity"),
                cve=content.get("cve"),
                disclosure=content.get("disclosure"),
                solutions=content.get("solutions"),
                references=content.get("references"),
                tags=content.get("tags"),
                from_source=content.get("from"),
                reason=content.get("reason"),
                # Add other fields as needed
            )

        # Handle specific event types
        if event_type == "watchvuln-initial":
            # Handle initialization message
            version = content.get("version")
            vuln_count = content.get("vuln_count")
            interval = content.get("interval")
            providers = content.get("provider")
            
            # Add your logic to process the initialization message

        elif event_type == "watchvuln-text":
            # Handle text message
            message = content.get("message")

            # Add your logic to process the text message

        # Add more conditions if new event types are introduced

        # Return successful response
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError as e:
        # JSON parsing error
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
