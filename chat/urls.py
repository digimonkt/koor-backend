from django.urls import path
from chat.views import (
    ChatView, ChatRoomView,
    ConversationListView,
    ChatHistory, Attachment,
    # ChatHistory, AttachmentChatMessage, 
    # ChatRoomView, ChatUnreadMessagesView
)

app_name = "chat"

urlpatterns = [
    path("", ChatView.as_view(), name="index"),
    path("/conversations/", ConversationListView.as_view(), name="conversation_list"),
    path("/<str:room_name>", ChatRoomView.as_view(), name="chat_room"),
    # path("<str:agent_id>/attachment/", AttachmentChatMessage.as_view(), name="chat_attachment"),
    path("/<str:agent_id>/history/", ChatHistory.as_view(), name="chat_history"),
    
    path("/attachment", Attachment.as_view(), name="attachment"),
    # path("<str:agent_id>/unreads/", ChatUnreadMessagesView.as_view(), name="chat_unread"),
]
