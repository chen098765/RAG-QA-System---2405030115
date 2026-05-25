# RAG问答系统

基于Ollama和LangChain构建的本地知识库问答系统，支持PDF/DOCX/TXT文档的上传、解析、向量化存储和智能问答。

## 功能特点

- 📄 支持PDF、DOCX、TXT文档的批量读取
- 🔍 使用Chroma向量数据库进行文档向量化存储
- 🤖 集成Ollama大模型进行问答
- 💬 支持多轮对话和上下文记忆
- 🌐 基于Streamlit的Web界面

## 环境要求

- Python 3.10+
- Ollama (用于运行大模型)

## 安装步骤

### 1. 安装Ollama

访问 [Ollama官网](https://ollama.com/) 下载并安装Ollama。

### 2. 下载模型

```bash
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用说明

### 运行Web应用

```bash
streamlit run app.py
```

### 使用步骤

1. 在左侧侧边栏上传PDF/DOCX/TXT文件
2. 点击"构建/更新知识库"按钮处理文档
3. 在问答交互区输入问题并点击"提问"
4. 查看回答结果，支持多轮对话

## 关键技术点

### RAG流程

1. **文档加载**: 使用PyPDF2和python-docx读取文档内容
2. **文本分块**: 使用RecursiveCharacterTextSplitter，chunk_size=1000，chunk_overlap=200
3. **向量化**: 使用Ollama的nomic-embed-text模型将文本块向量化
4. **存储**: 使用Chroma向量数据库存储向量
5. **检索**: 给定查询，检索最相关的3个文本块
6. **生成**: 将检索结果作为上下文输入到大模型生成答案

### 模型配置

- 问答模型: deepseek-r1:7b
- 嵌入模型: nomic-embed-text

### 系统提示词

```
你是一个基于知识库的问答助手。请根据提供的参考文档内容回答用户的问题。

重要规则：
1. 回答必须基于提供的参考文档
2. 如果文档中没有相关信息，请明确说"文档中未找到相关答案"
3. 不要编造答案
4. 保持回答简洁明了
```

## 项目结构

```
├── app.py              # Streamlit Web应用入口
├── rag_cli.py          # 命令行版本
├── requirements.txt    # 依赖列表
├── .gitignore          # Git忽略文件
├── docs/               # 示例文档目录
└── utils/
    ├── document_loader.py  # 文档加载模块
    ├── vector_db.py        # 向量数据库模块
    └── rag_chain.py        # RAG问答链模块
```

## 已知问题与改进方向

- 目前仅支持中文文档
- 大模型响应速度取决于本地硬件配置
- 可考虑添加文档预览和管理功能

## License

MIT License