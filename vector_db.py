import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

class VectorDatabase:
    def __init__(self, persist_dir='./chroma_db'):
        """初始化向量数据库"""
        self.persist_dir = persist_dir
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # 确保持久化目录存在
        os.makedirs(persist_dir, exist_ok=True)
        
        # 创建或加载Chroma数据库
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # 使用Ollama嵌入函数
        from chromadb.api.types import EmbeddingFunction
        class OllamaEmbeddingFunction(EmbeddingFunction):
            def __call__(self, texts):
                return self.embeddings.embed_documents(texts)
            
            @property
            def embedding_dimension(self):
                return 768  # nomic-embed-text的维度
        
        self.embedding_function = OllamaEmbeddingFunction()
        self.embedding_function.embeddings = self.embeddings
        
        self.collection = self.client.get_or_create_collection(
            "nlp_docs",
            embedding_function=self.embedding_function
        )
    
    def add_documents(self, documents):
        """向向量库添加文档"""
        if not documents:
            return
        
        # 使用RecursiveCharacterTextSplitter进行文本分块
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        all_texts = []
        all_metadatas = []
        all_ids = []
        doc_id = 0
        
        for doc in documents:
            texts = text_splitter.split_text(doc['content'])
            for i, text in enumerate(texts):
                all_texts.append(text)
                all_metadatas.append({
                    'filename': doc['filename'],
                    'chunk_index': i
                })
                all_ids.append(f"doc_{doc_id}_{i}")
            doc_id += 1
        
        # 添加到向量库
        if all_texts:
            # 先计算嵌入
            embeddings = self.embeddings.embed_documents(all_texts)
            
            self.collection.add(
                documents=all_texts,
                metadatas=all_metadatas,
                ids=all_ids,
                embeddings=embeddings
            )
            print(f"已添加 {len(all_texts)} 个文本块")
    
    def search(self, query, k=3):
        """检索与查询最相关的k个文本块"""
        # 先计算查询的嵌入
        query_embedding = self.embeddings.embed_query(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        if results and results['documents']:
            return [
                {
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else None,
                    'distance': results['distances'][0][i] if results['distances'] else None
                }
                for i in range(len(results['documents'][0]))
            ]
        return []
    
    def get_stats(self):
        """获取向量库统计信息"""
        count = self.collection.count()
        return {
            'total_chunks': count
        }
    
    def clear_database(self):
        """清空向量库"""
        self.client.delete_collection("nlp_docs")
        self.collection = self.client.create_collection(
            "nlp_docs",
            embedding_function=self.embedding_function
        )
        print("向量库已清空")

if __name__ == "__main__":
    from document_loader import load_documents_from_folder
    
    # 加载文档
    docs = load_documents_from_folder('../docs')
    print(f"加载了 {len(docs)} 个文档")
    
    # 初始化向量数据库
    db = VectorDatabase()
    
    # 添加文档到向量库
    db.add_documents(docs)
    
    # 测试检索功能
    results = db.search("Transformer架构是什么？", k=3)
    print(f"\n检索到 {len(results)} 个相关文本块")
    for i, result in enumerate(results):
        print(f"\n结果 {i+1}:")
        print(f"来源: {result['metadata']['filename']}")
        print(f"内容预览: {result['content'][:100]}...")