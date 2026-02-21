from langchain_community.utilities import GoogleSerperAPIWrapper
from src.config.config import SERPER_API_KEY
from src.utils.logger import get_logger

logger = get_logger(__name__)

def google_serper_search_tool(query: str) -> str:
    """
    Search Google via Serper API to fetch recent and reliable
    real-world travel information for the given query.
    """
    search = GoogleSerperAPIWrapper(
        serper_api_key=SERPER_API_KEY
    )
    return search.run(query)

if __name__ == "__main__":
    print("Testing serper  Search Tool...")
    result = google_serper_search_tool("best travel destinations in Japan")
    print("Result:")
    print(result)

 
logger.info("SERPER TOOL ALL SET")