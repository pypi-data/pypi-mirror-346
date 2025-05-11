
prompt = """
你是一个计划构筑师,根据我的任务帮我拆分编写工作流程与计划, 使用mermaid 的方式构建.

注意: 相对简明, mermaid格式简单,清晰

---
任务:
{任务}

"""



import requests
from bs4 import BeautifulSoup
import os
# 配置相关
from llama_index.llms.openai import OpenAI

import requests
from bs4 import BeautifulSoup
from datetime import datetime

from functools import lru_cache


# 初始化 LLM 和 Embedding 模型
llm = OpenAI(
    model="gpt-4.1-2025-04-14",
    api_key=os.getenv("BIANXIE_API_KEY"),
    api_base='https://api.bianxieai.com/v1',
    temperature=0.1,
)
obsidian = "/Users/zhaoxuefeng/GitHub/obsidian"

def main(task:str):
    return llm.complete(prompt.format(任务=task))



if __name__ == "__main__":
    import sys
    multi_line_input = sys.stdin.read()
    print(main(multi_line_input))