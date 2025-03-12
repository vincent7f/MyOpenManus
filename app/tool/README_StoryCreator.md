# StoryCreator Tool

StoryCreator是一个用于生成创意故事的工具类，它利用AI语言模型根据用户提供的提示和参数生成故事内容。

## 功能特点

- 根据用户提供的提示生成原创故事
- 支持指定故事的体裁（如奇幻、科幻、恐怖等）
- 可以控制故事的长度（短、中、长）
- 可以指定写作风格（如描述性、简洁、诗意等）
- 可以指定故事中的主要角色

## 使用方法

### 直接使用StoryCreator类

```python
from app.llm import get_llm
from app.tool import StoryCreator

async def generate_story():
    # 获取语言模型
    llm = get_llm()
    
    # 创建StoryCreator实例
    story_creator = StoryCreator(llm=llm)
    
    # 生成故事
    story = await story_creator.execute(
        prompt="一个探险家在丛林中发现了一座古老的神庙",
        genre="冒险",
        length="medium",
        style="描述性",
        characters="勇敢的探险家Alex，聪明的考古学家Maya，神秘的当地向导"
    )
    
    print(story)
```

### 通过ToolCallAgent使用

```python
from app.agent.toolcall import ToolCallAgent
from app.llm import get_llm
from app.tool import StoryCreator, ToolCollection

async def generate_story_with_agent():
    # 获取语言模型
    llm = get_llm()
    
    # 创建StoryCreator实例
    story_creator = StoryCreator(llm=llm)
    
    # 创建ToolCallAgent，将StoryCreator作为可用工具
    agent = ToolCallAgent(
        llm=llm,
        available_tools=ToolCollection(story_creator),
        system_prompt=(
            "你是一个创意故事生成助手，可以根据用户的提示创作故事。"
            "使用story_creator工具来生成创意故事。"
        )
    )
    
    # 初始化agent
    agent.init_memory()
    
    # 添加用户消息
    user_prompt = "创作一个关于太空探索的科幻故事，包含一位宇航员和一个AI助手"
    agent.memory.add_message(agent.create_user_message(user_prompt))
    
    # 运行agent
    await agent.run()
```

## 参数说明

StoryCreator.execute()方法接受以下参数：

- `prompt` (必需): 故事的主要提示或创意
- `genre` (可选): 故事的体裁（如奇幻、科幻、爱情、恐怖等）
- `length` (可选): 故事的长度，可选值为"short"、"medium"、"long"，默认为"medium"
- `style` (可选): 故事的写作风格（如描述性、简洁、诗意等）
- `characters` (可选): 故事中主要角色的描述

## 示例

查看`examples/story_creator_example.py`文件，了解完整的使用示例。

## 注意事项

- StoryCreator需要一个语言模型实例才能工作，请确保在创建StoryCreator实例时提供llm参数
- 生成故事可能需要一些时间，特别是对于较长的故事
- 生成的故事内容取决于AI模型的能力和训练数据 