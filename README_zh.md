[English](README.md) | 简体中文

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

5. 增加sandbox目录。新建的文件只能在保存在这个目录里，增加文件安全性。

6. 增加StoryCreator工具，用于生成创意故事。
   - 支持根据用户提供的提示生成原创故事
   - 可以指定故事的体裁（如奇幻、科幻、恐怖等）
   - 可以控制故事的长度（短、中、长）
   - 可以指定写作风格（如描述性、简洁、诗意等）
   - 可以指定故事中的主要角色
   
   使用示例可参考`examples/story_creator_example.py`文件。
