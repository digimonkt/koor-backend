from django.urls import path

from .views import (
    ConversationListView, ChatHistory,
    Attachment, GetConversationView
)

app_name = "chat"

urlpatterns = [
    path("/attachment", Attachment.as_view(), name="attachment"),
    path("/conversations", ConversationListView.as_view(), name="conversation_list"),
    path("/conversations/<str:userId>", GetConversationView.as_view(), name="get_conversation"),
    path("/<str:conversationId>/history", ChatHistory.as_view(), name="chat_history"),
]
