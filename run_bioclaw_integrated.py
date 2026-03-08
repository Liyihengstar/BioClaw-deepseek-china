#!/usr/bin/env python3
"""
运行BioClaw集成代理层 (AlphaFold + DeepSeek API)
"""

import os
import sys
import time
from pathlib import Path

# 设置DeepSeek API密钥
DEEPSEEK_API_KEY = "sk-0641e7a89a56429290a71bc429ae1fe7"
os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

print("🚀 启动BioClaw集成代理层 (AlphaFold + DeepSeek)")
print(f"📡 API密钥: {DEEPSEEK_API_KEY[:8]}...{DEEPSEEK_API_KEY[-8:]}")
print("🧬 集成功能: BLAST + PubMed + AlphaFold")
print("=" * 60)

# 检查Python依赖
try:
    import yaml
    import requests
    print("✅ Python依赖检查通过")
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("安装依赖: pip install pyyaml requests")
    sys.exit(1)

# 导入代理层
try:
    from agent_layer import AgentLayer
    print("✅ 代理层导入成功")
    
    # 初始化代理层
    agent = AgentLayer()
    print("✅ 代理层初始化完成")
    
    # 运行验证测试
    print("\n🧪 运行集成验证测试...")
    test_results = agent.run_verification_tests()
    
    print(f"\n验证测试结果:")
    print(f"  总测试数: {test_results['total_tests']}")
    print(f"  通过测试: {test_results['passed_tests']}")
    print(f"  失败测试: {test_results['failed_tests']}")
    
    # 显示AlphaFold测试详情
    print("\n🔍 AlphaFold测试详情:")
    for test in test_results["details"]:
        if test["command_type"] == "alphafold":
            print(f"  ✅ {test['name']}")
            print(f"     状态: {test['status']}")
            print(f"     结果: {test['result_summary']}")
    
    # 演示命令
    print("\n💡 演示命令:")
    demo_commands = [
        "blast搜索ATCGATCGATCG",
        "pubmed搜索cancer therapy",
        "alphafold on MVSKGEEDNMASLPATHELHIFGSINGVDFDMVGQGTGNPNDGYEELNLK",
        "帮助"
    ]
    
    for cmd in demo_commands:
        print(f"  • {cmd}")
    
    # 交互模式
    print("\n" + "=" * 60)
    print("💬 交互模式 (输入 'quit' 退出)")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 退出交互模式")
                break
                
            if not user_input:
                continue
                
            print("⏳ 处理中...")
            start_time = time.time()
            result = agent.process_message(user_input)
            elapsed = time.time() - start_time
            
            print(f"\n🤖 BioClaw (DeepSeek + AlphaFold):")
            print(f"⏱️  响应时间: {elapsed:.2f}秒")
            print(f"📊 命令类型: {result.get('command_type', '未知')}")
            print("-" * 40)
            print(result.get('formatted_message', '无响应'))
            print("-" * 40)
            
            # 显示验证说明
            print(f"\n💡 {result.get('verification_notes', '')}")
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保 agent_layer.py 存在")
except Exception as e:
    print(f"❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()