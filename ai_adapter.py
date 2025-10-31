"""
AI 回复适配器 - 解耦 BiliGo 和具体 LLM 实现
职责：统一 AI 调用接口，支持多种 LLM 后端（RAG、直接 LLM 等）
"""

import requests
import json
from typing import Optional


class AIReplyAdapter:
    """AI 回复中转适配器"""

    def __init__(self, rag_service_url: str = "http://127.0.0.1:8000", timeout: int = 30):
        """
        初始化 AI 适配器

        Args:
            rag_service_url: RAG 服务地址（可从配置读取）
            timeout: 请求超时时间（秒）
        """
        self.rag_service_url = rag_service_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def reply(
        self,
        message: str,
        user_id: str,
        user_name: str,
        **kwargs
    ) -> Optional[str]:
        """
        获取 AI 回复（通用接口）

        Args:
            message: 用户消息内容
            user_id: 用户 ID（用于维护对话历史）
            user_name: 用户名称
            **kwargs: 其他参数（保留扩展性）

        Returns:
            AI 回复文本，失败返回 None
        """
        # 处理空消息
        if not message or not isinstance(message, str) or not message.strip():
            return None

        try:
            # 调用 RAG 服务
            request_data = {
                "platform": "bilibili",  # 标识来源平台
                "user_id": str(user_id),
                "user_name": user_name,
                "message": message.strip()
            }

            response = self.session.post(
                f"{self.rag_service_url}/chat",
                json=request_data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    reply = result.get("reply")
                    # 确保返回字符串，不返回 None 或空字符串
                    if reply and isinstance(reply, str):
                        return reply
                    return None
                else:
                    return None
            else:
                return None

        except requests.Timeout:
            return None
        except json.JSONDecodeError:
            return None
        except Exception as e:
            # 记录异常但不抛出
            return None

    def is_available(self) -> bool:
        """检查 AI 服务是否可用"""
        try:
            response = self.session.get(
                f"{self.rag_service_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# 全局实例
ai_adapter = None


def init_ai_adapter(rag_service_url: str = "http://127.0.0.1:8000") -> bool:
    """初始化 AI 适配器

    Args:
        rag_service_url: RAG 服务地址

    Returns:
        初始化成功返回 True，失败返回 False
    """
    global ai_adapter
    try:
        ai_adapter = AIReplyAdapter(rag_service_url=rag_service_url)
        if ai_adapter.is_available():
            return True
        else:
            return False
    except Exception as e:
        return False
