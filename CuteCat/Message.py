from typing import Any

class Message:
    def __init__(self, msg : Any = None):
        self.msg = msg

    @property
    def type(self):
        type_dict = {
            0      : 'eventnotify', # 成员变更 面对面付款
            1      : 'text',
            3      : 'image',
            34     : 'voice',
            35     : 'qqmail',
            37     : 'friendrequest',
            42     : 'card',
            43     : 'video',
            47     : 'animatedsticker',
            48     : 'location',
            49     : 'share',
            50     : 'voip',
            106    : 'sysnotify',   # system notification 修改群名称
            2000   : 'transfer',
            2001   : 'redpacket',
            2002   : 'miniprogram',
            2003   : 'groupinvite',
            2005   : 'revokemsg',
            2006   : 'groupannouncement',
            10000  : 'sysmsg',      # 拍一拍 语音消息 撤回消息 等等 , 通过SendOutMsg接收
            10002  : 'other'        # multivoip , taptap , ClientCheckConsistency
        }
        return type_dict[self.msg['type']] if self.msg['type'] in type_dict else self.msg['type']


    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg
