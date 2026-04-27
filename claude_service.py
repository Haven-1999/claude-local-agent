import asyncio
import os
import sys
import re
import time
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

# 加载环境变量
load_dotenv()

class ClaudeAgentService:
    def __init__(self):
        self.model = os.getenv("MODEL_NAME")
        self.last_activity_time = time.time()

    def parse_command(self, raw_input: str):
        """解析命令行输入：分离主任务描述和 /skill- 技能调用"""
        skill_pattern = r"/skill-(\w+)"
        skills = re.findall(skill_pattern, raw_input)
        main_task = re.sub(skill_pattern, "", raw_input).strip()
        return main_task, skills

    async def heartbeat(self):
        """心跳提示：防止用户以为程序卡死"""
        while True:
            await asyncio.sleep(2)
            if time.time() - self.last_activity_time > 1.5:
                print("⏳  正在处理中...", end="\r")
            else:
                print(" " * 20, end="\r")

    async def execute_task(self, prompt: str, custom_skills: list = None):
        print(f"[Agent] 主任务：{prompt}")
        if custom_skills:
            print(f"[Agent] 调用技能：{', '.join(custom_skills)}")
        print("🔗 正在连接 Claude 服务...\n")
        
        # 基础工具 + 动态添加用户指定的技能
        base_tools = ["Read", "Glob", "Bash", "Skill"]
        allowed_tools = base_tools + (custom_skills if custom_skills else [])
        
        # 原生技能加载：直接指定 superpowers 文件夹路径
        options = ClaudeAgentOptions(
            model=self.model,
            allowed_tools=allowed_tools,
            permission_mode="acceptEdits",
            skills=["./superpowers"]  # 打包后会在同一目录
        )

        # 记录开始时间
        start_time = time.time()
        self.last_activity_time = time.time()

        # 启动心跳任务
        heartbeat_task = asyncio.create_task(self.heartbeat())

        try:
            # 流式执行任务
            async for message in query(prompt=prompt, options=options):
                self.last_activity_time = time.time()
                
                # 1. 输出AI思考过程
                if hasattr(message, "thought") and message.thought:
                    print(f"💡 [思考] {message.thought}")
                
                # 2. 输出工具调用信息
                if hasattr(message, "tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:
                        print(f"🔧 [调用工具] {tool_call.name}")
                
                # 3. 输出工具执行结果
                if hasattr(message, "tool_results") and message.tool_results:
                    for tool_result in message.tool_results:
                        print(f"✅ [工具执行完成] {tool_result.name}")
                
                # 4. 输出最终执行结果
                if hasattr(message, "result") and message.result:
                    print("\n" + "="*50)
                    print("📝 最终执行结果：")
                    print("="*50)
                    print(message.result)

        finally:
            # 停止心跳任务
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass

        # 计算耗时
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 输出统计信息
        self._print_stats(elapsed_time)

    def _print_stats(self, elapsed_time: float):
        """打印耗时统计"""
        print("\n" + "="*50)
        print("📊 本次执行统计")
        print("="*50)
        print(f"⏱️  耗时：{elapsed_time:.2f} 秒")
        print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方式：./claude_service \"你的任务描述 /skill-技能名\"")
        print("示例：./claude_service \"帮我头脑风暴一个项目 /skill-brainstorming\"")
        sys.exit(1)

    raw_input = sys.argv[1]
    agent = ClaudeAgentService()
    main_task, skills = agent.parse_command(raw_input)
    
    # 自动转换技能名为 superpowers:xxx 格式
    if skills:
        skills = [f"superpowers:{skill}" for skill in skills]
    
    asyncio.run(agent.execute_task(main_task, skills))
