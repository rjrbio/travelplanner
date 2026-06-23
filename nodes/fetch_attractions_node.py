from services.attractions.attractions_fetcher import AttractionsFetcher

def fetch_attractions_node(state):
    """
    Node del grafo:
    - Recibe la ciudad desde el PlannerAgent
    - Llama a AttractionsFetcher
    - Devuelve top N atracciones
    """

    city = state.get("destination_city")
    limit = state.get("attractions_limit", 5)
    currency = state.get("currency", "EUR")
    language = state.get("language", "en-us")

    attractions = AttractionsFetcher.get_attractions_for_city(
        city=city,
        limit=limit,
        currency=currency,
        language=language
    )

    return {
        **state,
        "attractions": attractions
    }
