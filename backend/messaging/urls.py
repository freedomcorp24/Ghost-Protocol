# ...
from . import web_views

urlpatterns = [
    # existing ...
    path('webChat/', web_views.web_chat_page, name='web_chat'),
    path('webChatList/', web_views.web_chat_list, name='web_chat_list'),
    path('webChatSend/', web_views.web_chat_send, name='web_chat_send'),

    path('webGroupChat/', web_views.web_group_chat_page, name='web_group_chat'),
    path('webGroupList/<int:group_id>/', web_views.web_group_list, name='webGroupList'),
    path('webGroupSend/<int:group_id>/', web_views.web_group_send, name='webGroupSend'),

    path('webArchived/', web_views.web_archived_page, name='web_archived'),
    path('webArchivedList', web_views.web_archived_list, name='web_archived_list'),
    path('webUnarchive/<int:msg_id>/', web_views.web_unarchive, name='webUnarchive'),
    # ...
]
