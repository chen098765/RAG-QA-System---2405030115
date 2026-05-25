import sys
sys.path.insert(0, 'utils')

from document_loader import load_documents_from_folder
from vector_db import VectorDatabase

# 加载文档
docs = load_documents_from_folder('docs')
print(f"加载了 {len(docs)} 个文档")

# 初始化向量数据库
db = VectorDatabase()
db.add_documents(docs)

# 获取统计信息
stats = db.get_stats()
print(f"向量库已构建，共 {stats['total_chunks']} 个文本块")

# 测试检索功能
results = db.search("Transformer架构是什么？", k=3)
print(f"\n检索到 {len(results)} 个相关文本块")
for i, result in enumerate(results):
    print(f"\n结果 {i+1}:")
    print(f"来源: {result['metadata']['filename']}")
    print(f"内容预览: {result['content'][:150]}...")