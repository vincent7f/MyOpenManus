from typing import Dict, Optional

from app.logger import logger
from app.schema import Message
from app.tool.base import BaseTool
from app.llm import LLM, get_llm
from pydantic import Field


class StoryCreator(BaseTool):
    """Tool for creating stories based on user prompts using AI."""
    
    name: str = "story_creator"
    short_description: str = "Creates a story based on user prompt."
    description: str = (
        "Creates a creative story based on the user's prompt. "
        "You can specify genre, length, and other parameters to customize the story."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The main prompt or idea for the story.",
            },
            "genre": {
                "type": "string",
                "description": "The genre of the story (e.g., fantasy, sci-fi, romance, horror, etc.).",
            },
            "length": {
                "type": "string",
                "description": "The desired length of the story (short, medium, long).",
                "enum": ["short", "medium", "long"],
            },
            "style": {
                "type": "string",
                "description": "The writing style for the story (e.g., descriptive, concise, poetic, etc.).",
            },
            "characters": {
                "type": "string",
                "description": "Description of main characters to include in the story.",
            },
        },
        "required": ["prompt"],
    }
    
    # 添加llm字段声明
    llm: Optional[LLM] = Field(default=None)
    
    def __init__(self, llm=None):
        """Initialize the StoryCreator tool.
        
        Args:
            llm: The language model to use for generating stories
        """
        super().__init__()
        self.llm = llm
    
    async def execute(
        self, 
        prompt: str, 
        genre: Optional[str] = None, 
        length: Optional[str] = "medium", 
        style: Optional[str] = None,
        characters: Optional[str] = None
    ) -> str:
        """Execute the story creation with the given parameters.
        
        Args:
            prompt: The main prompt or idea for the story
            genre: The genre of the story
            length: The desired length of the story
            style: The writing style for the story
            characters: Description of main characters
            
        Returns:
            The generated story as a string
        """
        # 如果没有提供llm，尝试获取全局llm
        if not self.llm:
            try:
                self.llm = get_llm()
                logger.info("🔄 Using global LLM for story creation")
            except Exception as e:
                return f"Error: No language model available for story creation. {str(e)}"
        
        # 如果仍然没有llm，返回错误
        if not self.llm:
            return "Error: No language model available for story creation."
        
        # Prepare system message with instructions
        system_message = self._create_system_message(genre, length, style, characters)
        
        # Prepare user message with the prompt
        user_message = Message.user_message(prompt)
        
        logger.info(f"🖋️ Creating a story with prompt: {prompt}")
        
        try:
            # Call the language model to generate the story
            response = await self.llm.ask_tool(
                messages=[user_message],
                system_msgs=[system_message] if system_message else None,
                tools=None,  # No tools needed for story generation
                tool_choice="none",  # Don't use tool calls for story generation
            )
            
            # Extract the story content from the response
            story = response.content
            
            logger.info(f"✨ Story created successfully! ({len(story)} characters)")
            
            return story
        except Exception as e:
            error_msg = f"Failed to create story: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
    
    def _create_system_message(
        self, 
        genre: Optional[str], 
        length: Optional[str], 
        style: Optional[str],
        characters: Optional[str]
    ) -> Message:
        """Create a system message with instructions for story generation.
        
        Args:
            genre: The genre of the story
            length: The desired length of the story
            style: The writing style for the story
            characters: Description of main characters
            
        Returns:
            A system message with instructions
        """
        # Build the system prompt based on provided parameters
        instructions = [
            "You are a creative storyteller. Create an engaging and original story based on the user's prompt.",
        ]
        
        # Add genre instruction if provided
        if genre:
            instructions.append(f"The story should be in the {genre} genre.")
        
        # Add length instruction
        word_count = {
            "short": "500-1000",
            "medium": "1500-2500",
            "long": "3000-5000"
        }.get(length, "1500-2500")
        instructions.append(f"The story should be approximately {word_count} words long.")
        
        # Add style instruction if provided
        if style:
            instructions.append(f"Write in a {style} style.")
        
        # Add characters instruction if provided
        if characters:
            instructions.append(f"Include these characters: {characters}")
        
        # Add final formatting instructions
        instructions.append("Format the story with proper paragraphs, dialogue, and structure.")
        instructions.append("Be creative, original, and engaging.")
        
        # Join all instructions into a single system prompt
        system_prompt = "\n".join(instructions)
        
        return Message.system_message(system_prompt) 