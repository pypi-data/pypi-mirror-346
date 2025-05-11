""" 脚本交互 """

import subprocess
from datetime import datetime
from llama_index.core import PromptTemplate
from promptlibz import Templates,TemplateType
from llmada import BianXieAdapter
import shlex

def give_a_task_time(task:str)->str:
    llm = BianXieAdapter()
    llm.set_model("gemini-2.5-flash-preview-04-17-nothinking")

    template = Templates(TemplateType.ESTIMATE_DURATION)
    prompt = template.format(task=task)

    completion = llm.product(prompt)
    return completion + " "+ task

def generate_schedule(text: str,habit: str="") -> str:
    """
    使用 GPT 模型生成日程安排
    :param text: 输入文本
    :return: 生成的日程安排结果
    """
    llm = BianXieAdapter()

    template = Templates(TemplateType.GENERATE_SCHEDULE)
    current_utc_time = str(datetime.today())[:-7]
    prompt = template.format(text=text,habit=habit,current_utc_time = current_utc_time)
    completion = llm.product(prompt)
    return completion

from .utils import extract_type_code

def judge_type(task:str):
    """判断任务类型

    Args:
        task (str): 任务
    """

    llm = BianXieAdapter()
    llm.set_model('gpt-4.1-mini')
    prompt = Templates(TemplateType.JUDGETYPE)
    completion = llm.product(prompt.format(task=task))
    return extract_type_code(completion)


def run_applescript(script:str)->str:
    """运行apple script 脚本

    Args:
        script (str): applescript 脚本

    Returns:
        str: 脚本的输出
    """
    result = subprocess.run(['osascript', '-e', script],capture_output=True,check=False)
    return result.stdout.decode().replace('\n','')

def run_shortcut(shortcut_name:str,params:str=None):
    """运行快捷指令

    Args:
        shortcut_name (str, optional): 快捷指令名称. Defaults to ''.
        params (str, optional): 参数. Defaults to None.

    Returns:
        str: 快捷指令的输出
    """
    # 安全开启 放弃
    if params is None:
        result = run_applescript(f'''tell application "Shortcuts"
            run shortcut "{shortcut_name}"
        end tell''')
    else:
        result = run_applescript(f'''tell application "Shortcuts"
            run shortcut "{shortcut_name}" with input "{params}"
        end tell''')
    return result


def write_notes(content):
    content = content.replace("\n",",").replace('- [ ]','')
    # 构造 AppleScript 脚本  TODO 解决无法换行问题
    script = f'''
    tell application "Notes"
        activate
        -- 获取默认账户
        set defaultAccount to default account
        -- 创建一个新的备忘录
        set newNote to make new note in defaultAccount
        -- 写入文本信息到备忘录
        set body of newNote to "{content}"
        -- 显示新创建的备忘录
        show newNote
    end tell
    '''

    # 执行 AppleScript 脚本
    subprocess.run(['/usr/bin/osascript', '-e', script])



def write_reminder(content, 
                    list_name="Reminders",  # 指定列表名称
                    due_date=None,         # 设置到期日
                    priority=None,         # 设置优先级(1-4)
                    notes=""               # 添加备注
                ):
    # 预处理内容
    processed_content = content.replace('\n', ' ').replace('- [ ]', '').strip()
    processed_content = processed_content.replace('"', '\\"')
    notes = notes.replace('"', '\\"')
    
    # 构建属性字典
    properties = [f'name:"{processed_content}"']
    if due_date:
        properties.append(f'due date:(date "{due_date}")')
    if priority and 1 <= priority <= 4:
        properties.append(f'priority:{priority}')
    if notes:
        properties.append(f'body:"{notes}"')
    
    # 构造AppleScript
    script = f'''
    tell application "Reminders"
        activate
        set targetList to list "{list_name}"
        make new reminder in targetList with properties {{{', '.join(properties)}}}
    end tell
    '''
    script = f'''
    tell application "Reminders"
        activate
        set targetList to default list
        set newReminder to make new reminder in targetList with properties {{{', '.join(properties)}}}
        show newReminder
    end tell
    '''    
    subprocess.run(['/usr/bin/osascript', '-e', script])

def update_calulate(start_date = "2025年4月25日8:00",
                    end_date = "2025年4月25日9:00",
                    event_name = "会议",
                    ):
    script = PromptTemplate(template='''
    tell application "Calendar"
        activate
        tell calendar "Obsidian" -- 或者 tell first calendar
            -- nih
            -- 假设您已经将开始时间、结束时间和标题存储在变量中
            set theStartDate to date "{start_date}" -- 示例日期时间
            set theEndDate to date "{end_date}" -- 示例日期时间
            set theSummary to "{event_name}" -- 示例标题
            make new event with properties {summary:theSummary, start date:theStartDate, end date:theEndDate}
        end tell
    end tell
    ''')

    # 构造 AppleScript 脚本
    scrip = script.format(start_date=start_date,end_date=end_date,event_name=event_name)

    # 执行 AppleScript 脚本
    subprocess.run(['/usr/bin/osascript', '-e', scrip])




def get_choice_from_applescript(prompt_text="请从下面的列表中选择一项：", list_title="请选择", options=None, default_option=None):
    """
    使用 AppleScript 显示一个列表选择框，并返回用户的选择。

    Args:
        prompt_text (str): 显示在列表上方的提示信息。
        list_title (str): 选择框窗口的标题。
        options (list): 供用户选择的字符串列表。
        default_option (str): 默认选中的项目。

    Returns:
        str: 用户选择的项目。
        None: 如果用户取消或发生错误。
    """
    import sys
    if sys.platform != 'darwin':
        print("错误：此功能仅在 macOS 上可用。")
        return None

    if options is None:
        options = ["选项 A", "选项 B", "选项 C", "另一个选项"] # 默认选项

    # 将 Python 列表转换为 AppleScript 列表字符串: {"item1", "item2", ...}
    applescript_list = '{' + ', '.join([f'"{item}"' for item in options]) + '}'

    # 构建 AppleScript
    script = f'''
    try
        set myList to {applescript_list}
        set thePrompt to "{prompt_text}"
        set theTitle to "{list_title}"
        '''

    # 添加默认项（如果提供且有效）
    if default_option and default_option in options:
        script += f'set defaultChoice to {{"{default_option}"}}\n'
        script += f'set theChoice to choose from list myList with title theTitle with prompt thePrompt default items defaultChoice'
    else:
        script += f'set theChoice to choose from list myList with title theTitle with prompt thePrompt'

    script += f'''
        -- 检查用户是否点击了取消按钮
        if theChoice is false then
            error number -128 -- 引发标准取消错误
        else
            -- 返回选择的第一个项目 (choose from list 返回列表)
            return item 1 of theChoice
        end if
    on error number -128
        -- 捕获取消错误，可以返回特定值或让 Python 处理异常
         return "USER_CANCELLED" -- 返回一个特殊标记
         -- 或者你可以不处理，让 osascript 返回非零退出码
         -- error number -128
    end try
    '''

    try:
        # 不需要 shlex.quote
        result = subprocess.run(
            ['osascript', '-e', script],
            check=True,          # 如果 osascript 返回非零则抛出异常
            capture_output=True, # 捕获 stdout/stderr
            text=True,           # 将输出解码为文本
            encoding='utf-8'     # 指定编码
        )
        output = result.stdout.strip()
        if output == "USER_CANCELLED":
            print("用户取消了选择。")
            return None
        else:
            return output # 返回用户的选择
    except subprocess.CalledProcessError as e:
        # osascript 执行失败或返回错误码 (例如，如果我们在 AppleScript 中直接 error -128)
        # 检查 stderr 获取更多信息
        error_message = e.stderr.strip()
        if "-128" in error_message: # 检查是否是用户取消的标准错误代码
             print("用户取消了选择 (通过错误码捕获)。")
        else:
             print(f"执行 AppleScript 时出错: {e}")
             print(f"错误详情: {error_message}")
        return None
    except FileNotFoundError:
        print("错误: 'osascript' 命令未找到。请确保你在 macOS 上运行。")
        return None
    except Exception as e:
        print(f"发生意外错误: {e}")
        return None




def display_dialog(title, text, button_text="OK",button_cancel = True):
    # # --- 示例 ---
    # display_dialog("任务完成", "您的 Python 脚本已成功执行！")
    # display_dialog("用户输入", "请输入一些内容：", button_text="确认") # 这是一个简单的信息框，获取输入更复杂
    """使用 AppleScript 显示一个简单的对话框"""
    if button_cancel:
        script = f'''
        display dialog "{text}" with title "{title}" buttons {{"cancel","{button_text}"}} \
            default button "{button_text}"
        '''
    else:
        script = f'''
        display dialog "{text}" with title "{title}" buttons {{"{button_text}"}} \
            default button "{button_text}"
        '''

    try:
        # 使用 shlex.quote 防止注入
        shlex.quote(script)
        result = subprocess.run(['osascript', '-e', script],
                                check=True, capture_output=True, text=True)
        # print(result.stdout)
        return result.stdout[16:-1]
    except subprocess.CalledProcessError as e:
        print(f"Error displaying dialog: {e}")
    except FileNotFoundError:
        print("Error: 'osascript' command not found. Ensure you are on macOS.")

def display_dialog_for_end(title, text, button_text="OK",button_text2="OK",button_cancel = True):
    # # --- 示例 ---
    # display_dialog("任务完成", "您的 Python 脚本已成功执行！")
    # display_dialog("用户输入", "请输入一些内容：", button_text="确认") # 这是一个简单的信息框，获取输入更复杂
    """使用 AppleScript 显示一个简单的对话框"""
    if button_cancel:
        script = f'''
        display dialog "{text}" with title "{title}" buttons {{"cancel","{button_text}","{button_text2}"}} \
            default button "{button_text}"
        '''
    else:
        script = f'''
        display dialog "{text}" with title "{title}" buttons {{"{button_text}"}} \
            default button "{button_text}"
        '''

    try:
        # 使用 shlex.quote 防止注入
        shlex.quote(script)
        result = subprocess.run(['osascript', '-e', script],
                                check=True, capture_output=True, text=True)
        # print(result.stdout)
        return result.stdout[16:-1]
    except subprocess.CalledProcessError as e:
        print(f"Error displaying dialog: {e}")
    except FileNotFoundError:
        print("Error: 'osascript' command not found. Ensure you are on macOS.")


import asyncio
import pyppeteer

async def get_page_html(url: str) -> str | None:
    """
    使用 pypeteer 访问指定 URL，等待页面完全加载后获取 HTML 内容。

    Args:
        url: 要访问的网页 URL。

    Returns:
        页面的 HTML 内容字符串，如果发生错误则返回 None。
    """
    browser = None # 初始化 browser 变量，以便在 finally 块中检查
    try:
        # 启动浏览器
        # headless=True 表示无头模式运行（不显示浏览器窗口）
        # 可以设置为 headless=False 进行调试，会弹出一个浏览器窗口
        print("正在启动浏览器...")
        browser = await pyppeteer.launch(headless=True, 
                                         userDataDir='/Users/zhaoxuefeng/GitHub/test1/userdata3', 
                                         args=['--no-sandbox']) # 添加 --no-sandbox 参数，某些环境下可能需要

        page = await browser.newPage()

        print(f"正在访问网页: {url}")
        # 导航到指定 URL 并等待页面完全加载
        # waitUntil='networkidle0' 会等待直到网络连接数降至 0 且持续 500ms
        # 这通常意味着页面上的主要资源（包括通过 JS 加载的）都已经加载完成
        # 其他选项包括 'load', 'domcontentloaded', 'networkidle2'
        await page.goto(url, waitUntil='networkidle0')
        print("页面加载完毕，正在获取 HTML 内容...")

        # 获取页面的完整 HTML 内容
        html_content = await page.content()
        print("HTML 内容获取成功。")

        return html_content

    except pyppeteer.errors.TimeoutError:
        print(f"访问 {url} 超时。")
        return None
    except Exception as e:
        print(f"访问 {url} 时发生错误: {e}")
        return None
    finally:
        # 关闭浏览器实例
        if browser:
            print("正在关闭浏览器...")
            await browser.close()
            print("浏览器已关闭。")

