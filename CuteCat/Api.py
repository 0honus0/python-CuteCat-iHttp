import abc
import functools
from typing import Callable, Any, Union, Awaitable , Optional , Dict
import requests
import json
import logging

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

    def __init__(self, api_url: Optional[str] = None, access_token: Optional[str] = None, robot_wxid: Optional[str] = None):
        super().__init__()
        self._api_url = api_url
        self._access_token = access_token
        self.robot_wxid = robot_wxid

    def call_action(self, action: str, **params) -> Any:
        if not self._api_url:
            raise Exception('ApiNotAvailable')

        headers = {}
        if self._access_token:
            headers['Authorization'] = self._access_token

        params['success'] = "true"
        params['event'] = action
        if not params.get('robot_wxid'):
            params['robot_wxid'] = self.robot_wxid
        if not params.get('to_wxid'):
            params['to_wxid'] = ''
        if not params.get('msg'):
            params['msg'] = ''
        if not params.get('group_wxid'):
            params['group_wxid'] = ''
        if not params.get('member_wxid'):
            params['member_wxid'] = ''

        retry = 3
        while retry > 0:
            try:
                ret = requests.post(self._api_url, headers=headers, json=params)
                if  ret.json()["code"] == -1:
                    continue
                return json.loads(ret.text)
            except Exception as e:
                logging.getLogger(__name__).warning(f"call_action {action} failed: {e}")
                retry -= 1
        return None
        
