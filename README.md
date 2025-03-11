English | [简体中文](README_zh.md)

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

