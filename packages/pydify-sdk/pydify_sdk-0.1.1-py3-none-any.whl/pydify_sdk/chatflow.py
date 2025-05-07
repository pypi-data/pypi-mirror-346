import json
from typing import Any, Optional

import requests
from pydantic import BaseModel
from sseclient import SSEClient

from .base import REQUEST_TIME_OUT, DifySDK, ModelType
from .constants.base import HttpMethod
from .schema import (
    ChatFlowResponse,
    ChatFlowStreamResponse,
    ChatHistoryResponse,
    ChatListResponse,
    ChatSuggestedResponse,
    FileInput,
)


class DifyChatFlow(DifySDK):
    def _build_data(
        self, query: str, conversation_id: str, data: Optional[dict | ModelType], files: Optional[list[FileInput]]
    ) -> dict:
        return {
            "query": query,
            "conversation_id": conversation_id,
            "inputs": data.model_dump() if isinstance(data, BaseModel) else (data or {}),
            "files": files,
        }

    def chat(
        self,
        user: str,
        query: str,
        *,
        conversation_id: str = "",
        data: Optional[dict | ModelType] = None,
        files: Optional[list[FileInput]] = None,
    ) -> ChatFlowStreamResponse:
        """
        对话(流式返回)
        @return: ChatFlowStreamResponse
        """
        request_data = self._build_data(query, conversation_id, data, files)
        response = self.request("chat-messages", user, data=request_data, stream=True, model=ChatFlowStreamResponse)
        return response  # type: ignore

    def sync_chat(
        self,
        user: str,
        query: str,
        *,
        conversation_id: str = "",
        data: Optional[dict | ModelType] = None,
        files: Optional[list[FileInput]] = None,
    ) -> ChatFlowResponse:
        """
        对话(同步返回)
        @return: ChatFlowResponse
        """
        request_data = self._build_data(query, conversation_id, data, files)
        response = self.request("chat-messages", user, data=request_data, model=ChatFlowResponse)
        return response  # type: ignore

    def async_chat(
        self,
        user: str,
        query: str,
        *,
        conversation_id: str = "",
        data: Optional[dict | ModelType] = None,
        files: Optional[list[FileInput]] = None,
    ) -> tuple[str, str, str]:
        """
        以http回调的方式对话
        @return: (conversation_id, task_id, message_id)
        """
        url = f"{self.api_url}/chat-messages"
        data = self._complete_data(self._build_data(query, conversation_id, data, files), user, True)
        resp = requests.post(url, json=data, headers=self.headers, stream=True, timeout=REQUEST_TIME_OUT)
        self._handle_error_response(resp)
        _conversation_id = task_id = message_id = ""
        client = SSEClient(resp)  # type: ignore
        for item in client.events():
            event = json.loads(item.data)
            _conversation_id = event.get("conversation_id", "")
            task_id = event.get("task_id", "")
            message_id = event.get("message_id", "")
            break
        return _conversation_id, task_id, message_id

    def stop_chat(self, user: str, task_id: str) -> None:
        self.request(
            "chat-messages/run/:task_id/stop",
            user,
            path_params={"task_id": task_id},
            http_method=HttpMethod.POST,
        )

    def feedback_chat(
        self,
        user: str,
        message_id: str,
        rating: str = "",
        content: str = "",
    ) -> None:
        """消息反馈"""
        self.request(
            "chat-messages/run/:task_id/feedback",
            user,
            data={"rating": rating, "content": content},
            path_params={"message_id": message_id},
            http_method=HttpMethod.POST,
        )

    def get_suggested(self, user: str, message_id: str) -> ChatSuggestedResponse:
        """
        获取下一个问题建议
        @return: ChatSuggestedResponse
        """
        return self.request(
            "messages/:message_id/suggested",
            user,
            path_params={"message_id": message_id},
            model=ChatSuggestedResponse,
            http_method=HttpMethod.GET,
        )  # type: ignore

    def get_chat_history(
        self, user: str, conversation_id: str, first_id: Optional[str] = None, limit: int = 20
    ) -> ChatHistoryResponse:
        """
        获取聊天记录
        @return: ChatHistoryResponse
        """
        data: dict[str, Any] = {"conversation_id": conversation_id, "limit": limit}
        if first_id:
            data["first_id"] = first_id
        return self.request(
            "messages",
            user,
            data=data,
            model=ChatHistoryResponse,
            http_method=HttpMethod.GET,
        )  # type: ignore

    def get_conversations(
        self, user: str, last_id: Optional[str] = None, limit: int = 20, sort_by: Optional[str] = None
    ) -> ChatListResponse:
        """
        获取会话列表
        @return: ChatListResponse
        """
        data: dict[str, Any] = {"limit": limit}
        if last_id:
            data["last_id"] = last_id
        if sort_by:
            data["sort_by"] = sort_by
        return self.request(
            "conversations",
            user,
            data=data,
            model=ChatListResponse,
            http_method=HttpMethod.GET,
        )  # type: ignore

    def delete_conversation(self, user: str, conversation_id: str) -> None:
        """删除会话"""
        self.request(
            "conversations/:conversation_id",
            user,
            path_params={"conversation_id": conversation_id},
            http_method=HttpMethod.DELETE,
        )

    def delete_chat_history(self, user: str, conversation_id: str) -> None:
        """删除会话记录"""
        self.request(
            "messages/conversation/:conversation_id",
            user,
            path_params={"conversation_id": conversation_id},
            http_method=HttpMethod.DELETE,
        )

    def rename_conversation(self, user: str, conversation_id: str, name: Optional[str], auto: Optional[bool]) -> None:
        """重命名会话"""
        self.request(
            "conversations/:conversation_id/name",
            user,
            data={"name": name, "auto_generate": auto},
            path_params={"conversation_id": conversation_id},
            http_method=HttpMethod.POST,
        )

    def create_annotation(self, question: str, answer: str) -> dict:
        """创建标注"""
        return self.system_request(
            "apps/annotations",
            data={"question": question, "answer": answer},
            http_method=HttpMethod.POST,
        )

    def update_annotation(self, annotation_id: str, question: str, answer: str) -> dict:
        """更新标注"""
        return self.system_request(
            "apps/annotations/:annotation_id",
            data={"question": question, "answer": answer},
            path_params={"annotation_id": annotation_id},
            http_method=HttpMethod.PUT,
        )

    def delete_annotation(self, annotation_id: str) -> dict:
        """删除标注"""
        return self.system_request(
            "apps/annotations/:annotation_id",
            path_params={"annotation_id": annotation_id},
            http_method=HttpMethod.DELETE,
        )
