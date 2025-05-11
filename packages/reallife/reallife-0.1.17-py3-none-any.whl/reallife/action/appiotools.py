from datetime import datetime
from functools import lru_cache
import requests
from bs4 import BeautifulSoup
from llmada import BianXieAdapter

from reallife import Date
from .scripts import write_notes, generate_schedule, write_reminder, update_calulate
from .utils import read_file
from typing import Optional
import re


# 正则解析相关
def parse_execution_pool(text: str) -> Optional[str]:
    """
    使用正则表达式解析 "执行池" 内容
    :param text: 输入文本
    :return: 解析后的执行池内容
    """
    pattern = r'## 执行池\n(.+?)\n##'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1).strip()
        formatted_content = '\n'.join([line.strip()
                                       for line in content.split('\n') if line.strip()])
        return formatted_content
    else:
        return None


# 正则解析相关
def parse_execution_jiangyou_pool(text: str) -> Optional[str]:
    """
    使用正则表达式解析 "执行池" 内容
    :param text: 输入文本
    :return: 解析后的执行池内容
    """
    pattern = r'## 酱油池\n(.+?)\n##'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1).strip()
        formatted_content = '\n'.join([line.strip()
                                       for line in content.split('\n') if line.strip()])
        return formatted_content
    else:
        return None
    

from .scripts import get_page_html
import asyncio

class APPIO():
    def __init__(self):
        self.year = '2025年'
        self.kanban_path ="/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md"
        self.habit ="7点-9点起床洗漱, 12点到14点吃饭+午休,19点以后就是自由时间"

    def sync_calulate(self):

        # 读取文件
        text = read_file(self.kanban_path)

        if not text:
            print("文件内容为空，无法解析执行池")
            return

        # 解析执行池
        execution_pool = parse_execution_pool(text)

        if execution_pool:
            print(f"解析到的执行池内容:\n{execution_pool}")
            # 生成日程安排
            schedule_result = generate_schedule(execution_pool,habit =self.habit)
            xx = [i for i in schedule_result.split('\n') if i!='']
            for xp in xx:
                v = [(self.year+k if i<2 else k) for i,k in enumerate(xp.split('$'))]
                update_calulate(*v)

        else:
            print("未能解析到执行池内容")

    def sync_notes(self):
        # 读取文件
        date_c = Date()
        text = read_file(self.kanban_path)
        # 解析执行池
        execution_pool = parse_execution_jiangyou_pool(text)

        # 生成日程安排
        current_utc_time = datetime.utcnow()
        schedule_result = str(current_utc_time)[:10] + '\n' + execution_pool

        write_notes(schedule_result)
        for content in schedule_result.split("\n")[1:]:
            write_reminder(content, 
                list_name="工作",
                due_date=f"{date_c.date} {date_c.time}",
                priority=2,
                notes="")

    def sync_news(self,date:str):
        """同步资讯

        Args:
            date (str): 日期,字符串格式
        """
        def _get_articlie_link():
            # 目标网页的 URL
            url = "https://www.jiqizhixin.com"
            file_links = ["https://www.jiqizhixin.com/articles/2025-05-07-9",
                          "https://www.jiqizhixin.com/articles/2025-05-07-8",
                          "https://www.jiqizhixin.com/articles/2025-05-07-7",
                          "https://www.jiqizhixin.com/articles/2025-05-07-6",
                          ]
            return file_links
        
        def _get_articlie_link_2():
            # 目标网页的 URL
            url = "https://www.jiqizhixin.com"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/91.0.4472.124 Safari/537.36"
            }
            # 发送 HTTP 请求获取网页内容
            # response = requests.get(url)
            response = requests.get(url, headers=headers)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析 HTML 内容
                soup = BeautifulSoup(response.content, 'html.parser')

                # 提取所有文件链接
                file_links = []
                for link in soup.find_all('a', href=True,attrs={
                    'class': 'article-item__title t-strong js-open-modal',
                }):
                    href = link['href']
                    file_links.append(url + href)
            else:
                print("请求失败，状态码：", response.status_code)
            return file_links
        
        async def _get_context_from_jq_url(url):
            # 目标网页的 URL
             
            target_url = url
            html = await get_page_html(target_url)


            soup = BeautifulSoup(html, 'html.parser')

            # 提取网页中的文字内容
            text = soup.get_text()
            return text
            
        @lru_cache(maxsize=100)
        def _extra_text(text):
            template = """
            我希望你可以对一个内容进行汇总和总结, 我会给你一段网页的内容，你来用一些简短的文字告诉我这篇内容的主要信息, 以及列出其中相关的重点和链接

            网页内容:
            ---
            {text}
            ---

            输出信息:
            """

            llm = BianXieAdapter()
            llm.set_model("gpt-4o")
            prompt = template.format(text = text)
            completion = llm.product(prompt)
            return completion
        
        file_links = _get_articlie_link()
        print(file_links,'file_links')
        article = []
        for file_link in file_links:
            print(file_link)
            result = asyncio.run(_get_context_from_jq_url(file_link))
            xx = _extra_text(result)
            article.append(xx)

        file_path = f"/Users/zhaoxuefeng/GitHub/obsidian/工作/日记/{date}.md"
        with open(file_path,'a') as f:
            f.write("\n\n# 今日资讯\n---\n## 消息\n" +'\n\n---\n## 消息\n'.join(article))
