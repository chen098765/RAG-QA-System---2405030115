#!/usr/bin/env python3
"""
RAG问答系统 - 命令行版本
"""

import os
import sys

# 添加项目三目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '项目三'))

from document_loader import load_documents_from_folder
from vector_db import VectorDatabase
from rag_chain import RAGQAChain

def main():
    print("=" * 60)
    print("RAG问答系统 - 命令行版本")
    print("=" * 60)
    
    # 加载文档
    print("\n正在加载文档...")
    docs = load_documents_from_folder('项目二')
    print(f"已加载 {len(docs)} 个文档")
    
    # 初始化向量数据库
    print("正在构建向量数据库...")
    db = VectorDatabase()
    db.add_documents(docs)
    
    # 获取统计信息
    stats = db.get_stats()
    print(f"向量数据库构建完成，共 {stats['total_chunks']} 个文本块")
    
    # 初始化问答链
    print("正在初始化问答链...")
    qa_chain = RAGQAChain(db)
    
    print("\n问答系统已就绪！输入问题开始提问（输入 'exit' 退出）")
    print("-" * 60)
    
    while True:
        question = input("\n请输入问题: ")
        
        if question.lower() == 'exit':
            print("感谢使用RAG问答系统，再见！")
            break
        
        if not question.strip():
            print("请输入有效的问题")
            continue
        
        print("正在思考...")
        answer = qa_chain.ask(question)
        print(f"\n答案: {answer}")

if __name__ == "__main__":
    main()