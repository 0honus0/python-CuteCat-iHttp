from typing import Any

class Message:
    def __init__(self, msg : Any = None):
        self.msg = msg

    @property
    def type(self):
        type_dict = {
            1      : 'text',
            3      : 'image',
            34     : 'voice',
            42     : 'card',
            43     : 'video',
            47     : 'animatedsticker',
            48     : 'location',
            49     : 'share',
            50     : 'voip',
            2000   : 'transfer',
            2001   : 'redpacket',
            2002   : 'miniprogram',
            2003   : 'groupinvite',
            2005   : 'revokemsg',
            10002  : 'multivoip'
        }
        return type_dict[self.msg['type']] if self.msg['type'] in type_dict else self.msg['type']


    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg
