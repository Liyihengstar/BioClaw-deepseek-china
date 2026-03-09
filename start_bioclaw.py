#!/usr/bin/env python3
"""
BioClaw国内适配版 - 快速启动脚本
专为DeepSeek API优化的生物信息学助手
"""

import os
import sys
import argparse

def main():
    """主函数"""
    print("🚀 BioClaw国内适配版 (DeepSeek API)")
    print("=" * 60)
    
    # 检查API密钥
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 错误: 未设置DEEPSEEK_API_KEY环境变量")
        print("请先设置API密钥:")
        print("  export DEEPSEEK_API_KEY='你的DeepSeek API密钥'")
        print("或创建.env文件并设置DEEPSEEK_API_KEY")
        return 1
    
    print(f"✅ API密钥: {api_key[:8]}...{api_key[-8:]}")
    print("🧬 可用功能: BLAST + PubMed + AlphaFold")
    print("=" * 60)
    
    # 导入代理层
    try:
        sys.path.append('.')
        from src.agent_layer import AgentLayer
        
        print("🔧 初始化BioClaw代理层...")
        agent = AgentLayer()
        print("✅ 初始化完成")
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装依赖: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return 1
    
    # 交互模式
    print("\n💬 交互模式 (输入 'quit' 或 '退出' 结束)")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', '退出', '结束']:
                print("\n👋 感谢使用BioClaw!")
                break
                
            if not user_input:
                continue
            
            # 处理命令
            print("⏳ 处理中...")
            result = agent.process_message(user_input)
            
            # 显示结果
            print(f"\n🤖 BioClaw响应:")
            print("-" * 40)
            print(result.get('formatted_message', '无响应'))
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断")
            break
        except Exception as e:
            print(f"\n❌ 处理错误: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())