#!/usr/bin/env python3
"""
使用 AI 生成智能回复并发送给指定用户
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import BilibiliAPI, config, load_config
from ai_adapter import AIReplyAdapter


def send_ai_reply_to_user(user_id: int, user_message: str):
    """
    给用户发送 AI 生成的智能回复

    Args:
        user_id: B 站用户 ID
        user_message: 用户的问题/消息（用于生成回复）
    """
    print(f"准备为用户 {user_id} 生成 AI 回复")
    print(f"用户消息: {user_message}")
    print("-" * 60)

    # 加载配置
    load_config()

    # 检查登录信息
    if not config.get('sessdata') or not config.get('bili_jct'):
        print("❌ 错误：请先配置登录信息")
        return False

    try:
        # 1. 使用 AI 适配器生成回复
        print("⏳ 正在使用 RAG 服务生成智能回复...")
        rag_service_url = config.get('rag_service_url', 'http://127.0.0.1:8000')
        adapter = AIReplyAdapter(rag_service_url=rag_service_url)

        # 检查 RAG 服务是否可用
        if not adapter.is_available():
            print(f"❌ RAG 服务不可用: {rag_service_url}")
            return False

        # 生成回复
        ai_reply = adapter.reply(
            message=user_message,
            user_id=str(user_id),
            user_name=f"用户_{user_id}"
        )

        if not ai_reply:
            print("❌ AI 无法生成回复")
            return False

        print(f"✅ AI 生成回复成功")
        print(f"\n📝 AI 回复内容:")
        print("-" * 60)
        print(ai_reply)
        print("-" * 60)

        # 2. 发送回复给用户
        print(f"\n⏳ 正在发送消息到 B 站...")

        api = BilibiliAPI(config['sessdata'], config['bili_jct'])

        # 验证登录状态
        my_uid = api.get_my_uid()
        if not my_uid:
            print("❌ 登录状态失效")
            return False

        print(f"✅ 登录状态有效 (UID: {my_uid})")

        # 发送 AI 生成的回复
        result = api.send_msg(user_id, msg_type=1, content=ai_reply)

        if result is None:
            print("❌ 发送失败：网络错误")
            return False

        code = result.get('code')

        if code == 0:
            print(f"✅ 智能回复发送成功！")
            print(f"\n📊 发送总结:")
            print(f"  收件人: {user_id}")
            print(f"  用户问题: {user_message}")
            print(f"  AI 回复: {ai_reply[:100]}...")
            return True

        elif code == -412:
            print(f"⚠️ 触发频率限制，请稍候")
            return False

        elif code == -101:
            print(f"❌ 登录已失效，请重新配置")
            return False

        else:
            error_msg = result.get('message', '未知错误')
            print(f"❌ 发送失败 [错误码: {code}]: {error_msg}")
            return False

    except Exception as e:
        print(f"❌ 异常错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("\n🤖 BiliGo - AI 智能回复工具\n")

    if len(sys.argv) < 2:
        # 默认示例：询问关于某个主题
        user_id = 1207958559
        user_question = "请问如何学习计算机科学？有什么推荐的资源吗？"
    else:
        user_id = int(sys.argv[1])
        user_question = sys.argv[2] if len(sys.argv) > 2 else "你好，请问有什么帮助吗？"

    success = send_ai_reply_to_user(user_id, user_question)
    print()
    sys.exit(0 if success else 1)
