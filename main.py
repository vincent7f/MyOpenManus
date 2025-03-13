import asyncio

from app.agent.mymanus import MyManus
from app.logger import logger
from app.config import config

def log_config_info():
    """记录配置信息到日志"""
    default_settings = config.llm.get("default")
    
    logger.info("Configuration loaded successfully")
    logger.info(f"Default LLM model: {default_settings.model}")
    logger.info(f"Default LLM base URL: {default_settings.base_url}")
    logger.info(f"Default LLM max tokens: {default_settings.max_tokens}")
    logger.info(f"Default LLM temperature: {default_settings.temperature}")
    logger.info(f"Default LLM API type: {default_settings.api_type}")
    
    # 记录LLM覆盖配置
    llm_overrides = {k: v for k, v in config.llm.items() if k != "default"}
    if llm_overrides:
        logger.info(f"LLM overrides found for: {', '.join(llm_overrides.keys())}")
        for name, override in llm_overrides.items():
            logger.info(f"  - {name} override: {override}")
    
    # 记录工具配置
    tool_list = config.tools.tool_list
    if tool_list:
        logger.info(f"Enabled tools: {', '.join(tool_list)}")
    else:
        logger.info("No tools enabled")

async def main():
    # 记录配置信息
    log_config_info()
    
    agent = MyManus()
    while True:
        try:
            prompt = input("Enter your prompt (or 'exit'/'quit' to quit): ")
            
            prompt_lower = prompt.lower()
            if prompt_lower in ["exit", "quit"]:
                logger.info("Goodbye!")
                break
            if not prompt.strip():
                logger.warning("Skipping empty prompt.")
                continue
            logger.info(f"Received prompt: {prompt}")
            logger.warning("Processing your request...")
            await agent.run(prompt)
        except KeyboardInterrupt:
            logger.warning("Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())
