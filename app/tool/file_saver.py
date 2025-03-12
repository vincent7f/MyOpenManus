import os
from typing import ClassVar

import aiofiles

from app.tool.base import BaseTool


class FileSaver(BaseTool):
    name: str = "file_saver"    
    short_description: str = "Save files locally, such as txt, py, html, etc."
    description: str = """Save content to a local file at a specified path within the sandbox directory.
Use this tool when you need to save text, code, or generated content to a file on the local filesystem.
The tool accepts content and a file path, and saves the content to that location within the sandbox directory.
All files will be saved under the sandbox directory for security reasons.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "(required) The content to save to the file.",
            },
            "file_path": {
                "type": "string",
                "description": "(required) The path where the file should be saved, including filename and extension. Will be created under the sandbox directory.",
            },
            "mode": {
                "type": "string",
                "description": "(optional) The file opening mode. Default is 'w' for write. Use 'a' for append.",
                "enum": ["w", "a"],
                "default": "w",
            },
        },
        "required": ["content", "file_path"],
    }

    # Define the sandbox directory with ClassVar type annotation
    SANDBOX_DIR: ClassVar[str] = "sandbox"

    async def execute(self, content: str, file_path: str, mode: str = "w") -> str:
        """
        Save content to a file at the specified path within the sandbox directory.

        Args:
            content (str): The content to save to the file.
            file_path (str): The path where the file should be saved (will be created under sandbox).
            mode (str, optional): The file opening mode. Default is 'w' for write. Use 'a' for append.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            # Ensure the file path is within the sandbox directory
            # Normalize the path to handle different path formats
            normalized_path = os.path.normpath(file_path)
            
            # Remove any leading directory separators and drive specifications
            normalized_path = normalized_path.lstrip(os.path.sep)
            if os.path.splitdrive(normalized_path)[0]:
                normalized_path = os.path.splitdrive(normalized_path)[1].lstrip(os.path.sep)
            
            # Ensure the path doesn't try to escape the sandbox using relative paths
            if ".." in normalized_path.split(os.path.sep):
                return "Error: Path cannot contain '..' to prevent directory traversal"
            
            # Create the full path within the sandbox directory
            safe_path = os.path.join(self.SANDBOX_DIR, normalized_path)
            
            # Ensure the directory exists
            directory = os.path.dirname(safe_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Write directly to the file
            async with aiofiles.open(safe_path, mode, encoding="utf-8") as file:
                await file.write(content)

            return f"Content successfully saved to {safe_path}"
        except Exception as e:
            return f"Error saving file: {str(e)}"
