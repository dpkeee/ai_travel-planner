from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.agents.travel_agent import agent
from src.utils.logger import get_logger
from src.utils.custom_exception import CustomException
from pydantic import BaseModel

logger = get_logger(__name__)


class ItineraryInput(BaseModel):
    city: str
    days: int
    interests: list[str]
    style: str
    pace: str
    month: str | None = None


class TravelPlanner:
    def __init__(self):
        self.messages = []
        logger.info("TravelPlanner initialized")

    def create_itinerary(self, user_input: ItineraryInput):
        try:
            # SYSTEM PROMPT (rules only)
            system_prompt = """
You are a travel planning assistant.

REQUIRED FIELDS:
- city
- days
- interests
- travel style
- pace

RULES:
1. If ANY required fields are missing or unclear, ask ONE follow-up question.
2. Do NOT generate an itinerary until all fields are collected.
3. Once all fields are present, generate a detailed itinerary.
4. Maintain conversation context.
"""

            # Add system message only once
            if not self.messages:
                self.messages.append(SystemMessage(content=system_prompt))

            # Build the USER prompt from the Pydantic model
            user_prompt = f"""
Plan a {user_input.days}-day trip to {user_input.city}.

Interests: {', '.join(user_input.interests)}
Style: {user_input.style}
Pace: {user_input.pace}
Month: {user_input.month or 'Any'}
"""

            # Add user message
            self.messages.append(HumanMessage(content=user_prompt))

            # Invoke agent
            response = agent.invoke({"messages": self.messages})
            ai_msg = response["messages"][-1].content

            # Save AI response
            self.messages.append(AIMessage(content=ai_msg))

            return ai_msg

        except Exception as e:
            logger.error(f"Planner error: {e}")
            raise CustomException("Failed to generate itinerary", e)