# ChatGLM-6B+Langchain 与 Dify 实现知识库检索

1. 基于 ChatGLM-6B+Langchain 实现本地化知识库检索与搜索引擎接入

2. 基于 Dify 构建知识库与聊天机器人

## ChatGLM-6B+Langchain

### 知识库向量索引

- 中文维基百科截止4月份数据，45万
- 截止去年九月的130w条中文维基百科处理结果和对应faiss向量文件
- 金融研报知识图谱
- 以上共 23GB 资料
- [下载链接](https://pan.baidu.com/s/1lcI1JHArTWlOpcSiDH1O3A) 提取码: u6ep

### 运行配置

- 显存 ≥ 12GB ， 运行内存 ≥ 32GB
- 深度学习工作站：GPU: RTX 4090, CPU: Intel(R) Xeon(R) CPU E5-2660 v2

### 搭建流程

1. 创建并激活虚拟环境 `python3 -m venv env`

2. 克隆GitHub repository `git clone https://github.com/catundchat/Chinese-LangChain.git`

3. 安装所需库 `pip install -r requirements.txt`

4. 按需修改 `main.py` 文件中的文件路径，代码块，应用选择后运行即可。 

### 使用

接入搜索引擎，知识库添加文件

## Dify

### 搭建过程

1. 构建数据集：只支持单个文件上传，不能整个文件夹上传，单个文件大小小于15MB，支持文件类型`TXT, HTML, Markdown, PDF`

2. 文本分段与清洗：设置分段与预处理规则
   
3. 文档索引：

    a. 嵌入：调用 OpenAI embedding 接口，在用户查询时准确度更高(0.002$/1000 tokens)
   
    b. 其他索引方法：离线向量引擎索引，关键词索引，倒排索引，位图索引等(0 token)
    
    c. 文档索引结束后，数据集即可集成至应用内作为上下文
    
4. 提示词编排：设置prompt

5. 模型选择：支持 OpenAI, Azure OpenAI API KEY

| 模型 | 能否使用 |
|:---|:---:|
| gpt-3.5-turbo | ✔️ |
| gpt-4 | ✔️ |

注：GPT-4 API 正在申请中无法测试

### 使用

1. Web 端对话机器人：[Psychology Q&A](https://udify.app/chat/vXCCPTRUjWIBdang)

2. API : 支持调用对话型应用 API  [官网](https://dify.ai) 

## Comparison

| 特性 | CHATGLM-6B+Langchain | Dify |
|:---|:---:|:---:|
| 可使用数据库 | ✔️ | ✔️ |
| 支持的数据类型 | md、pdf、docx、txt | txt,html,markdown,pdf |
|最大文件|理论上是显存大小|15MB|
|数据上传|多个文件|单个文件|
|   可使用 GPT-4  |  ❌  |  ✔️   |
|API调用|❌|✔️|


