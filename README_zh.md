
OpenManus的说明，请详见官方github:
https://github.com/mannaandpoem/OpenManus/blob/main/README_zh.md

这个版本主要是对以下几方面进行了修改：

1. 增加提供对bing.com的支持，方便国内用户使用。
2. 增加自动结束检测，当AI不调用任何工具时，主动停止。通过增加EndGame这个Tool，让AI去主动结束。

   详见ToolCallAgent类的think方法，增加了以下代码

   ```
   if "end_game" in [call.function.name for call in response.tool_calls]:
      logger.info(f"🏁 Special tool 'EndGame' has completed the task!")
      self.state = AgentState.FINISHED
      return False
   ```
3. 增加配置文件中指定那些工具可以，例如不需要google的话，直接注释掉就行了。

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
4. 增加了小量调试信息。
