from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Subscriber
from .utils import send_newsletter

class SubscriberViewSet(viewsets.ModelViewSet):
    ...
    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def send_newsletter(self, request):
        subject = request.data.get("subject", "Our Newsletter")
        message = request.data.get("message", "")
        subscribers = Subscriber.objects.filter(is_active=True).values_list("email", flat=True)
        send_newsletter(subject, message, list(subscribers))
        return Response({"status": "Newsletter sent"}, status=status.HTTP_200_OK)
