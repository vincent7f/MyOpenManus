from pydantic import Field

from app.agent.toolcall import ToolCallAgent
from app.config import config
from app.prompt.manus import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from app.tool import Terminate, ToolCollection
from app.tool.browser_use_tool import BrowserUseTool
from app.tool.file_saver import FileSaver
from app.tool.google_search import GoogleSearch
from app.tool.python_execute import PythonExecute
from app.tool.bing_search import BingSearch

class Manus(ToolCallAgent):
    """
    A versatile general-purpose agent that uses planning to solve various tasks.

    This agent extends PlanningAgent with a comprehensive set of tools and capabilities,
    including Python execution, web browsing, file operations, and information retrieval
    to handle a wide range of user requests.
    """

    name: str = "Manus"
    description: str = (
        "A versatile agent that can solve various tasks using multiple tools"
    )

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: str = NEXT_STEP_PROMPT

    # Add general-purpose tools to the tool collection
    available_tools: ToolCollection = Field(
        default_factory=lambda: Manus._create_tool_collection()
    )
    
    @classmethod
    def _get_tool_mapping(cls):
        """获取工具映射表"""
        return {
            "PythonExecute": PythonExecute,
            "GoogleSearch": GoogleSearch,
            "BrowserUseTool": BrowserUseTool,
            "FileSaver": FileSaver,
            "Terminate": Terminate,
            "BingSearch": BingSearch,
        }
    
    @classmethod
    def _create_tool_collection(cls) -> ToolCollection:
        """根据配置创建工具集合"""
        # 获取配置的工具列表
        configured_tools = config.tools.tool_list
        
        # 获取工具映射表
        tool_mapping = cls._get_tool_mapping()
        
        # 如果配置的工具列表为空，使用默认工具
        if not configured_tools:
            return ToolCollection(
                PythonExecute(),
                BrowserUseTool(),
                FileSaver(),
                Terminate(),
                BingSearch(),
            )
        
        # 根据配置创建工具实例
        tool_instances = []
        for tool_name in configured_tools:
            if tool_name in tool_mapping:
                tool_class = tool_mapping[tool_name]
                tool_instances.append(tool_class())
        
        # 确保至少有一个工具可用
        if not tool_instances:
            tool_instances.append(Terminate())
        
        return ToolCollection(*tool_instances)
