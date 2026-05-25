import ollama

def test_ollama_connection():
    """测试Ollama API连接"""
    try:
        # 测试列出已安装的模型
        models = ollama.list()
        print("已安装的模型:")
        for model in models.get('models', []):
            print(f"  - {model['name']}")
        
        # 测试生成响应
        response = ollama.generate(
            model='deepseek-r1:7b',
            prompt='Hello, how are you?'
        )
        print("\n模型响应:")
        print(response.get('response', ''))
        
        return True
    except Exception as e:
        print(f"连接失败: {e}")
        return False

if __name__ == "__main__":
    print("测试Ollama API连接...")
    success = test_ollama_connection()
    if success:
        print("\nOllama API测试成功!")
    else:
        print("\nOllama API测试失败，请检查Ollama服务是否已启动")