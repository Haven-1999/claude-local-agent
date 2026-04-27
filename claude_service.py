import asyncio
import os
import sys
import re
import time
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

# Load environment variables
load_dotenv()

class ClaudeAgentService:
    def __init__(self):
        self.model = os.getenv("MODEL_NAME")
        self.last_activity_time = time.time()
        self.skills_dir = "./skills"
        self.loaded_skills = self._load_skills()

    def _load_skills(self):
        """🔥 Auto-scan and load all skills from the skills/ directory"""
        skill_paths = []
        if not os.path.exists(self.skills_dir):
            print(f"[Warning] Skills directory '{self.skills_dir}' not found. Creating it...")
            os.makedirs(self.skills_dir)
            return skill_paths

        # Iterate all subdirectories in skills/
        for item in os.listdir(self.skills_dir):
            item_path = os.path.join(self.skills_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                skill_paths.append(item_path)
                print(f"[Agent] Auto-loaded skill: {item}")
        
        return skill_paths

    def parse_command(self, raw_input: str):
        """Parse command input: split task and /skill- calls"""
        skill_pattern = r"/skill-(\w+)"
        skills = re.findall(skill_pattern, raw_input)
        main_task = re.sub(skill_pattern, "", raw_input).strip()
        return main_task, skills

    async def heartbeat(self):
        """Heartbeat tip for long-running tasks"""
        while True:
            await asyncio.sleep(2)
            if time.time() - self.last_activity_time > 1.5:
                print("⏳  Processing...", end="\r")
            else:
                print(" " * 20, end="\r")

    async def execute_task(self, prompt: str, custom_skills: list = None):
        print(f"[Agent] Task: {prompt}")
        if custom_skills:
            print(f"[Agent] Requested Skills: {', '.join(custom_skills)}")
        print("🔗 Connecting to Claude Service...\n")
        
        # Base tools
        base_tools = ["Read", "Glob", "Bash", "Skill"]
        allowed_tools = base_tools + (custom_skills if custom_skills else [])
        
        # 🔥 Use auto-loaded skills from skills/ directory
        options = ClaudeAgentOptions(
            model=self.model,
            allowed_tools=allowed_tools,
            permission_mode="acceptEdits",
            skills=self.loaded_skills
        )

        start_time = time.time()
        self.last_activity_time = time.time()
        heartbeat_task = asyncio.create_task(self.heartbeat())

        try:
            async for message in query(prompt=prompt, options=options):
                self.last_activity_time = time.time()
                
                if hasattr(message, "thought") and message.thought:
                    print(f"💡 [Thinking] {message.thought}")
                if hasattr(message, "tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:
                        print(f"🔧 [Using Tool] {tool_call.name}")
                if hasattr(message, "tool_results") and message.tool_results:
                    for tool_result in message.tool_results:
                        print(f"✅ [Tool Completed] {tool_result.name}")
                if hasattr(message, "result") and message.result:
                    print("\n" + "="*50)
                    print("📝 Final Result:")
                    print("="*50)
                    print(message.result)

        finally:
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass

        elapsed_time = time.time() - start_time
        self._print_stats(elapsed_time)

    def _print_stats(self, elapsed_time: float):
        print("\n" + "="*50)
        print("📊 Execution Stats")
        print("="*50)
        print(f"⏱️  Time Elapsed: {elapsed_time:.2f}s")
        print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./claude_service \"your task /skill-skillname\"")
        print("Example: ./claude_service \"Brainstorm a project /skill-brainstorming\"")
        sys.exit(1)

    raw_input = sys.argv[1]
    agent = ClaudeAgentService()
    main_task, skills = agent.parse_command(raw_input)
    
    # Auto-prefix skill calls (supports any skill in skills/ directory)
    if skills:
        # Try to infer skill namespace from directory name (simplified)
        # For superpowers, it's still superpowers:xxx
        prefixed_skills = []
        for skill in skills:
            # Simple heuristic: if superpowers is loaded, prefix with superpowers:
            # This can be extended for multi-skill setups
            prefixed_skills.append(f"superpowers:{skill}")
        skills = prefixed_skills
    
    asyncio.run(agent.execute_task(main_task, skills))
