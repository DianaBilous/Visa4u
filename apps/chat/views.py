from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Message

# @login_required
# def get_messages(request):
#     messages = Message.objects.all().order_by('timestamp')
#     messages_data = [{"user": msg.user.username, "text": msg.text, "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for msg in messages]
#     return JsonResponse({"messages": messages_data})

# @login_required
# def send_message(request):
#     if request.method == "POST":
#         text = request.POST.get("text")
#         user = request.user
#         new_message = Message.objects.create(user=user, text=text)
#         return JsonResponse({"user": new_message.user.username, "text": new_message.text, "timestamp": new_message.timestamp.strftime("%Y-%m-%d %H:%M:%S")})


@staff_member_required
def chat_room_admin_view(request, room_name):
    messages = Message.objects.filter(room=room_name).order_by('timestamp')
    return render(request, 'admin/chat_room.html', {'messages': messages, 'room_name': room_name})

@staff_member_required
def send_message_admin(request, room_name):
    if request.method == "POST":
        text = request.POST.get("text")
        user = request.user
        Message.objects.create(user=user, text=text, room=room_name, is_admin=True)
    return redirect('admin:chat_room_view', room_name=room_name)