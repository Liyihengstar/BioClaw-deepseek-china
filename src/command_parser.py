#!/usr/bin/env python3
"""
BioQQ 命令解析器

将自然语言或结构化命令解析为可执行的操作
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple

class CommandParser:
    """命令解析器"""
    
    def __init__(self):
        # 预定义命令模式
        self.command_patterns = {
            'blast': [
                r'blast\s+(?:search\s+)?(.+)',  # blast search <sequence>
                r'运行\s*blast\s*(?:搜索\s*)?(.+)',  # 运行blast搜索<sequence>
                r'搜索序列\s+(.+)',  # 搜索序列<sequence>
            ],
            'pubmed': [
                r'pubmed\s+(?:search\s+)?(.+)',  # pubmed search <query>
                r'文献搜索\s+(.+)',  # 文献搜索<query>
                r'查找文献\s+(.+)',  # 查找文献<query>
            ],
            'pdb': [
                r'pdb\s+(\w+)',  # pdb <id>
                r'蛋白质结构\s+(\w+)',  # 蛋白质结构<id>
                r'查看pdb\s+(\w+)',  # 查看pdb<id>
            ],
            'help': [
                r'help',
                r'帮助',
                r'功能',
                r'支持的命令',
            ],
            'status': [
                r'status',
                r'状态',
                r'进展',
            ]
        }
        
        # 命令描述
        self.command_descriptions = {
            'blast': 'BLAST序列搜索 - 示例: "blast搜索ATCG..." 或 "运行BLAST ATGGCC..."',
            'pubmed': 'PubMed文献检索 - 示例: "pubmed搜索cancer therapy" 或 "文献搜索基因编辑"',
            'pdb': '蛋白质结构查看 - 示例: "pdb 1abc" 或 "蛋白质结构2hhb"',
            'help': '显示帮助信息',
            'status': '显示系统状态'
        }
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        解析文本命令
        
        Args:
            text: 输入的文本命令
            
        Returns:
            解析后的命令结构
        """
        text = text.strip().lower()
        
        # 检查是否为JSON格式的命令
        if text.startswith('{') and text.endswith('}'):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
        
        # 匹配预定义模式
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.match(pattern, text, re.IGNORECASE)
                if match:
                    params = self._extract_params(command_type, match, text)
                    return {
                        'type': command_type,
                        'original_text': text,
                        'params': params,
                        'confidence': 0.9
                    }
        
        # 没有匹配到预定义模式，可能是自然语言
        return self._parse_natural_language(text)
    
    def _extract_params(self, command_type: str, match: re.Match, text: str) -> Dict[str, Any]:
        """提取命令参数"""
        params = {}
        
        if command_type == 'blast':
            # 提取序列
            sequence = match.group(1).strip()
            # 清理序列中的非字母字符
            sequence = re.sub(r'[^a-zA-Z]', '', sequence).upper()
            
            # 判断序列类型
            if re.match(r'^[ATCGU]+$', sequence):
                params = {
                    'sequence': sequence,
                    'program': 'blastn' if 'U' not in sequence else 'blastn',  # RNA也使用blastn
                    'database': 'nr',
                    'mode': 'online'
                }
            elif re.match(r'^[ACDEFGHIKLMNPQRSTVWY]+$', sequence):
                params = {
                    'sequence': sequence,
                    'program': 'blastp',
                    'database': 'swissprot',
                    'mode': 'online'
                }
            else:
                params = {
                    'sequence': sequence,
                    'program': 'blastn',  # 默认
                    'database': 'nr',
                    'mode': 'online',
                    'note': '序列类型不确定'
                }
                
        elif command_type == 'pubmed':
            query = match.group(1).strip()
            params = {
                'query': query,
                'max_results': 10
            }
            
        elif command_type == 'pdb':
            pdb_id = match.group(1).strip().upper()
            params = {
                'pdb_id': pdb_id[:4],  # PDB ID通常是4字符
                'format': 'summary'  # 默认为摘要
            }
            
        return params
    
    def _parse_natural_language(self, text: str) -> Dict[str, Any]:
        """解析自然语言命令"""
        text_lower = text.lower()
        
        # 检测关键词
        keywords = {
            'blast': ['blast', '序列', '比对', '搜索序列', 'dna', 'rna', '蛋白质序列'],
            'pubmed': ['pubmed', '文献', '论文', '研究', '文章'],
            'pdb': ['pdb', '结构', '蛋白质结构', '三维结构', '分子结构']
        }
        
        # 计算每个命令类型的分数
        scores = {}
        for cmd_type, kw_list in keywords.items():
            score = 0
            for kw in kw_list:
                if kw in text_lower:
                    score += 1
            if score > 0:
                scores[cmd_type] = score
        
        if scores:
            # 选择分数最高的命令
            best_cmd = max(scores.items(), key=lambda x: x[1])
            return {
                'type': best_cmd[0],
                'original_text': text,
                'params': {'raw_text': text},
                'confidence': best_cmd[1] / 5.0,  # 归一化到0-1
                'note': '自然语言解析，可能需要更多信息'
            }
        
        # 无法识别
        return {
            'type': 'unknown',
            'original_text': text,
            'params': {},
            'confidence': 0.0,
            'note': '无法识别命令'
        }
    
    def get_help(self) -> str:
        """获取帮助信息"""
        help_text = "BioQQ 支持的命令:\n\n"
        
        for cmd_type, description in self.command_descriptions.items():
            help_text += f"• {cmd_type.upper()}: {description}\n"
        
        help_text += "\n示例:\n"
        help_text += "• blast搜索ATCGATCGATCG\n"
        help_text += "• 文献搜索cancer therapy\n"
        help_text += "• pdb 1abc\n"
        help_text += "• 帮助\n"
        
        return help_text
    
    def format_response(self, command_result: Dict[str, Any]) -> str:
        """格式化命令响应"""
        cmd_type = command_result.get('type', 'unknown')
        
        if cmd_type == 'help':
            return self.get_help()
        
        elif cmd_type == 'status':
            return "BioQQ 系统状态: 运行正常\n功能: BLAST搜索, 文献检索, 蛋白质结构查看\n模式: 开发中"
        
        elif cmd_type == 'unknown':
            return f"无法识别命令: {command_result.get('original_text', '')}\n\n{self.get_help()}"
        
        else:
            # 其他命令的确认响应
            params = command_result.get('params', {})
            confidence = command_result.get('confidence', 0.0)
            
            response = f"识别到 {cmd_type.upper()} 命令"
            
            if confidence < 0.5:
                response += f" (置信度: {confidence:.1%})"
            
            if params:
                response += "\n参数:"
                for key, value in params.items():
                    if key != 'raw_text':
                        response += f"\n• {key}: {value}"
            
            response += "\n\n正在处理..."
            return response


# 测试函数
def test_parser():
    """测试命令解析器"""
    parser = CommandParser()
    
    test_cases = [
        "blast搜索ATCGATCG",
        "运行BLAST ATGGCCATTGTA",
        "文献搜索cancer therapy",
        "pdb 1abc",
        "帮助",
        "这是什么工具？",
        "我想搜索一个DNA序列"
    ]
    
    print("测试命令解析器:\n")
    for test in test_cases:
        print(f"输入: {test}")
        result = parser.parse(test)
        print(f"解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        print(f"响应: {parser.format_response(result)}")
        print("-" * 50)


if __name__ == "__main__":
    test_parser()