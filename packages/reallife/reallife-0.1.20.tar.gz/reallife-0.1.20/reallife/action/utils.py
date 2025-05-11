import functools
import requests

# 数据读取相关
def read_file(file_path: str) -> str:
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容字符串
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
        return ""

## 其他

def status(task:str,date:str,run_only = False):
    """执行任务并记录执行状态, 如果已经执行了则不再执行(每日)

    Args:
        task (str): 任务名称
        date (str): 2019-12-12

    Returns:
        str: '是否成功'
    """
    def outer_packing(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            response = requests.get(
                f"http://101.201.244.227:8000/action/{task}/{date}/status",timeout=20)
            if response.json().get('status') == '未执行':
                result = func(*args, **kwargs)
            else:
                result = None
            if run_only:
                response = requests.post(
                f"http://101.201.244.227:8000/action/{task}/{date}/execute",timeout=20)
            return result
        return wrapper
    return outer_packing


def create_func(task:str,date:str)->object:
    """创建特定对象

    Args:
        task (str): 任务
        date (str, optional): 日期. Defaults to date.

    Returns:
        object: 状态函数
    """
    @status(task=task,date=date)
    def func_():
        """提醒

        Returns:
            str: 任务内容
        """
        return task
    return func_


import re


def extract_type_code(text: str)->str:
    """从文本中提取python代码

    Args:
        text (str): 输入的文本。

    Returns:
        str: 提取出的python文本
    """
    pattern = r'```type([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches[0].replace('\n','')


##
import os


def git_pull(repo: str):
    """拉取 git 仓库最新更改
    Args:
        repo (str): 仓库名称 (例如 'my-awesome-project')
    """
    repo_path = os.path.join("/Users/zhaoxuefeng/GitHub", repo)
    # 切换目录并执行 git pull
    # git pull 默认会尝试拉取当前分支对应的远程分支
    command = f"cd {repo_path} && git pull"
    print(f"Executing command: {command}") # 打印执行的命令，方便调试
    os.system(command)
    print(f"Pull command finished for repo: {repo}")


def git_push(repo: str,commit:str='test'):
    """推送 git 仓库更改到远程
    Args:
        repo (str): 仓库名称 (例如 'my-awesome-project')
    """
    repo_path = os.path.join("/Users/zhaoxuefeng/GitHub", repo)
    # 切换目录并执行 git push
    # git push 默认会尝试推送当前分支到其对应的远程分支
    command = f"cd {repo_path} && git commit -a -m {commit} && git push"
    print(f"Executing command: {command}") # 打印执行的命令，方便调试
    os.system(command)
    print(f"Push command finished for repo: {repo}")
