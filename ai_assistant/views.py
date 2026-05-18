import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from analytics.models import UserActivity

from .models import Conversation, Message
from .services import generate_ai_response


@login_required
def chat_view(request):
    conversations = Conversation.objects.filter(user=request.user)[:20]
    active_id = request.GET.get('conversation')
    active = None
    messages_list = []

    if active_id:
        active = get_object_or_404(Conversation, pk=active_id, user=request.user)
        messages_list = active.messages.all()
    elif conversations.exists():
        active = conversations.first()
        messages_list = active.messages.all()

    messages_list_data = [
        {'role': m.role, 'content': m.content}
        for m in messages_list
    ]

    return render(request, 'ai_assistant/chat.html', {
        'conversations': conversations,
        'active_conversation': active,
        'chat_messages': messages_list,
        'messages_list_data': messages_list_data,
    })


@login_required
@require_POST
def send_message_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    content = data.get('message', '').strip()
    conversation_id = data.get('conversation_id')
    context = data.get('context', '')

    if not content:
        return JsonResponse({'error': 'Message required'}, status=400)

    if conversation_id:
        conversation = get_object_or_404(Conversation, pk=conversation_id, user=request.user)
    else:
        conversation = Conversation.objects.create(
            user=request.user,
            title=content[:60],
        )

    user_msg = Message.objects.create(
        conversation=conversation,
        role=Message.Role.USER,
        content=content,
    )

    ai_content = generate_ai_response(content, context)
    ai_msg = Message.objects.create(
        conversation=conversation,
        role=Message.Role.ASSISTANT,
        content=ai_content,
    )

    UserActivity.objects.create(
        user=request.user,
        activity_type=UserActivity.ActivityType.AI_CHAT,
        metadata={'preview': content[:80]},
    )

    return JsonResponse({
        'conversation_id': conversation.id,
        'user_message': {'id': user_msg.id, 'content': user_msg.content, 'role': 'user'},
        'assistant_message': {'id': ai_msg.id, 'content': ai_msg.content, 'role': 'assistant'},
    })


@login_required
@require_GET
def conversation_messages_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, user=request.user)
    messages_data = [
        {'id': m.id, 'role': m.role, 'content': m.content, 'created_at': m.created_at.isoformat()}
        for m in conversation.messages.all()
    ]
    return JsonResponse({'messages': messages_data})
