# ChatGLM-6B+Langchain

基于ChatGLM-6B+Langchain实现本地化知识库检索与搜索引擎接入

# Dify

## 搭建过程

1. 构建数据集：只支持单个文件上传，不能整个文件夹上传，单个文件大小小于15MB，支持文件类型`TXT, HTML, Markdown, PDF`

2. 文本分段与清洗：设置分段与预处理规则
   
3. 文档索引：

    a. 嵌入：调用 OpenAI embedding 接口，在用户查询时准确度更高(0.001$/1000 tokens)
   
    b. 其他索引方法：离线向量引擎索引，关键词索引，倒排索引，位图索引等(0 token)
    
    c. 文档索引结束后，数据集即可集成至应用内作为上下文

[官网](https://dify.ai) 

[Psychology Q&A](https://udify.app/chat/vXCCPTRUjWIBdang)

# Comparison
