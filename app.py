"""
Smart AI Agent - 精简版在线体验
作者：薛伟成
GitHub: https://github.com/X-xue-wc/smart-ai-agent
"""
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
import os
import tempfile

# 页面配置
st.set_page_config(
    page_title="Smart AI Agent",
    page_icon="🤖",
    layout="wide"
)

# 标题
st.title("🤖 Smart AI Agent")
st.caption("基于LangChain + DeepSeek构建的智能AI助手 | 作者：薛伟成")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 模型选择
    model_mode = st.radio("选择模式", ["💬 普通对话", "📚 知识库问答"])
    
    st.divider()
    
    # API Key设置
    api_key = st.text_input("DeepSeek API Key", 
                           value="sk-9350e55d7bfa4fb69be2b217d7467dc1",
                           type="password")
    
    st.divider()
    st.markdown("📁 [GitHub源码](https://github.com/X-xue-wc/smart-ai-agent)")
    st.markdown("👨‍💻 作者：薛伟成")

# 初始化LLM
def get_llm():
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
        temperature=0.7
    )

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是Smart AI Agent，你可以问我任何问题。如果需要基于文档回答，请在侧边栏切换到知识库模式并上传PDF。"}
    ]

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 知识库模式
if model_mode == "📚 知识库问答":
    st.sidebar.divider()
    st.sidebar.subheader("📤 上传知识库文档")
    uploaded_file = st.sidebar.file_uploader("上传PDF文档", type="pdf")
    
    if uploaded_file:
        with st.spinner("正在处理文档..."):
            # 保存临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            # 加载并切分文档
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)
            
            # 构建向量库
            embeddings = OpenAIEmbeddings(
                model="BAAI/bge-small-zh-v1.5",
                api_key=api_key,
                base_url="https://api.deepseek.com/v1"
            )
            # 注意：DeepSeek不提供embedding，这里用简化方式
            st.session_state['documents'] = chunks
            st.sidebar.success(f"✅ 文档处理完成，共 {len(chunks)} 个片段")

# 聊天输入
if prompt := st.chat_input("输入你的问题..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 生成回答
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                llm = get_llm()
                
                if model_mode == "💬 普通对话":
                    # 普通对话
                    prompt_template = ChatPromptTemplate.from_messages([
                        ("system", "你是一个有用的AI助手，请用中文简洁回答问题。"),
                        ("human", "{question}")
                    ])
                    chain = prompt_template | llm | StrOutputParser()
                    response = chain.invoke({"question": prompt})
                else:
                    # 知识库模式
                    if 'documents' in st.session_state:
                        # 简单的上下文拼接方式
                        context = "\n\n".join([doc.page_content for doc in st.session_state['documents'][:3]])
                        prompt_text = f"""基于以下文档内容回答问题：

文档内容：
{context}

问题：{prompt}

如果文档中没有相关信息，请说"抱歉，文档中没有找到相关信息"。"""
                        response = llm.invoke(prompt_text).content
                    else:
                        response = "请先在左侧上传PDF文档，我才能基于文档回答问题。"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"出错了：{str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
