# LangChain AutoPlanner Generator - 完整AI工作流生成系统

## 🎯 什么是这个系统？

LangChain AutoPlanner Generator是一个**智能AI工作流自动生成器**，它能将您的简单需求描述自动转换为完整的、可运行的AI应用程序。您只需要告诉它您想要什么，它就能自动生成所有必要的代码、测试和文档。

**简单来说：您说需求，它生成完整的AI应用！**

## 🚀 核心功能

### 1. **智能需求理解**
- 自动分析您的需求描述
- 识别核心功能意图
- 智能规划技术实现方案

### 2. **模块化工作流生成**
- 将复杂任务分解为多个独立模块
- 每个模块负责特定功能
- 模块间自动协调工作

### 3. **并行处理支持**
- 自动识别可以并行执行的任务
- 提高程序运行效率
- 智能管理任务依赖关系

### 4. **自我规划能力**
- 生成的程序可以自己生成新功能模块
- 支持运行时动态添加新功能
- 具备自我进化能力

### 5. **配置驱动**
- 通过配置文件控制AI模型参数
- 支持多种AI模型切换
- 无需修改代码即可调整行为

## 📁 文件结构说明

```
output/
├── ai_models.yml           # AI模型配置文件（重要！）
├── main_langchain_flow.py  # 主程序文件
├── modules/               # 功能模块文件夹
│   ├── intent_recognition_module.py    # 意图识别模块
│   ├── data_processing_module.py       # 数据处理模块
│   ├── analysis_module.py             # 分析模块
│   └── validation_module.py           # 验证模块
├── tests/               # 测试文件
├── docs/               # 文档文件
└── README.md           # 说明文档
```

## 🔧 配置文件详解 (ai_models.yml)

这是最重要的配置文件，控制AI模型的行为：

```yaml
# AI模型配置
api_config:
  base_url: "https://api.openai.com/v1"  # AI API地址
  primary_model: "gpt-4"                 # 主要使用的AI模型
  temperature: 0.7                       # 创造性程度 (0-1, 越高越有创意)
  max_tokens: 2000                       # 最大响应长度

# 模型路由 - 不同任务使用不同模型
model_routing:
  intent_recognition: "primary_model"    # 意图识别用主模型
  code_generation: "primary_model"       # 代码生成用主模型
  validation: "primary_model"            # 验证用主模型

# 高级功能配置
advanced:
  # 自定义请求参数
  custom_body:
    user_id: "test_user_123"
    custom_header: "my_custom_value"
    request_source: "langchain_autoplanner"
  
  # 多模型支持
  multi_models:
    - name: "gpt4"
      model: "gpt-4"
      base_url: "https://api.openai.com/v1"
      temperature: 0.7
    - name: "gpt35"
      model: "gpt-3.5-turbo"
      base_url: "https://api.openai.com/v1"
      temperature: 0.8
    - name: "claude"
      model: "claude-3-opus"
      base_url: "https://api.anthropic.com/v1"
      temperature: 0.6

# 自我规划配置
self_planning:
  enabled: true              # 是否启用自我规划
  max_depth: 3              # 最大递归深度
  version_timestamps: true  # 是否使用时间戳版本
```

**重要提示：** 您需要在使用前修改`ai_models.yml`中的API密钥和模型设置！

## 🛠️ 安装和使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置API密钥
在使用前，您需要：
- 设置环境变量 `OPENAI_API_KEY` 为您的OpenAI API密钥
- 或在`ai_models.yml`中配置正确的API端点

### 3. 运行主程序
```bash
python main_langchain_flow.py
```

### 4. 运行测试
```bash
python -m pytest tests/
```

## 💡 使用示例

### 示例1：数据分析应用
需求：`"创建一个分析用户评论情感的应用"`

系统会自动生成：
- 评论文本解析模块
- 情感分析处理模块
- 结果验证模块
- 完整的测试用例

### 示例2：数据处理管道
需求：`"创建一个处理CSV数据并生成报告的系统"`

系统会自动生成：
- CSV文件读取模块
- 数据清洗模块
- 报告生成模块
- 错误处理模块

## 🔍 技术特性

### 自我规划功能
生成的系统具备自我扩展能力：
- 可以在运行时分析新需求
- 自动生成新的功能模块
- 自动集成新模块到现有系统
- 支持递归深度控制，防止无限循环

### 配置驱动架构
- 所有AI模型参数可通过配置文件调整
- 支持多模型切换和路由
- 自定义请求参数注入
- 环境隔离，便于部署

### 模块化设计
- 每个功能模块职责单一
- 模块间松耦合
- 易于维护和扩展
- 支持并行执行

## 📊 输出内容

系统会生成完整的项目结构：

1. **代码文件** - 完整的Python源代码
2. **测试文件** - 单元测试和集成测试
3. **文档文件** - 架构说明和使用指南
4. **配置文件** - 可调整的AI模型配置
5. **依赖文件** - 项目依赖清单

## ⚡ 性能优化

- **并行执行** - 自动识别可并行的任务
- **智能缓存** - 避免重复计算
- **资源管理** - 优化内存和API调用
- **错误恢复** - 具备自愈能力

## 🔐 安全特性

- **API密钥安全** - 支持环境变量配置
- **输入验证** - 防止恶意输入
- **访问控制** - 配置驱动的权限管理
- **审计日志** - 完整的操作记录

## 🆘 故障排除

### 常见问题：
1. **API错误** - 检查API密钥配置
2. **依赖错误** - 确保所有依赖包已安装
3. **配置错误** - 验证YAML文件格式正确

### 调试步骤：
1. 检查`ai_models.yml`配置
2. 验证API密钥设置
3. 运行测试文件验证功能
4. 查看日志输出定位问题

## 🎯 适用场景

- **快速原型开发** - 几分钟内生成完整应用
- **AI应用构建** - 自动集成各种AI模型
- **数据处理管道** - 自动化数据处理流程
- **企业应用** - 可扩展的企业级解决方案
- **学习研究** - AI和LangChain学习工具

## 📞 支持和反馈

这个系统是为非技术用户和开发者设计的，旨在让AI应用开发变得简单高效。如果您有任何问题或建议，欢迎随时改进配置和代码！

**开始使用吧！** 只需要修改配置文件，运行主程序，您就能拥有一个完整的AI工作流应用！
