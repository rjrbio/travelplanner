class RAGAgent:

    def run(self, state):
        query = state.get("user_query") or state.get("destination_city")
        if not query:
            return {**state, "rag_data": {}}

        try:
            from rag.rag_query import RAGQuery

            chunks = RAGQuery().search(query)

            rag_data = {
                "weather": None,
                "transport": None,
                "events": [],
                "neighborhoods": [],
                "tips": [],
            }

            for c in chunks:
                text = c.get("content", "").lower()

                if "clima" in text or "temperatura" in text:
                    rag_data["weather"] = c["content"]
                if "transporte" in text or "metro" in text or "bus" in text:
                    rag_data["transport"] = c["content"]
                if "evento" in text or "festival" in text:
                    rag_data["events"].append(c["content"])
                if "barrio" in text or "zona" in text:
                    rag_data["neighborhoods"].append(c["content"])
                if "tip" in text or "consejo" in text:
                    rag_data["tips"].append(c["content"])

            return {**state, "rag_data": rag_data}
        except Exception:
            return {**state, "rag_data": {}}


rag_agent = RAGAgent().run
