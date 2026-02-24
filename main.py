import os
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver

# API key de Groq
os.environ["GROQ_API_KEY"] = "La API KEY (git no deja subir la API :3)"

# Prompt
SYSTEM_PROMPT = """You are an expert weather forecaster who speaks in puns.
You have access to two tools:
- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location
If a user asks for the weather, make sure you know the location."""

@dataclass
class Context:
    user_id: str

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user location based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "New York"


model = init_chat_model(
    "llama-3.3-70b-versatile",
    model_provider="groq",
    temperature=0.5,
    max_tokens=1000
)

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather outside?"}]},
    config=config,
    context=Context(user_id="1")
)
print("Respuesta 1:")
last_message = response["messages"][-1]
print(last_message.content)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Thank you!"}]},
    config=config,
    context=Context(user_id="1")
)
print("\nRespuesta 2:")
last_message = response["messages"][-1]
print(last_message.content)
