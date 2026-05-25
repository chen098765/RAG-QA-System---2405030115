from langchain.chains import ConversationalRetrievalChain
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory

class RAGQAChain:
    def __init__(self, vector_db, model_name="deepseek-r1:7b"):
        """初始化RAG问答链"""
        self.vector_db = vector_db
        
        # 创建Ollama语言模型
        self.llm = OllamaLLM(
            model=model_name,
            temperature=0.1
        )
        
        # 创建对话记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 系统提示词
        self.system_prompt = """
        你是一个基于知识库的问答助手。请根据提供的参考文档内容回答用户的问题。
        
        重要规则：
        1. 回答必须基于提供的参考文档
        2. 如果文档中没有相关信息，请明确说"文档中未找到相关答案"
        3. 不要编造答案
        4. 保持回答简洁明了
        
        参考文档：
        {context}
        
        问题：{question}
        """
    
    def ask(self, question):
        """回答用户问题"""
        try:
            # 先检索相关文档
            docs = self.vector_db.search(question, k=3)
            
            if not docs:
                return "文档中未找到相关答案"
            
            # 构建上下文
            context = "\n\n".join([doc['content'] for doc in docs])
            
            # 构建完整提示词
            prompt = self.system_prompt.format(context=context, question=question)
            
            # 调用语言模型
            answer = self.llm.invoke(prompt)
            
            # 检查是否是有效答案
            if not answer.strip() or "不知道" in answer or "无法回答" in answer:
                return "文档中未找到相关答案"
            
            return answer
        except Exception as e:
            print(f"问答过程中发生错误: {e}")
            return "文档中未找到相关答案"
    
    def clear_memory(self):
        """清空对话记忆"""
        self.memory.clear()

if __name__ == "__main__":
    from vector_db import VectorDatabase
    from document_loader import load_documents_from_folder
    
    # 加载文档
    docs = load_documents_from_folder('../docs')
    print(f"加载了 {len(docs)} 个文档")
    
    # 初始化向量数据库
    db = VectorDatabase()
    db.add_documents(docs)
    
    # 初始化问答链
    qa_chain = RAGQAChain(db)
    
    # 测试问答功能
    test_questions = [
        "什么是自然语言处理？",
        "Transformer架构的核心组件有哪些？",
        "BERT模型有什么特点？",
        "情感分析的主要类型有哪些？",
        "问答系统的实现方法有哪些？",
        "什么是人工智能？",  # 无关问题
        "今天天气怎么样？"   # 无关问题
    ]
    
    print("\n测试问答效果：")
    for question in test_questions:
        print(f"\n问题: {question}")
        answer = qa_chain.ask(question)
        print(f"答案: {answer}")