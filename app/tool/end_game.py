from typing import List
from app.tool.base import BaseTool


class EndGame(BaseTool):
    name: str = "end_game"
    short_description: str = "Indicates that the task is completed and no further communication with AI is needed."
    description: str = """Indicates that the task is completed and no further communication with AI is needed.
Use this tool to indicate that the current task has been completed and the user does not need further interaction with the AI.
This tool does not perform any actual operations, it serves only as a marker.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "(Optional) Additional message when ending the task.",
            }
        },
        "required": [],
    }

    async def execute(self, message: str = "") -> str:
        """
        Indicates that the task is completed and no further communication with AI is needed.

        Args:
            message (str, optional): Additional message when ending the task.

        Returns:
            str: Message confirming that the task has ended.
        """
        print(f"Task completed: {message}")
        
        return f"Task completed, no further communication with AI is needed.{' ' + message if message else ''}" 