from flask import Flask, request, abort, jsonify, Response
from typing import List, Callable , Coroutine , Dict , Any
from .Event import Event
from .Message import Message
from .Bus import EventBus
from .Api import SyncApi , HttpApi
import logging

class CuteCat(SyncApi):

    def __init__(self , api_root : str = None , robot_wxid : str = None ,access_token : str = None) :
        self._bus = EventBus()
        self._server_app = Flask(__name__)
        self._server_app.add_url_rule('/event', methods=['POST'],view_func=self._handle_event)
        self.logger = self._server_app.logger
        self.api_root = api_root
        if not access_token:
            self._api = HttpApi(api_root = api_root , robot_wxid = robot_wxid)
        else:
            self._api = HttpApi(api_root = api_root , access_token = access_token , robot_wxid = robot_wxid)
        
    def on(self , *event_type : str) -> Callable:
        def deco(func: Callable) -> Callable:
            for _type in event_type:
                self.subscribe( _type , func)
            return deco
        return deco
    
    def subscribe(self, event_name: str, func: Callable) -> None:
        self._bus.subscribe(event_name, func)

    def call_action(self , action : str , **params):
        return self._api.call_action(action , **params)

    def _handle_event(self) -> Any:
        payload = request.json

        ev = Event.from_payload(payload)
        if not ev:
            return

        event_type = ev.type
        self.logger.info(f'received event: {event_type}')

        message = Message(ev)
        ev['type'] = message.type
        if message.type in ['image' , 'voice' , 'video' , 'share']:
            ev['msg'] = self.url_preprocess(ev)
        results = self._bus.emit(event_type, ev)
        res = results[0] if results else None
        return jsonify(res)

    def url_preprocess(self , msg : str):
        path = msg['msg']
        if '\\WeChat' in path:
            path = '/WeChat'+ path.split('\\WeChat')[-1].replace('\\', '/')
            return self.api_root + path
        else:
            return path

    def run(self,
            host: str = '0.0.0.0',
            port: int = 18888,
            *args,
            **kwargs) -> None:
        """运行 bot 对象，实际就是运行 Flask app，参数与 `Flask.run` 一致。"""
        if 'use_reloader' not in kwargs:
            kwargs['use_reloader'] = False
        self._server_app.run(host=host, port=port, *args, **kwargs)

    