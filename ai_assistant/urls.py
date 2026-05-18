from django.urls import path

from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message_view, name='send'),
    path('conversation/<int:pk>/messages/', views.conversation_messages_view, name='messages'),
]
