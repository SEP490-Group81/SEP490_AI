import time
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
import hospital_booking_agent.sub_agents.plan_agent.prompt as prompt
import hospital_booking_agent.sub_agents.plan_agent.tools as tools
from hospital_booking_agent.tools.hospitals import hos_select_tool
from hospital_booking_agent.tools.memory import memorize

def create_agent_with_retry(model_name, name, description, instruction, output_key, tools_list, max_retries=5, initial_delay=1):
    """
    Tạo một Agent với cơ chế thử lại bằng backoff lũy thừa.
    """
    retries = 0
    delay = initial_delay
    while retries < max_retries:
        try:
            return Agent(
                model=model_name, 
                name=name,
                description=description,
                instruction=instruction,
                output_key=output_key,
                tools=tools_list
            )
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e):
                print(f"Lỗi: {e}. Đang thử lại sau {delay} giây (lần thử {retries + 1}/{max_retries})...")
                time.sleep(delay)
                delay *= 2  # Tăng gấp đôi thời gian chờ
                retries += 1
            else:
                raise e # Lỗi khác không phải do cạn kiệt tài nguyên
    raise Exception(f"Không thể tạo Agent sau {max_retries} lần thử do lỗi RESOURCE_EXHAUSTED.")


plan_agent = create_agent_with_retry(
    model_name="gemini-2.0-flash-001", 
    name="plan_agent",
    description="A sub-agent that plans the hospital appoinment base on user input",
    instruction=prompt.PLAN_AGENT_INSTR,
    output_key="appointment_plan",
    tools_list=[
        hos_select_tool,
        memorize,
        AgentTool(agent=tools.hospital_services_agent),
        AgentTool(agent=tools.specialization_tool),
        AgentTool(agent=tools.doctor_tool),
        AgentTool(agent=tools.timeline_tool)
    ]
)