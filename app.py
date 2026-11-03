"""
Smart AI Agent - 精简版在线体验
作者：薛伟成
GitHub: https://github.com/X-xue-wc/smart-ai-agent
"""
import streamlit as st
from openai import OpenAI
import tempfile
import os

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
    
    # 密码校验，只有输对密码才能看到Key
    PASSWORD = "xwc2005"
    if "auth_ok" not in st.session_state:
        st.session_state.auth_ok = False
    
    if not st.session_state.auth_ok:
        pwd = st.text_input("输入管理密码查看API配置", type="password")
        if st.button("验证"):
            if pwd == PASSWORD:
                st.session_state.auth_ok = True
                st.rerun()
            else:
                st.error("密码错误")
    else:
        st.success("✅ 已解锁API配置")
        api_key = st.text_input("DeepSeek API Key", 
                               value="sk-9350e55d7bfa4fb69be2b217d7467dc1",
                               type="password")
        if st.button("锁定配置"):
            st.session_state.auth_ok = False
            st.rerun()
    
    # 默认Key，未解锁时用这个
    if "api_key" not in locals() or not st.session_state.auth_ok:
        api_key = "sk-9350e55d7bfa4fb69be2b217d7467dc1"
    
    st.divider()
    st.markdown("📁 [GitHub源码](https://github.com/X-xue-wc/smart-ai-agent)")
    st.markdown("👨‍💻 作者：薛伟成")

# 初始化OpenAI客户端（指向DeepSeek）
def get_client():
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
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
uploaded_text = ""
if model_mode == "📚 知识库问答":
    st.sidebar.divider()
    st.sidebar.subheader("📤 上传知识库文档")
    uploaded_file = st.sidebar.file_uploader("上传PDF文档", type="pdf")
    
    if uploaded_file:
        with st.spinner("正在处理文档..."):
            # 保存临时文件并读取PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            try:
                from pypdf import PdfReader
                reader = PdfReader(tmp_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                uploaded_text = text[:8000]  # 限制长度
                st.session_state['uploaded_text'] = uploaded_text
                st.sidebar.success(f"✅ 文档处理完成，共 {len(reader.pages)} 页")
            except Exception as e:
                st.sidebar.error(f"处理失败：{e}")

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
                client = get_client()
                
                # 构建消息
                messages = [{"role": "system", "content": "你是一个有用的AI助手，请用中文简洁回答问题。"}]
                
                if model_mode == "📚 知识库问答" and 'uploaded_text' in st.session_state:
                    messages.append({
                        "role": "system", 
                        "content": f"请基于以下文档内容回答问题。如果文档中没有相关信息，请说'抱歉，文档中没有找到相关信息'。\n\n文档内容：\n{st.session_state['uploaded_text']}"
                    })
                
                # 加入历史对话（最近10条）
                for msg in st.session_state.messages[-11:-1]:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                
                messages.append({"role": "user", "content": prompt})
                
                # 调用DeepSeek
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    temperature=0.7,
                    stream=False
                )
                
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                error_msg = f"出错了：{str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
