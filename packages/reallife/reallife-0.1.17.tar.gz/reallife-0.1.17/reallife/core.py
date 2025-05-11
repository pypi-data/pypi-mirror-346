""" 提供对外的方法 提供一些带状态的消息 """

from datetime import datetime
from .action.action import sync_calulate,sync_weight,sync_ready_pool,sync_order_pool,add_tips
from .action.action import sync_run_pool, sync_note, sync_news, sync_note_night, recycle_tasks
from .action.action import git_obsidian_pull, git_obsidian_push,git_obsidian_pull1,git_obsidian_push1

from .nodes import clean_and_update,edit_coder, test_and_study
from .nodes import design, meeting_and_talk
from .nodes import task_failed,task_complete

from .action.scripts import run_shortcut, display_dialog, display_dialog_for_end, judge_type
from .utils import check_action_,check_, TaskInfo
from .utils import create_func,push_task
from reallife import Date, Setting


def morning()->str:
    """清晨动作

    Returns:
        str: 系统消息
    """
    date = Date().date

    try:
        check_(create_func(task='记录灵感',date=date))
        check_(create_func(task='记录体重',date=date))
        check_(create_func(task='跑步',date=date))
        check_(create_func(task='记录吃了什么',date=date))
        check_(create_func(task='洗漱护肤',date=date))
        check_(create_func(task='收拾家与锻炼',date=date))
    except TaskInfo as e:
        return e

    return {"message":"success"}

def start_work(debug=True)->str:
    """开工

    Args:
        debug (bool, optional): 是否调试模式. Defaults to True.

    Returns:
        str: 系统消息
    """
    date = Date().date
    try:
        check_(create_func(task='上班打卡',date=date))
        check_action_(git_obsidian_pull,debug)
        check_action_(sync_ready_pool,debug)
        check_action_(sync_order_pool,debug)
        check_action_(sync_weight,debug)
        check_action_(git_obsidian_push,debug)
        check_(create_func(task='调整优先级',date=date))
        check_action_(git_obsidian_pull1,debug)
        check_action_(sync_run_pool,debug)
        # check_action_(sync_news) # 对方改版了,等着用pypeteer去做吧
        check_action_(git_obsidian_push1,debug)
        check_action_(sync_calulate,debug)
        check_action_(sync_note,debug)
        check_(create_func(task='拉取git',date=date))
        check_(create_func(task='倒水茶水',date=date))
        # bulid知识库
    except TaskInfo as e:
        return e

    return {"message":"success"}

def tasks():
    """任务列表

    Returns:
        str: 系统消息
    """
    date = Date().date
    try:
        check_(create_func(task='写下灵感',date=date))
        check_(create_func(task='跟进阻塞池',date=date))
        task = run_shortcut("获取任务")
        print("task:",task)
        if not task:
            return '无任务'
        task_type = judge_type(task)
        if task_type == "代码与练习":
            edit_coder(task)
        elif task_type == "实验与学习":
            test_and_study(task)
        elif task_type == "整理与优化":
            clean_and_update(task)
        elif task_type == "设计":
            design(task)
        elif task_type == "开会与对齐":
            meeting_and_talk(task)
        else:
            print('新的类别')
            # 开会与对齐
            meeting_and_talk(task)

        task_result = display_dialog_for_end("判断",f"任务是否完成: ",button_text="complete",button_text2="blockage",button_cancel=True)

        if task_result == 'complete':
            # 完成任务
            task_complete(task=task)
        
        elif task_result == 'blockage':
            # 任务阻塞
            #TODO
            pass

        else:
            # 完成未任务
            task_failed(task=task)

        
        # 移除完成的任务
        run_shortcut("移除完成的任务",task)

    except TaskInfo as e:
        return e

    return {"message":"success"}

def finish_work():
    """收工动作

    Returns:
        str: 系统信息
    """
    date = Date().date
    try:
        #TODO 知识库整理
        check_action_(recycle_tasks)
        check_action_(sync_note_night)
        check_(create_func(task='检查和收集咨询',date=date))
        check_(create_func(task='检查是否仍在禅模式',date=date))
        check_(create_func(task='检测git提交',date=date))
        check_(create_func(task='下班打卡',date=date))
        check_(create_func(task='倒水茶水晚上',date=date))
    except TaskInfo as e:
        return e
    return {"message":"success"}

def evening()->str:
    """晚间休息的任务

    Returns:
        str: 系统消息
    """
    date = Date().date
    try:
        check_(create_func(task='整理家里和猫猫',date=date))
        check_(create_func(task='晚上洗漱,刷牙,护肤',date=date))
        check_(create_func(task='锻炼',date=date))
        check_(create_func(task='睡觉',date=date))
    except TaskInfo as e:
        return e

    return {"message":"success"}

def rest()->str:
    date = Date().date
    try:
        check_(create_func(task='吃早饭',date=date))
        check_(create_func(task='洗漱',date=date))
        check_(create_func(task='锻炼',date=date))
        check_(create_func(task='睡觉',date=date))
    except TaskInfo as e:
        return e
    return {"message":"success"}

from chinese_calendar import is_workday
from datetime import datetime

def receive()->str:
    """领取一个任务(普通模式)

    Returns:
        str: 任务信息
    """
    time = Date().time
    date = Date().date
    DEBUG = Setting().debug
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    if is_workday(date_obj):
        time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
        # Create datetime objects once to avoid repetition
        time_8_50 = datetime.strptime(date + " 8:50:00", "%Y-%m-%d %H:%M:%S")
        time_10_00 = datetime.strptime(date + " 10:00:00", "%Y-%m-%d %H:%M:%S") 
        time_18_00 = datetime.strptime(date + " 18:00:00", "%Y-%m-%d %H:%M:%S")
        time_19_00 = datetime.strptime(date + " 19:00:00", "%Y-%m-%d %H:%M:%S")
        time_23_00 = datetime.strptime(date + " 23:00:00", "%Y-%m-%d %H:%M:%S")
        
        if time < time_8_50:
            return morning()

        elif time_8_50 < time <= time_10_00:
            return start_work(debug=DEBUG)

        elif time_10_00 <= time < time_18_00:
            return tasks()

        elif time_18_00 <= time < time_19_00:
            return finish_work()

        elif time_19_00 <= time < time_23_00:
            return evening()

        return 'success'
    else:
        return rest()


def complete():
    """完成当前任务
    """
    date = Date().date
    task = receive()
    result = push_task(task=task,date=date)
    return {"message":result}


def add_tip(task:str):
    return add_tips(task)



#TODO 强化型健身  1周一次 在突破技能   5000米 + 负重 + 拳击