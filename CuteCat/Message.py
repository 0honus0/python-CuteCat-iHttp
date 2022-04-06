from typing import Any

class Message:
    def __init__(self, msg : Any = None):
        self.msg = msg

    def type(self):
        if self.msg['type'] == 1:
            return 'text'
        if self.msg['type'] == 3:
            return 'image'
        if self.msg['type'] == 34:
            return 'voice'
        if self.msg['type'] == 42:
            return 'card'
        if self.msg['type'] == 43:
            return 'video'
        if self.msg['type'] == 47:
            return 'animated_sticker'
        if self.msg['type'] == 48:
            return 'location'
        if self.msg['type'] == 49:
            return 'share'
        if self.msg['type'] == 50:
            return 'voip'
        if self.msg['type'] == 2000:
            return 'transfer'
        if self.msg['type'] == 2001:
            return 'redpacket'
        if self.msg['type'] == 2002:
            return 'miniprogram'
        if self.msg['type'] == 2003:
            return 'group_invite'
        if self.msg['type'] == 10002:
            return 'multivoip'

    def __str__(self):
        return self.msg

    def __repr__(self):
        return str(self.msg)
