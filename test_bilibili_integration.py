"""
B站私信与RAG服务集成测试
验证BiliGo系统能否通过AI适配器接入RAG服务
"""

import json
import sys
from ai_adapter import AIReplyAdapter, init_ai_adapter


def test_ai_adapter_with_rag_service():
    """测试 AI 适配器与 RAG 服务的集成"""
    print("=" * 60)
    print("测试 1: AI 适配器初始化")
    print("=" * 60)

    rag_service_url = "http://127.0.0.1:8000"
    result = init_ai_adapter(rag_service_url=rag_service_url)

    if result:
        print(f"✅ AI 适配器初始化成功")
        print(f"   服务地址: {rag_service_url}")
    else:
        print(f"❌ AI 适配器初始化失败")
        return False

    print("\n" + "=" * 60)
    print("测试 2: RAG 服务健康检查")
    print("=" * 60)

    adapter = AIReplyAdapter(rag_service_url=rag_service_url)
    is_available = adapter.is_available()

    if is_available:
        print(f"✅ RAG 服务可用")
    else:
        print(f"❌ RAG 服务不可用")
        return False

    print("\n" + "=" * 60)
    print("测试 3: B站私信场景 - 用户咨询")
    print("=" * 60)

    # 模拟B站用户私信
    test_cases = [
        {
            "user_id": "123456",
            "user_name": "粉丝_001",
            "message": "你好，请问怎么使用这个功能？"
        },
        {
            "user_id": "789012",
            "user_name": "粉丝_002",
            "message": "我对你的产品很感兴趣，能否详细介绍一下"
        },
        {
            "user_id": "345678",
            "user_name": "粉丝_003",
            "message": "谢谢你的帮助！"
        }
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[用例 {i}] {test_case['user_name']} 的私信:")
        print(f"  消息: {test_case['message']}")

        reply = adapter.reply(
            message=test_case['message'],
            user_id=test_case['user_id'],
            user_name=test_case['user_name']
        )

        if reply:
            print(f"  ✅ AI 回复: {reply[:100]}...")
        else:
            print(f"  ❌ AI 无法生成回复")
            all_passed = False

    print("\n" + "=" * 60)
    print("测试 4: 适配器参数验证")
    print("=" * 60)

    # 测试空消息
    empty_reply = adapter.reply(
        message="",
        user_id="test",
        user_name="test"
    )

    if empty_reply is None:
        print("✅ 空消息正确处理")
    else:
        print("❌ 空消息处理异常")
        all_passed = False

    # 测试 None 消息
    none_reply = adapter.reply(
        message=None,
        user_id="test",
        user_name="test"
    )

    if none_reply is None:
        print("✅ None 消息正确处理")
    else:
        print("❌ None 消息处理异常")
        all_passed = False

    print("\n" + "=" * 60)
    print("集成测试总结")
    print("=" * 60)

    if all_passed:
        print("✅ 所有测试通过 - B站私信系统已成功接入RAG服务")
        return True
    else:
        print("⚠️ 部分测试失败 - 请检查RAG服务配置")
        return False


if __name__ == '__main__':
    print("\n🚀 BiliGo - AI 适配器集成测试启动\n")
    success = test_ai_adapter_with_rag_service()
    sys.exit(0 if success else 1)
