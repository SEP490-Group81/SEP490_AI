from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

plan_agent = Agent(
    model="gemini-2.0-flash-001",
    name="hospital_suggestion_agent",
    description="A sub-agent that suggests hospitals based on user input",
    before_agent_callback=None
)