from django.shortcuts import render
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
def get_messages(request):
    messages = Message.objects.all().order_by('timestamp')
    messages_data = [{"user": msg.user.username, "text": msg.text, "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for msg in messages]
    return JsonResponse({"messages": messages_data})

@login_required
def send_message(request):
    if request.method == "POST":
        text = request.POST.get("text")
        user = request.user
        new_message = Message.objects.create(user=user, text=text)
        return JsonResponse({"user": new_message.user.username, "text": new_message.text, "timestamp": new_message.timestamp.strftime("%Y-%m-%d %H:%M:%S")})
