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
            'alphafold': [
                r'alphafold\s+(?:on\s+)?(.+)',  # alphafold on <sequence>
                r'运行\s*alphafold\s*(?:预测\s*)?(.+)',  # 运行alphafold预测<sequence>
                r'预测蛋白质结构\s+(.+)',  # 预测蛋白质结构<sequence>
                r'蛋白质结构预测\s+(.+)',  # 蛋白质结构预测<sequence>
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
            'alphafold': 'AlphaFold蛋白质结构预测 - 示例: "alphafold on MVSKG..." 或 "预测蛋白质结构 MVSKG..."',
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
                        'confidence': 1.0,
                        'note': f'匹配模式: {pattern}'
                    }
        
        # 尝试自然语言解析
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
            
        elif command_type == 'alphafold':
            # 提取序列 - 可能包含"protein sequence"等前缀
            sequence_text = match.group(1).strip()
            # 移除常见前缀
            sequence_text = re.sub(r'^(?:protein\s+sequence|seq|sequence)\s*[:=]?\s*', '', sequence_text, flags=re.IGNORECASE)
            # 清理序列
            sequence = re.sub(r'[^a-zA-Z]', '', sequence_text).upper()
            
            params = {
                'sequence': sequence,
                'job_name': f'protein_{sequence[:10]}_{hash(sequence) % 10000}',
                'model_type': 'alphafold2_ptm',
                'num_models': 1,
                'num_recycles': 3
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
            'alphafold': ['alphafold', '结构预测', '蛋白质结构', '三维结构', 'af2', 'af2预测'],
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
        help_text += "• pubmed搜索cancer immunotherapy\n"
        help_text += "• alphafold on MVSKGEEDNMASLPATHELHIFGSINGVDFDMVGQGTGNPNDGYEELNLK\n"
        help_text += "• pdb 1abc\n"
        help_text += "• 帮助\n"
        
        return help_text

if __name__ == "__main__":
    parser = CommandParser()
    
    # 测试
    test_commands = [
        "alphafold on MVSKGEEDNMASLPATHELHIFGSINGVDFDMVGQGTGNPNDGYEELNLK",
        "运行alphafold预测MVSKGEEDNMASLPATHELHIFGSINGVDFDMVGQGTGNPNDGYEELNLK",
        "预测蛋白质结构 MVSKGEEDNMASLPATHELHIFGSINGVDFDMVGQGTGNPNDGYEELNLK",
        "help",
    ]
    
    for cmd in test_commands:
        result = parser.parse(cmd)
        print(f"输入: {cmd}")
        print(f"结果: {result}")
        print()
