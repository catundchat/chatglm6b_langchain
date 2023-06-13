import os
import shutil

from app_modules.overwrites import postprocess
from app_modules.presets import *
from clc.langchain_application import LangChainApplication

# please change into your own configuration
class LangChainCFG:
    llm_model_name = 'THUDM/chatglm-6b-int4-qe'  # huggingface repository
    # llm_model_name = 'THUDM/chatglm-6b' # or local file path
    embedding_model_name = 'GanymedeNil/text2vec-large-chinese'  # huggingface: text to vector
    embedding_model_name = 'shibing624/text2vec-base-chinese' # huggingface: text to vector
    vector_store_path = './cache'
    docs_path = './docs'
    kg_vector_stores = {
        '中文维基百科': './cache/zh_wikipedia',
        '大规模金融研报': './cache/financial_research_reports',
        '心理学与生活': './cache/psychology_and_life',
        '初始化': './cache',
    }  
    # change it to your own knowledge database, if doesn't need it, set it "None"
    # kg_vector_stores=None
    patterns = ['模型问答', '知识库问答']  #
    n_gpus=1


config = LangChainCFG()
application = LangChainApplication(config)

application.source_service.init_source_vector()

def get_file_list():
    if not os.path.exists("docs"):
        return []
    return [f for f in os.listdir("docs")]


file_list = get_file_list()


def upload_file(file):
    if not os.path.exists("docs"):
        os.mkdir("docs")
    filename = os.path.basename(file.name)
    shutil.move(file.name, "docs/" + filename)
    # insert files into the first place of file_list 
    file_list.insert(0, filename)
    application.source_service.add_document("docs/" + filename)
    return gr.Dropdown.update(choices=file_list, value=filename)


def set_knowledge(kg_name, history):
    try:
        application.source_service.load_vector_store(config.kg_vector_stores[kg_name])
        msg_status = f'{kg_name}知识库已成功加载'
    except Exception as e:
        print(e)
        msg_status = f'{kg_name}知识库未成功加载'
    return history + [[None, msg_status]]


def clear_session():
    return '', None


def predict(input,
            large_language_model,
            embedding_model,
            top_k,
            use_web,
            use_pattern,
            history=None):
    # print(large_language_model, embedding_model)
    print(input)
    if history == None:
        history = []

    if use_web == '使用':
        web_content = application.source_service.search_web(query=input)
    else:
        web_content = ''
    search_text = ''
    if use_pattern == '模型问答':
        result = application.get_llm_answer(query=input, web_content=web_content)
        history.append((input, result))
        search_text += web_content
        return '', history, history, search_text

    else:
        resp = application.get_knowledge_based_answer(
            query=input,
            history_len=1,
            temperature=0.1,
            top_p=0.9,
            top_k=top_k,
            web_content=web_content,
            chat_history=history
        )
        history.append((input, resp['result']))
        for idx, source in enumerate(resp['source_documents'][:4]):
            sep = f'----------【搜索结果{idx + 1}：】---------------\n'
            search_text += f'{sep}\n{source.page_content}\n\n'
        print(search_text)
        search_text += "----------【网络检索内容】-----------\n"
        search_text += web_content
        return '', history, history, search_text


with open("assets/custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()
with gr.Blocks(css=customCSS, theme=small_and_beautiful_theme) as demo:
    gr.Markdown("""<h1><center>Chinese-LangChain</center></h1>
        <center><font size=3>
        </center></font>
        """)
    state = gr.State()

    with gr.Row():
        with gr.Column(scale=1):
            embedding_model = gr.Dropdown([
                "text2vec-base"
            ],
                label="Embedding model",
                value="text2vec-base")

            large_language_model = gr.Dropdown(
                [
                    "ChatGLM-6B-int4",
                ],
                label="large language model",
                value="ChatGLM-6B-int4")

            top_k = gr.Slider(1,
                              20,
                              value=4,
                              step=1,
                              label="检索top-k文档",
                              interactive=True)

            use_web = gr.Radio(["使用", "不使用"], label="web search",
                               info="是否使用网络搜索，使用时确保网络通常",
                               value="不使用"
                               )
            use_pattern = gr.Radio(
                [
                    '模型问答',
                    '知识库问答',
                ],
                label="模式",
                value='模型问答',
                interactive=True)

            kg_name = gr.Radio(list(config.kg_vector_stores.keys()),
                               label="知识库",
                               value=None,
                               info="使用知识库问答，请加载知识库",
                               interactive=True)
            set_kg_btn = gr.Button("加载知识库")

            file = gr.File(label="将文件上传到知识库库，内容要尽量匹配",
                           visible=True,
                           file_types=['.txt', '.md', '.docx', '.pdf']
                           )

        with gr.Column(scale=4):
            with gr.Row():
                chatbot = gr.Chatbot(label='Chinese-LangChain').style(height=400)
            with gr.Row():
                message = gr.Textbox(label='请输入问题')
            with gr.Row():
                clear_history = gr.Button("🧹 清除历史对话")
                send = gr.Button("🚀 发送")
            with gr.Row():
                gr.Markdown("""提醒：<br>
                                        [Chinese-LangChain](https://github.com/yanqiangmiffy/Chinese-LangChain) <br>
                                        有任何使用问题[Github Issue区](https://github.com/yanqiangmiffy/Chinese-LangChain)进行反馈. <br>
                                        """)
        with gr.Column(scale=2):
            search = gr.Textbox(label='搜索结果')

        # ============= 触发动作=============
        file.upload(upload_file,
                    inputs=file,
                    outputs=None)
        set_kg_btn.click(
            set_knowledge,
            show_progress=True,
            inputs=[kg_name, chatbot],
            outputs=chatbot
        )
        # 发送按钮 提交
        send.click(predict,
                   inputs=[
                       message,
                       large_language_model,
                       embedding_model,
                       top_k,
                       use_web,
                       use_pattern,
                       state
                   ],
                   outputs=[message, chatbot, state, search])

        # 清空历史对话按钮 提交
        clear_history.click(fn=clear_session,
                            inputs=[],
                            outputs=[chatbot, state],
                            queue=False)

        # 输入框 回车
        message.submit(predict,
                       inputs=[
                           message,
                           large_language_model,
                           embedding_model,
                           top_k,
                           use_web,
                           use_pattern,
                           state
                       ],
                       outputs=[message, chatbot, state, search])

demo.queue(concurrency_count=2).launch(
    server_name='0.0.0.0',
    server_port=8888,
    share=False,
    show_error=True,
    debug=True,
    enable_queue=True,
    inbrowser=True,
)
