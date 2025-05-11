""" 系统工具箱 """

from datetime import datetime
import os
import requests
import importlib.resources
import yaml
from .action.scripts import display_dialog,run_shortcut

from .action.utils import create_func

def push_task(task:str, date:str):
    """推任务上去

    Args:
        task (str): 任务名
        date (str): 日期
    """
    requests.post(
        f"http://101.201.244.227:8000/action/{task}/{date}/execute",timeout=20)
    return 'success'

def reset_task(task:str,date:str)->str:
    """重置任务

    Args:
        task (str): 任务名
        date (str): 日期

    Returns:
        str: 系统消息
    """
    requests.post(
        f"http://101.201.244.227:8000/action/{task}/{date}/reset",timeout=20)
    return 'success'

def reset_tasks(date:str):
    """重置多任务

    Args:
        date (str): 日期
    """
    for task in ['同步进程池','同步预备池','同步就绪池','同步执行池',]:
        reset_task(task,date)



# Load configuration from YAML file
def load_config():
    with importlib.resources.open_text('reallife', 'config.yaml') as f:
        return yaml.safe_load(f)
    # with open('reallife/config.yaml', 'r', encoding='utf-8') as f:
    #     return yaml.safe_load(f)

class TaskInfo(Exception):
    """任务的抛出机制

    Args:
        Exception (_type_): 抛出
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def check_(func):
    """检查信息的封装

    Args:
        func (object): 信息方法

    Raises:
        TaskInfo: 遇到信息抛出消息等待被捕捉
    """
    result = func()
    if result:
        raise TaskInfo(result)

def check_action_(func,debug=True):
    """一个执行动作的配装

    Args:
        func (object): 动作函数
        debug (bool, optional): 是否debug模式. Defaults to True.
    """
    result = func()
    if result and debug:
        print(func.__name__)

def git_commit_something(repo:str,commit:str):
    """提交git commit 

    Args:
        repo (str): 仓库
        commit (str): 提交信息
    """
    os.system(f"cd /Users/zhaoxuefeng/GitHub/{repo};git add .; \
              git commit -m '{commit}' --allow-empty")


def failed_safe():
    # 安全开启 放弃
    '''
    查询session状态
    如果 当前session 状态是 session
        放弃session
    否则
        pass
    结束
    '''
    run_shortcut(shortcut_name="安全停止")


def task_with_time(task_name:str,time:int=1):
    """计时任务

    Args:
        task_name (str): 任务名
        time (int, optional): 费用. Defaults to 1.
    """
    run_shortcut(shortcut_name="执行计时任务",params=f"{task_name}${time}")
    display_dialog("计时结束", "需要结束计时任务吗?",button_text="结束",button_cancel=False)



class Date:
    """日期, 来控制系统时间

    Returns:
        object: 单例模式
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,date:str = None,time:str = None):
        # 只有第一次初始化时设置值，后续的初始化调用不会更改实例的值
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.date = date or datetime.today().strftime("%Y-%m-%d")
            self.time = time or datetime.today().strftime("%H:%M:%S")


class Setting:
    """日期, 来控制系统时间

    Returns:
        object: 单例模式
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 只有第一次初始化时设置值，后续的初始化调用不会更改实例的值
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.llm = None
            self.debug = None


