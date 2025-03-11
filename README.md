English | [中文](README_zh.md) | [한국어](README_ko.md) | [日本語](README_ja.md)

Link to official site:
https://github.com/mannaandpoem/OpenManus

This version has been modified in the following aspects:

1. Added support for bing.com, making it more convenient for users in China.
2. Added automatic termination detection, which actively stops when AI does not call any tools.

   See the think method in the ToolCallAgent class, which added the following code:

   ```
           if not response.tool_calls or len(response.tool_calls) <= 0:
               logger.info(f"🤔 Hmm, {self.name} didn't select any tools to use, so it will stop thinking")
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
4. Added minor call information.

