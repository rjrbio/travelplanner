from agents.planner_agent import PlannerAgent
from agents.search_agent import SearchAgent
from agents.itinerary_agent import ItineraryAgent
from tests.conftest import pytestmark_agentes


pytestmark = pytestmark_agentes


def test_planner_agent():
    agent = PlannerAgent()
    result = agent.plan_trip("Lima", 3)
    assert result["destination"] == "Lima"
    assert result["duration_days"] == 3


def test_search_agent():
    agent = SearchAgent()
    result = agent.search_options("playa")
    assert isinstance(result, list)
    assert len(result) > 0


def test_itinerary_agent():
    agent = ItineraryAgent()
    result = agent.build_itinerary("Roma", 2)
    assert len(result["itinerary"]) == 2
