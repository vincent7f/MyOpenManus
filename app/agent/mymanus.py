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
from app.tool.end_game import EndGame

class MyManus(ToolCallAgent):
    """
    A versatile general-purpose agent that uses planning to solve various tasks.

    This agent extends PlanningAgent with a comprehensive set of tools and capabilities,
    including Python execution, web browsing, file operations, and information retrieval
    to handle a wide range of user requests.
    """

    name: str = "MyManus"
    description: str = (
        "A versatile agent that can solve various tasks using multiple tools"
    )

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: str = None

    # Add general-purpose tools to the tool collection
    available_tools: ToolCollection = Field(
        default_factory=lambda: MyManus._create_tool_collection()
    )
    
    @classmethod
    def _get_tool_mapping(cls):
        """Get tool mapping table"""
        return {
            "PythonExecute": PythonExecute,
            "GoogleSearch": GoogleSearch,
            "BrowserUseTool": BrowserUseTool,
            "FileSaver": FileSaver,
            "Terminate": Terminate,
            "BingSearch": BingSearch,
            "EndGame": EndGame,
        }
    
    @classmethod
    def _create_tool_collection(cls) -> ToolCollection:
        """Create tool collection based on configuration"""
        # Get configured tool list
        configured_tools = config.tools.tool_list
        
        # Get tool mapping table
        tool_mapping = cls._get_tool_mapping()
        
        # If configured tool list is empty, use default tools
        if not configured_tools:
            # Use default tools
            tool_instances = [
                PythonExecute(),
                BrowserUseTool(),
                FileSaver(),
                Terminate(),
                BingSearch(),
            ]
        else:
            # Create tool instances based on configuration
            tool_instances = []
            for tool_name in configured_tools:
                if tool_name in tool_mapping:
                    tool_class = tool_mapping[tool_name]
                    tool_instances.append(tool_class())
            
            # Ensure at least one tool is available
            if not tool_instances:
                tool_instances.append(Terminate())

        # Ensure EndGame is always available
        tool_instances.append(EndGame())

        # Dynamically generate next_step_prompt
        cls._update_next_step_prompt(tool_instances)
        
        return ToolCollection(*tool_instances)
    
    @classmethod
    def _update_next_step_prompt(cls, tool_instances):
        """Dynamically update next_step_prompt based on tool instances"""
        # Generate tool introduction section
        tool_descriptions = []
        tool_details = []
        
        # Collect tool names and descriptions
        for tool in tool_instances:
            # Skip Terminate tool as it's for internal use
            if tool.name == "terminate":
                continue
                
            # Get tool class name (for display)
            tool_class_name = tool.__class__.__name__
            
            # Add to tool list
            tool_descriptions.append(tool_class_name)
            
            # Get tool's short description (first line)
            short_desc = tool.short_description.strip()
            tool_details.append(f"{tool_class_name}: {short_desc}")
        
        # Build prompt content
        if tool_descriptions:
            intro = f"You can interact with the computer using the following tools: {', '.join(tool_descriptions)}.\n\n"
            details = "\n\n".join(tool_details)
            conclusion = "\n\nBased on user needs, proactively select the most appropriate tool or combination of tools. For complex tasks, you can break down the problem and use different tools step by step to solve it. After using each tool, clearly explain the execution results and suggest the next steps. EndGame is a special tool that will end the conversation when the task is completed. Check whether the tool EndGame should be used to end the conversation."
            
            # Update next_step_prompt
            cls.next_step_prompt = intro + details + conclusion
        else:
            # If no tools available, use default prompt
            cls.next_step_prompt = NEXT_STEP_PROMPT
