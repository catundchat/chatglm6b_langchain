# ChatGLM-6B+Langchain 与 Dify 实现知识库检索

1. 基于 ChatGLM-6B+Langchain 实现本地化知识库检索与搜索引擎接入

2. 基于 Dify 构建知识库与聊天机器人

## ChatGLM-6B+Langchain

Milchstrasse

## Dify

### 搭建过程

1. 构建数据集：只支持单个文件上传，不能整个文件夹上传，单个文件大小小于15MB，支持文件类型`TXT, HTML, Markdown, PDF`

2. 文本分段与清洗：设置分段与预处理规则
   
3. 文档索引：

    a. 嵌入：调用 OpenAI embedding 接口，在用户查询时准确度更高(0.001$/1000 tokens)
   
    b. 其他索引方法：离线向量引擎索引，关键词索引，倒排索引，位图索引等(0 token)
    
    c. 文档索引结束后，数据集即可集成至应用内作为上下文
    
4. 提示词编排：设置prompt

5. 模型选择：支持 OpenAI, Azure OpenAI API KEY

| 模型 | 能否使用 |
|:---|:---:|
| gpt-3.5-turbo | ✔️ |
| gpt-4 | ✔️ |

### 使用

1. Web 端对话机器人：[Psychology Q&A](https://udify.app/chat/vXCCPTRUjWIBdang)

2. API : 支持对话型应用 API 调用

[官网](https://dify.ai) 

## Comparison

| 特性 | CHATGLM-6B+Langchain | Dify |
|:---|:---:|:---:|
| 可使用数据库 | ✔️ | ✔️ |
| 支持的数据类型 | ? |txt,html,markdown,pdf |
|数据上传|?|单个文件|
|   可使用 GPT-4  |  ❌  |  ✔️   |
|API调用|?|✔️|

