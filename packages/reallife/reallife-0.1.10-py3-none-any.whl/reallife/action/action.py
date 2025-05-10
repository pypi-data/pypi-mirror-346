""" 动作函数 """
from reallife import KANBAN_PATH,WORK_CANVAS_PATH,Date
from .utils import status
from .kanbantools import KanBanManager
from .appiotools import APPIO

date_c = Date()
date = date_c.date

@status(task="同步体重",date=date,run_only=True)
def sync_weight():
    """同步体重
    """
    kanb = KanBanManager(kanban_path=KANBAN_PATH,
                         pathlib=WORK_CANVAS_PATH)
    kanb.sync_weight(date)

@status(task="同步预备池",date=date,run_only=True)
def sync_ready_pool()->str:
    """同步预备池
    """
    kanb = KanBanManager(kanban_path=KANBAN_PATH,
                         pathlib=WORK_CANVAS_PATH)
    kanb.sync_ready()

@status(task="同步就绪池",date=date,run_only=True)
def sync_order_pool()->str:
    """同步就绪池
    """
    kanb = KanBanManager(kanban_path=KANBAN_PATH,
                         pathlib=WORK_CANVAS_PATH)
    kanb.sync_order()

@status(task="同步执行池",date=date,run_only=True)
def sync_run_pool()->str:
    """同步执行池
    """
    kanb = KanBanManager(kanban_path=KANBAN_PATH,
                         pathlib=WORK_CANVAS_PATH)
    kanb.sync_run()

@status(task="同步日历",date=date,run_only=True)
def sync_calulate()->str:
    """同步日历
    """
    appio = APPIO()
    appio.sync_calulate()


@status(task="同步备忘录",date=date,run_only=True)
def sync_note()->str:
    """同步备忘录
    """
    appio = APPIO()
    appio.sync_notes()

@status(task="同步备忘录夜",date=date,run_only=True)
def sync_note_night()->str:
    """同步备忘录夜
    """
    appio = APPIO()
    appio.sync_notes()

@status(task="回收未完成的任务",date=date,run_only=True)
def recycle_tasks()->str:
    """回收未完成的任务
    """
    kanb = KanBanManager(kanban_path=KANBAN_PATH,
                         pathlib=WORK_CANVAS_PATH)
    kanb.sync_run2order()

def add_tips(task:str)->str:
    """回收未完成的任务
    """
    kanb = KanBanManager(kanban_path=KANBAN_PATH,
                         pathlib=WORK_CANVAS_PATH)
    kanb.add_tips(task)
    return 'success'

@status(task="收集资讯",date=date,run_only=True)
def sync_news()->str:
    """收集资讯
    """
    appio = APPIO()
    appio.sync_news(date)
