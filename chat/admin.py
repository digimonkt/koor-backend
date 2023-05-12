from django.contrib import admin
from .models import Conversation, ConversationUser, ChatMessage

admin.site.register(Conversation)
admin.site.register(ConversationUser)
admin.site.register(ChatMessage)

