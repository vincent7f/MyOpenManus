English | [简体中文](README_zh.md)

NOTE: This page is generated and translated by Cursor.

For OpenManus documentation, please refer to the official GitHub:
https://github.com/mannaandpoem/OpenManus/blob/main/README.md

This version has been modified in the following aspects:

1. Added support for bing.com, making it more convenient for users in China.
2. Added automatic termination detection, which actively stops when AI does not call any tools. This is done through the addition of an EndGame Tool that allows AI to actively end the process.

   See the think method in the ToolCallAgent class, which added the following code:

   ```
   if "end_game" in [call.function.name for call in response.tool_calls]:
      logger.info(f"🏁 Special tool 'EndGame' has completed the task!")
      self.state = AgentState.FINISHED
      return False
   ```
3. Added the ability to specify which tools are available in the configuration file. For example, if you don't need Google, you can simply comment it out.

   ```
   # Tool configuration
   [tools]
   # List of enabled tools
   # Available options: "PythonExecute", "GoogleSearch", "BrowserUseTool", "FileSaver", "Terminate", "BingSearch"
   tool_list = [
       "PythonExecute",
       # "GoogleSearch",
       "BrowserUseTool",
       "FileSaver",
       "Terminate",
       "BingSearch",
   ]
   ```
4. Added minor debugging information.
5. Added a sandbox directory. New files can only be saved in this directory, enhancing file security.
6. Added StoryCreator tool for generating creative stories.

   - Supports generating original stories based on user-provided prompts
   - Can specify the genre of the story (e.g., fantasy, sci-fi, horror, etc.)
   - Can control the length of the story (short, medium, long)
   - Can specify writing style (e.g., descriptive, concise, poetic, etc.)
   - Can specify main characters to include in the story

   **Story Example: Guan Yu vs Qin Qiong**

   > PROMPT: Write a short story about Guan Yu fighting Qin Qiong, around 600 words, and save the story
   >

   [https://github.com/vincent7f/MyOpenManus/blob/main/results/%E5%85%B3%E5%85%AC%E6%88%98%E7%A7%A6%E7%90%BC.md](https://github.com/vincent7f/MyOpenManus/blob/main/results/%E5%85%B3%E5%85%AC%E6%88%98%E7%A7%A6%E7%90%BC.md)

   **Composition Example: Environmental Short Story**

   > PROMPT (AI-generated): Please write a short story about environmental protection in a sci-fi style, with the main character being a cat that can communicate with humans.
   >

   [https://github.com/vincent7f/MyOpenManus/blob/main/results/%E7%8E%AF%E4%BF%9D%E7%9A%84%E7%9F%AD%E6%95%85%E4%BA%8B.txt](https://github.com/vincent7f/MyOpenManus/blob/main/results/%E7%8E%AF%E4%BF%9D%E7%9A%84%E7%9F%AD%E6%95%85%E4%BA%8B.txt)
