import json
import threading
import httpx
from typing import Dict, Any, Set
from pydantic import BaseModel, Field, HttpUrl
import socketio
import time

class PostPublishEventPayload(BaseModel):
    applicationId: str = Field(..., description="Application ID")
    channel: str = Field(..., description="ChannelID")
    data: Dict[str, Any]

class PostPublishEventResponse(BaseModel):
    message: str = Field(..., description="Message from the server")
    id: str = Field(..., description="ID of the message")

class ZenBrokerIncommingMessage(BaseModel):
    id: str = Field(..., description="ID of the message")
    channel: str = Field(..., description="Channel of the message")
    createdAt: str = Field(..., description="Created at timestamp")
    data: str = Field(..., description="Data of the message")

class ZenbrokerClient:
    def __init__(self, base_url: HttpUrl, application_id: str) -> None:
        self._url: str = str(base_url)
        self._application_id: str = str(application_id)

        self._api = httpx.Client(base_url=self._url)

        # Socket.IO client
        self._sio = socketio.Client(logger=True)
        self._sio.connect(f"{self._url}?applicationId={self._application_id}", socketio_path="/ws")
        self._sio.on("message", self._on_socket_message)
        
        # Channels
        self._channels: Set[str] = set()

        # Callbacks
        self._callbacks: list[callable] = []

    def _on_socket_message(self, data):
        _message = ZenBrokerIncommingMessage.model_validate(json.loads(data))
        for callback in self._callbacks:
            callback(_message)
    

    def on_message(self, callback: callable) -> callable:
        self._callbacks.append(callback)
        
        def unsubscribe():
            if callback in self._callbacks:
                self._callbacks.remove(callback)
        
        return unsubscribe

    def subscribe(self, channel: str) -> bool:
        if channel in self._channels:
            return False

        self._sio.emit("subscribe", channel)
        self._channels.add(channel)

        return True
    
    def unsubscribe(self, channel: str) -> bool:
        if channel not in self._channels:
            return False

        self._sio.emit("unsubscribe", channel)
        self._channels.remove(channel)
        return True
    
    def publish_ws(self, channel: str, data: Dict[str, Any]) -> bool:
        post_data: PostPublishEventPayload = PostPublishEventPayload(
            applicationId=self._application_id,
            channel=channel,
            data=data
        )
        self._sio.emit("message", data=post_data.model_dump())
        return True

    def publish(self, channel: str, data: Dict[str, Any]) -> PostPublishEventResponse:
        post_data: PostPublishEventPayload = PostPublishEventPayload(
            applicationId=self._application_id,
            channel=channel,
            data=data
        )

        response = self._api.post(
            url="/producer/emit",
            json=post_data.model_dump()
        )

        response.raise_for_status()
        result = response.json()

        return PostPublishEventResponse(
            id=result['id'],
            message=result['message']
        )
    
    def listen(self):
        """
        Keeps the Socket.IO client running and listening for messages.
        This method will not block the main thread.
        """
        def _listen():
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self._sio.disconnect()

        thread = threading.Thread(target=_listen)
        thread.start()
    
