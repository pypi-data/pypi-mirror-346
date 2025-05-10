""" 执行任务 """
from .action.action import KanBanManager
from .utils import git_commit_something, failed_safe, task_with_time
from .action.scripts import display_dialog, get_choice_from_applescript
from . import KANBAN_PATH, WORK_CANVAS_PATH



def edit_coder(task:str):
    """编写代码

    Args:
        task (str): 任务
    """

    # 是否创建项目
    create_proj = False
    display_dialog("编写代码",f"是否创建新项目: {task}",button_text="开始",button_cancel=False)
    create_proj = display_dialog("编写代码",f"是否创建新项目: ",button_text="create",button_cancel=True)
    if create_proj == 'create':
        display_dialog("创建项目","1. pypi查重 \n  2. obsidian创建Reader | Docs \n \
                       3创建github仓库",button_text="确认",button_cancel=False)
        display_dialog("创建项目","初始化 uv init and 修改解释器 \
                       mkdocs new .  update  文档推送  创建文件夹,\
                       测试文件等  \
                       uv build publish  ",button_text="确认", button_cancel=False)
    print(task,'task')
    # TODO
    lst = ['coderTools','grapher','kanban']

    get_choice_from_applescript()
    all_options = ['coderTools','grapher','kanban','llmada','networkx','ob_ragtools','obsidian','promptlib',
                   'pypidoctor','readerLLamaIndex','reallife','tools','aiworker']
    choice = get_choice_from_applescript(
        prompt_text="请选择作为工作区的仓库:",
        list_title="工作区",
        options=all_options,
        default_option="kanban"
    )
    if choice:
        select = choice
    else:
        select = None
        raise Exception('选择失效')
    #
    display_dialog("编码与练习","基础逻辑",button_text="确认")
    task_with_time(task_name = task,time=40)
    display_dialog("编码与练习","测试与测试用例",button_text="确认")
    task_with_time(task_name = task,time=30)
    display_dialog("编码与练习","整理代码,注释,格式,文档与发布",button_text="确认")
    task_with_time(task_name = task,time=20)
    display_dialog("编码与练习","环境与推送新版本",button_text="确认")
    task_with_time(task_name = task,time=10)
    # 仓库$编写目标
    git_commit_something(select,task)
    failed_safe()

def test_and_study(task:str):
    """实验与学习

    Args:
        task (str): 任务
    """
    # 实验与学习
    display_dialog("实验与学习",f"请打开飞书会议, 标题为{task}",button_text="确认",button_cancel=False)
    task_with_time(task_name = task,time=60)
    display_dialog("实验与学习","自我审视+ 反思 + 分析笔记",button_text="确认",button_cancel=False)
    failed_safe()

def clean_and_update(task:str):
    """整理与优化

    Args:
        task (str): 任务
    """
    display_dialog("整理与优化",f"是否可以开始整理与优化: {task}",button_text="可以",button_cancel=False)
    task_with_time(task_name = task,time=20)
    failed_safe()

def design(task:str):
    """设计

    Args:
        task (str): 任务名
    """
    display_dialog("设计",f"准备开始设计: {task}",button_text="开始",button_cancel=False)
    task_with_time(task_name = task,time=60)
    git_commit_something("obsidian",task)
    failed_safe()

def meeting_and_talk(task:str):
    """开会与对齐

    Args:
        task (str): 任务名
    """
    display_dialog("开会与对齐",f"准备开会与对齐: {task}",button_text="开始",button_cancel=False)
    task_with_time(task_name = task,time=60)
    failed_safe()



def task_complete(task):

    # 任务已完成
    # multi_line_input = "真实人生-将对应的执行池内容添加到完成池"

    """
     script/kanban_manager_2over_function.py
    任务$canvas_path
     script/kanban_manager_2over.py
    """
    project_paths = WORK_CANVAS_PATH
    # task = "真实人生-将对应的执行池内容添加到完成池"
    project = task.split('-',1)[0]
    now_project_path = None
    for project_path in project_paths:
        if project == project_path.split('/')[-2]:
            now_project_path = project_path

    kbm = KanBanManager(kanban_path=KANBAN_PATH,pathlib=WORK_CANVAS_PATH)
    print('now_project_path',now_project_path)
    if now_project_path:
        kbm.sync_run2over(task,canvas_path=now_project_path)
    try:
        canvas_path = now_project_path.replace('\n','')
        kbm.sync_run2over(task,canvas_path =canvas_path)
    except AttributeError as e:
        print('noe')
    return 'success'

##########


def task_failed(task):
    # 任务未完成
    """
     script/kanban_manager_runner2order.py
    """
    kbm = KanBanManager(kanban_path=KANBAN_PATH,pathlib=WORK_CANVAS_PATH)

    kbm.sync_run2order()
