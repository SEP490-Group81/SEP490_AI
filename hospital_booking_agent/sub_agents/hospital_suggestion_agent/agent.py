import os
from google.adk.agents import Agent
from hospital_booking_agent.sub_agents.hospital_suggestion_agent import prompt
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from hospital_booking_agent.shared_libraries.types import SymtomInputSchema
from hospital_booking_agent.shared_libraries.types import json_response_config

get_symptoms_agent = VertexAiRagRetrieval(
    name="get_symptoms_rag_document",
    description="Use this tool to retrieve documentation and reference materials for the question from the RAG corpus",
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("RAG_CORPUS")
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

symtom_advisor_agent = Agent(
    model="gemini-2.0-flash-001",
    name="symtom_advisor_agent",
    description="This agent that suggests conditions of user based on user input",
    instruction=prompt.CONDITION_SUGGESTION_AGENT_INSTR,
    output_key="possible_conditions",
    tools=[get_symptoms_agent]
)

location_suggestion_agent = Agent(
    model="gemini-2.0-flash-001",
    name="location_suggestion_agent",
    description="A sub-agent that suggests locations based on user input",
    instruction=prompt.LOCATION_SUGGESTION_AGENT_INSTR,
    before_agent_callback=None
)

hosptal_suggestion_agent = Agent(
    model="gemini-2.0-flash-001",
    name="hospital_suggestion_agent",
    description="A sub-agent that suggests hospitals based on user input",
    instruction=prompt.HOSPITAL_SUGGESTION_AGENT_INSTR,
    tools=[
        AgentTool(agent=location_suggestion_agent),
        AgentTool(agent=symtom_advisor_agent)
    ],
    before_agent_callback=None
)
