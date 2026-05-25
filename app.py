import streamlit as st
import os
import sys

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from document_loader import load_documents_from_folder, read_pdf, read_docx, read_txt
from vector_db import VectorDatabase
from rag_chain import RAGQAChain

def main():
    st.set_page_config(page_title="RAG问答系统", page_icon="📚", layout="wide")
    
    st.title("📚 RAG问答系统")
    st.markdown("基于Ollama和LangChain构建的本地知识库问答系统")
    
    # 初始化会话状态
    if 'vector_db' not in st.session_state:
        st.session_state.vector_db = VectorDatabase()
    
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    
    # 侧边栏
    with st.sidebar:
        st.header("📁 文档管理")
        
        # 文件上传
        uploaded_files = st.file_uploader(
            "上传PDF/DOCX/TXT文件",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.success(f"已选择 {len(uploaded_files)} 个文件")
        
        # 知识库构建按钮
        if st.button("🔄 构建/更新知识库", type="primary"):
            with st.spinner("正在处理文档..."):
                documents = []
                
                for uploaded_file in st.session_state.uploaded_files:
                    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                    
                    if file_ext == '.pdf':
                        content = read_pdf(uploaded_file)
                    elif file_ext == '.docx':
                        content = read_docx(uploaded_file)
                    elif file_ext == '.txt':
                        content = read_txt(uploaded_file)
                    else:
                        continue
                    
                    if content.strip():
                        documents.append({
                            'filename': uploaded_file.name,
                            'content': content
                        })
                
                if documents:
                    # 清空现有向量库并添加新文档
                    st.session_state.vector_db.clear_database()
                    st.session_state.vector_db.add_documents(documents)
                    
                    # 重新初始化问答链
                    st.session_state.qa_chain = RAGQAChain(st.session_state.vector_db)
                    st.success(f"知识库更新完成！已处理 {len(documents)} 个文档")
                else:
                    st.warning("没有有效的文档内容")
        
        # 从文件夹加载文档
        if st.button("📂 从docs文件夹加载文档"):
            with st.spinner("正在加载文档..."):
                docs = load_documents_from_folder('docs')
                
                if docs:
                    st.session_state.vector_db.clear_database()
                    st.session_state.vector_db.add_documents(docs)
                    st.session_state.qa_chain = RAGQAChain(st.session_state.vector_db)
                    st.success(f"成功加载 {len(docs)} 个文档")
                else:
                    st.warning("docs文件夹中没有找到有效文档")
        
        # 知识库状态
        st.header("📊 知识库状态")
        stats = st.session_state.vector_db.get_stats()
        st.info(f"当前文本块数量: **{stats['total_chunks']}**")
        
        # 清空对话历史
        if st.button("🗑️ 清空对话历史"):
            st.session_state.chat_history = []
            if st.session_state.qa_chain:
                st.session_state.qa_chain.clear_memory()
            st.success("对话历史已清空")
    
    # 主内容区 - 问答交互
    st.header("💬 问答交互")
    
    # 显示对话历史
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.markdown(f"**问题:** {question}")
        
        with st.chat_message("assistant"):
            st.markdown(f"**答案:** {answer}")
    
    # 输入问题
    question = st.text_input("请输入您的问题:", key="question_input")
    
    if st.button("🚀 提问"):
        if not question.strip():
            st.warning("请输入问题")
        else:
            if not st.session_state.qa_chain:
                st.warning("请先构建知识库")
            else:
                with st.spinner("正在思考..."):
                    answer = st.session_state.qa_chain.ask(question)
                    
                    # 添加到对话历史
                    st.session_state.chat_history.append((question, answer))
                    
                    # 刷新页面显示新对话
                    st.rerun()

if __name__ == "__main__":
    main()