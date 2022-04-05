import abc
import functools
from typing import Callable, Any, Union, Awaitable , Optional , Dict
import requests
import json

class SyncApi:
    """
    异步 API 接口类。
    继承此类的具体实现类应实现异步的 `call_action` 方法。
    """

    @abc.abstractmethod
    def call_action(self, action: str, **params) -> Any:
        ...

    def __getattr__(self,
                    item: str) -> Callable[..., Union[Awaitable[Any], Any]]:
        """获取一个可调用对象，用于调用对应 API。"""
        return functools.partial(self.call_action, item)

class HttpApi(SyncApi):
    """
    HTTP API 实现类。
    """

    def __init__(self, api_root: Optional[str] = None, access_token: Optional[str] = None, robot_wxid: Optional[str] = None):
        super().__init__()
        self._api_root = api_root
        self._access_token = access_token
        self.robot_wxid = robot_wxid

    def call_action(self, action: str, **params) -> Any:
        if not self._api_root:
            raise 'ApiNotAvailable'

        headers = {}
        if self._access_token:
            headers['Authorization'] = self._access_token

        params['success'] = "true"
        params['event'] = action
        if params.get('robot_wxid') is None:
            params['robot_wxid'] = self.robot_wxid
        if params.get('to_wxid') is None:
            params['to_wxid'] = ''
        if params.get('msg') is None:
            params['msg'] = ''
        if params.get('group_wxid') is None:
            params['group_wxid'] = ''
        if params.get('member_wxid') is None:
            params['member_wxid'] = ''

        try:
            ret = requests.post(self._api_root, headers=headers, json=params)
            return json.loads(ret.text)
        except Exception as e:
            print(e)
            return None
