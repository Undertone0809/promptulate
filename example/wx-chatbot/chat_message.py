from itchat.storage.messagequeue import Message


class ChatMessage(object):
    MsgId = None
    FromUSerName = None

    ToUserName = None
    Content = None
    MsgType = None
    Status = None
    ImgStatus = None
    CreateTime = None
    VoiceLength = None
    PlayLength = None
    FileName = None
    FileSize = None
    Url = None
    from_user_id = None
    from_user_nickname = None
    to_user_id = None
    to_user_nickname = None
    other_user_id = None
    other_user_nickname = None
    my_msg = False
    self_display_name = None

    is_group = False
    is_at = False
    actual_user_id = None
    actual_user_nickname = None
    at_list = None

    _prepare_fn = None
    _prepared = False
    _rawmsg = None


class ReceiveMessage(ChatMessage):
    FromUserName = None

    def __init__(self, msg: Message):
        self.msg = msg
        for key, value in self.msg.items():
            setattr(self, key, value)

    def __str__(self):
        result = "[ReceiveMessage]"
        for key, value in vars(self).items():
            result += "{}: {}\n".format(key, value)
        return result
