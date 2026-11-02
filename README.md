# Smart AI Agent - 智能AI助手服务

基于 LangGraph + FastAPI + Streamlit 构建的智能AI助手服务，支持RAG知识库问答、多工具调用和对话历史管理。

## 功能特性

- 🤖 **智能Agent**：基于 LangGraph 构建，支持多步推理和工具调用
- 📚 **RAG知识库**：上传PDF文档，构建向量知识库，实现精准问答
- 🌐 **Web界面**：Streamlit 构建的聊天界面，操作简单
- ⚡ **FastAPI服务**：后端API服务，支持流式响应
- 💾 **对话记忆**：支持SQLite存储对话历史
- 🔧 **多模型支持**：支持OpenAI、DeepSeek、Ollama等多种模型

## 技术栈

- **LangGraph** - Agent编排框架
- **FastAPI** - 后端API服务
- **Streamlit** - Web聊天界面
- **ChromaDB** - 向量数据库
- **Pydantic** - 数据模型
- **SQLite** - 对话历史存储

## 快速开始

### 1. 安装依赖

```bash
pip install -e .
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的API Key：

```env
OPENAI_API_KEY=your_api_key
```

### 3. 启动服务

```bash
# 启动后端API服务
python src/run_service.py

# 另开一个终端，启动Web界面
streamlit run src/streamlit_app.py
```

打开浏览器访问 http://localhost:8501 即可使用。

## 项目结构

```
├── src/
│   ├── agents/          # Agent定义
│   │   ├── rag_assistant.py    # RAG知识库问答
│   │   ├── research_assistant.py  # 研究助手
│   │   └── tools.py            # 工具定义
│   ├── core/           # 核心配置
│   ├── memory/         # 对话记忆
│   ├── schema/         # 数据模型
│   ├── service/        # FastAPI服务
│   └── streamlit_app.py  # Web界面
├── data/               # 知识库文档
└── pyproject.toml      # 依赖配置
```

## 作者

薛伟成 - GitHub: X-xue-wc

## License

MIT