# BioClaw DeepSeek-China Branch

**分支名称**: `deepseek-china`  
**目的**: 验证BioClaw项目在DeepSeek API下的可用性和性能  
**状态**: 开发中  

## 📋 概述

本分支旨在验证[BioClaw](https://github.com/Runchuan-BU/BioClaw)项目（生物信息学Claude技能）在使用DeepSeek API替代Claude API时的可用性和性能。通过**代理层架构**，在不修改原始BioClaw代码的前提下，验证核心功能。

## 🎯 验证目标

### 1. 可用性验证
- ✅ BLAST序列搜索功能
- ✅ PubMed文献检索功能  
- ⏳ 其他生物信息学工具

### 2. 性能评估
- 响应时间分析
- 准确率评估
- 资源消耗测量

### 3. 架构评估
- API兼容性分析
- 可扩展性评估
- 改进建议

## 🏗️ 系统架构

### 代理层设计
```
用户输入 → DeepSeek API → 代理转换层 → BioClaw技能模拟 → 生物信息学工具 → 结果返回
```

### 关键组件
1. **命令解析器** - 支持中英文自然语言命令
2. **DeepSeek集成** - 使用DeepSeek API处理自然语言
3. **Claude格式转换** - 适配BioClaw技能接口
4. **技能模拟器** - 执行BioClaw技能逻辑
5. **工具执行器** - 调用实际生物信息学工具
6. **结果格式化器** - 生成用户友好输出

## 📁 项目结构

```
bioqq/
├── src/                    # 源代码
│   ├── agent_layer.py     # 代理层主逻辑
│   ├── command_parser.py  # 命令解析器
│   └── __init__.py
├── bioclaw-skills/        # BioClaw技能文件
│   ├── blast-skill.md    # BLAST搜索技能
│   └── pubmed-skill.md   # PubMed检索技能
├── reporting/             # 状态汇报
│   └── status_report.py  # 自动汇报脚本
├── tests/                 # 测试文件
│   ├── test_agent_layer.py
│   └── test_blast.py
├── config/               # 配置文件
│   └── agent_config.yaml
├── docs/                 # 文档
│   ├── AGENT_LAYER_DESIGN.md
│   └── ARCHITECTURE.md
├── scripts/              # 实用脚本
├── requirements.txt      # Python依赖
├── .gitignore           # Git忽略文件
└── README.md            # 本文档
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- DeepSeek API密钥
- BioPython库

### 安装步骤
```bash
# 1. 克隆仓库
git clone https://github.com/Runchuan-BU/BioClaw.git
cd BioClaw
git checkout deepseek-china

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置API密钥
export DEEPSEEK_API_KEY="your-api-key-here"

# 5. 运行测试
python tests/test_agent_layer.py
```

### 基本用法
```python
from src.agent_layer import AgentLayer

# 初始化代理层
agent = AgentLayer()

# 处理BLAST搜索
result = agent.process_message("blast搜索ATGCGATCGATCG")
print(result["formatted_message"])

# 处理PubMed检索
result = agent.process_message("文献搜索cancer therapy")
print(result["formatted_message"])
```

## 🔬 验证方法

### 测试用例
1. **BLAST序列搜索**
   - DNA序列搜索
   - 蛋白质序列搜索
   - 复杂序列分析

2. **PubMed文献检索**
   - 简单关键词搜索
   - 复杂查询构建
   - 多条件筛选

### 性能指标
- **响应时间**: 从接收到结果的时间
- **准确性**: 结果与期望的匹配度
- **稳定性**: 连续运行的可靠性
- **资源使用**: CPU/内存消耗

## 📊 验证结果

### 当前状态
| 功能 | 状态 | 备注 |
|------|------|------|
| BLAST搜索 | ✅ 模拟通过 | 需要真实API集成 |
| PubMed检索 | ✅ 模拟通过 | 需要真实API集成 |
| 命令解析 | ✅ 完成 | 支持中英文 |
| 代理层架构 | ✅ 完成 | 可扩展设计 |

### 发现的问题
1. **API依赖**: BioClaw硬编码Claude Agent SDK，不支持直接替换
2. **架构限制**: 技能与工具紧耦合，扩展性有限
3. **配置缺失**: 缺少模型无关的API抽象层

## 💡 改进建议

### 短期改进
1. **增加API抽象层** - 支持多模型API
2. **配置化技能加载** - 动态技能管理
3. **性能监控** - 实时性能指标收集

### 长期优化
1. **模块化重构** - 清晰的责任分离
2. **缓存机制** - 减少重复API调用
3. **异步处理** - 提高并发性能

## 📈 路线图

### 阶段1: 基础验证 (当前)
- [x] 代理层架构设计
- [x] 命令解析器实现
- [x] 技能分析
- [ ] GitHub分支创建
- [ ] 真实API集成

### 阶段2: 功能验证
- [ ] BLAST真实功能测试
- [ ] PubMed真实功能测试
- [ ] 性能基准测试
- [ ] 可用性评估

### 阶段3: 优化发布
- [ ] 性能优化
- [ ] 文档完善
- [ ] 发布验证报告
- [ ] 提供改进建议

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进本项目。

### 开发流程
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -am '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建Pull Request

### 代码规范
- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档
- 编写单元测试

## 📄 许可证

本项目基于MIT许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [BioClaw项目](https://github.com/Runchuan-BU/BioClaw) - 原始生物信息学技能
- [DeepSeek](https://www.deepseek.com/) - AI模型API提供
- [NCBI](https://www.ncbi.nlm.nih.gov/) - 生物信息学工具和数据

## 📞 联系方式

如有问题或建议，请通过GitHub Issues提交。

---
*最后更新: 2026-03-08*  
*分支版本: 0.1.0*