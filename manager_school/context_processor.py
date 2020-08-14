def get_unread_chats_count(request):
    if request.user.is_authenticated:
        return {'unreaded_dialogs_counter': request.user.chat_set.unreaded(user=request.user).count()}
    else:
        return {'unreaded_dialogs_counter': 0}
