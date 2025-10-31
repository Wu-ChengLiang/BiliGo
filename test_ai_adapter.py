"""
AI 适配器的 TDD 测试用例
测试 AIReplyAdapter 与 RAG 服务的集成
"""

import pytest
import json
import requests
from unittest.mock import Mock, patch, MagicMock


class TestAIReplyAdapter:
    """AIReplyAdapter 测试套件"""

    @pytest.fixture
    def adapter(self):
        """创建 AIReplyAdapter 实例"""
        # 这个 import 会失败，因为 ai_adapter.py 还不存在
        from ai_adapter import AIReplyAdapter
        return AIReplyAdapter(rag_service_url="http://127.0.0.1:8000")

    def test_adapter_initialization(self, adapter):
        """测试适配器初始化"""
        assert adapter is not None
        assert adapter.rag_service_url == "http://127.0.0.1:8000"
        assert adapter.timeout == 30

    def test_adapter_with_custom_timeout(self):
        """测试自定义超时时间"""
        from ai_adapter import AIReplyAdapter
        adapter = AIReplyAdapter(rag_service_url="http://127.0.0.1:8000", timeout=60)
        assert adapter.timeout == 60

    def test_reply_with_valid_message(self, adapter):
        """测试获取有效回复"""
        reply = adapter.reply(
            message="什么是向量数据库？",
            user_id="123",
            user_name="test_user"
        )
        assert reply is not None
        assert isinstance(reply, str)
        assert len(reply) > 0

    def test_reply_returns_string(self, adapter):
        """测试回复返回字符串类型"""
        reply = adapter.reply(
            message="你好",
            user_id="456",
            user_name="another_user"
        )
        assert isinstance(reply, str)

    def test_reply_with_empty_message(self, adapter):
        """测试空消息处理"""
        reply = adapter.reply(
            message="",
            user_id="789",
            user_name="user"
        )
        # 应该返回 None 或空字符串
        assert reply is None or reply == ""

    def test_reply_with_none_message(self, adapter):
        """测试 None 消息处理"""
        reply = adapter.reply(
            message=None,
            user_id="999",
            user_name="user"
        )
        assert reply is None or reply == ""

    def test_reply_preserves_user_context(self, adapter):
        """测试用户上下文保持"""
        # 同一用户的多次回复应该保持一致
        reply1 = adapter.reply(
            message="第一个问题",
            user_id="123",
            user_name="user1"
        )
        reply2 = adapter.reply(
            message="第二个问题",
            user_id="123",
            user_name="user1"
        )
        # 验证都返回有效回复
        assert reply1 is not None
        assert reply2 is not None

    def test_health_check_success(self, adapter):
        """测试服务健康检查 - 成功情况"""
        is_available = adapter.is_available()
        assert is_available is True

    def test_health_check_failure(self):
        """测试服务不可用的情况"""
        from ai_adapter import AIReplyAdapter
        # 指向不存在的服务
        adapter = AIReplyAdapter(rag_service_url="http://127.0.0.1:9999")
        is_available = adapter.is_available()
        assert is_available is False

    def test_adapter_handles_network_timeout(self):
        """测试网络超时处理"""
        from ai_adapter import AIReplyAdapter
        adapter = AIReplyAdapter(
            rag_service_url="http://127.0.0.1:8000",
            timeout=0.001  # 设置极短超时
        )
        # 应该返回 None 而不是抛异常
        reply = adapter.reply(
            message="test",
            user_id="123",
            user_name="user"
        )
        assert reply is None

    def test_adapter_handles_invalid_json_response(self, adapter):
        """测试处理无效的 JSON 响应"""
        with patch.object(adapter.session, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_post.return_value = mock_response

            reply = adapter.reply(
                message="test",
                user_id="123",
                user_name="user"
            )
            assert reply is None

    def test_adapter_handles_unsuccessful_response(self, adapter):
        """测试处理失败的响应"""
        with patch.object(adapter.session, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": False,
                "reply": None,
                "error": "Service error"
            }
            mock_post.return_value = mock_response

            reply = adapter.reply(
                message="test",
                user_id="123",
                user_name="user"
            )
            assert reply is None

    def test_adapter_handles_http_error(self, adapter):
        """测试处理 HTTP 错误"""
        with patch.object(adapter.session, 'post') as mock_post:
            mock_post.return_value.status_code = 500

            reply = adapter.reply(
                message="test",
                user_id="123",
                user_name="user"
            )
            assert reply is None

    def test_global_init_function_failure(self):
        """测试全局初始化函数 - 失败情况"""
        from ai_adapter import init_ai_adapter
        result = init_ai_adapter(rag_service_url="http://127.0.0.1:9999")
        assert result is False

    def test_global_adapter_instance_after_init(self):
        """测试全局适配器实例创建"""
        from ai_adapter import init_ai_adapter, ai_adapter
        # 执行初始化
        init_ai_adapter(rag_service_url="http://127.0.0.1:9999")
        # 即使失败，adapter 也应该被创建
        assert ai_adapter is not None

    def test_request_includes_platform_identifier(self, adapter):
        """测试请求包含平台标识"""
        with patch.object(adapter.session, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "reply": "test reply"
            }
            mock_post.return_value = mock_response

            adapter.reply(
                message="test",
                user_id="123",
                user_name="user"
            )

            # 验证请求包含正确的数据
            call_args = mock_post.call_args
            json_data = call_args[1]['json']
            assert json_data['platform'] == 'bilibili'

    def test_reply_with_special_characters(self, adapter):
        """测试包含特殊字符的消息"""
        reply = adapter.reply(
            message="你好🎉世界@#$%",
            user_id="123",
            user_name="user"
        )
        # 应该能处理特殊字符
        assert reply is None or isinstance(reply, str)

    def test_reply_with_long_message(self, adapter):
        """测试长消息处理"""
        long_message = "这是一条很长的消息。" * 100
        reply = adapter.reply(
            message=long_message,
            user_id="123",
            user_name="user"
        )
        assert reply is None or isinstance(reply, str)

    def test_concurrent_requests(self, adapter):
        """测试并发请求处理"""
        import concurrent.futures

        def make_request(user_id):
            return adapter.reply(
                message=f"user {user_id} message",
                user_id=str(user_id),
                user_name=f"user_{user_id}"
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, i) for i in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # 所有请求都应该完成而不会出现错误
        assert len(results) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
