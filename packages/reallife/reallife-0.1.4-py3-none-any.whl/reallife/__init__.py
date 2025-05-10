""" 初始化 设定值"""

from llmada import BianXieAdapter
from .utils import Date, Setting, load_config
# Load configuration
config = load_config()
KANBAN_PATH = config.get('KANBAN_PATH', '')
WORK_CANVAS_PATH = config.get('WORK_CANVAS_PATH', [])

setting = Setting()
llm = BianXieAdapter()
llm.set_model("gemini-2.5-flash-preview-04-17-nothinking")
setting.llm = llm
setting.debug = False

# Date(date = '2025-01-01',time = '14:40:10')
Date()
