import os
import re

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


class ItineraryAgent:

    def __init__(self):
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = ChatOllama(
                model="qwen3:1.7b", temperature=0.7, num_predict=2048,
                base_url=OLLAMA_URL, client_kwargs={"timeout": 300},
            )
        return self._llm

    def build_itinerary(
        self,
        destination: str,
        days: int,
        planner_summary: str = "",
        attractions: list | None = None,
        rag_data: dict | None = None,
    ) -> dict:
        print(f"Generando itinerario de {days} días para {destination}...")

        attractions_text = "\n".join(
            f"- {a.get('name', a.get('nombre', str(a)))}"
            for a in (attractions or [])
        ) or "No hay atracciones disponibles."

        rag = rag_data or {}
        rag_context = (
            f"Clima: {rag.get('weather', 'No disponible')}\n"
            f"Transporte: {rag.get('transport', 'No disponible')}\n"
            f"Tips: {'; '.join(rag.get('tips', [])[:3]) or 'No disponible'}\n"
            f"Eventos: {'; '.join(rag.get('events', [])[:3]) or 'No disponible'}\n"
            f"Barrios: {'; '.join(rag.get('neighborhoods', [])[:3]) or 'No disponible'}"
        )

        with open("prompts/itinerary.txt", "r", encoding="utf-8") as f:
            prompt_text = f.read()

        prompt_template = ChatPromptTemplate.from_template(prompt_text)
        chain = prompt_template | self.llm

        response = chain.invoke({
            "destination": destination,
            "days": days,
            "planner_summary": planner_summary or "No disponible.",
            "attractions_text": attractions_text,
            "rag_context": rag_context,
        })

        raw = response.content.strip()
        print("--- Itinerario generado ---")
        print(raw[:500])
        print("---------------------------")

        parsed_days = self._parse_days(raw, destination, days, attractions or [])

        return {
            "destination": destination,
            "days": days,
            "itinerary": parsed_days,
        }

    def _parse_days(self, raw: str, destination: str, days: int, attractions: list) -> list:
        sections = re.split(r'(?:^|\n)DÍA\s*(\d+)\s*:', raw, flags=re.IGNORECASE | re.MULTILINE)
        result = []

        if len(sections) > 1:
            blocks = []
            current = None
            for part in sections[1:]:
                part = part.strip()
                if part.isdigit():
                    if current:
                        blocks.append(current)
                    current = {"num": int(part), "text": ""}
                elif current is not None:
                    current["text"] = part
            if current:
                blocks.append(current)

            for b in blocks:
                lines = b["text"].split("\n")
                title = ""
                description_lines = []
                activities = []

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    lower = line.lower()
                    if lower.startswith("actividades:"):
                        raw_acts = line[len("actividades:"):].strip()
                        raw_acts = raw_acts.replace("[", "").replace("]", "")
                        activities = [a.strip().strip("-").strip() for a in raw_acts.split("|") if a.strip()]
                        if not activities:
                            activities = [a.strip().strip("-").strip() for a in raw_acts.split(",") if a.strip()]
                    elif not title:
                        title = line
                    else:
                        description_lines.append(line)

                description = " ".join(description_lines) if description_lines else ""

                title = title.replace("**", "").replace("*", "")
                cleaned_activities = []
                for a in activities:
                    a = a.replace("**", "").replace("*", "").strip()
                    if a:
                        cleaned_activities.append(a)

                if not cleaned_activities and attractions:
                    start_idx = (b["num"] - 1) * min(3, len(attractions))
                    cleaned_activities = [
                        a.get("name", a.get("nombre", str(a)))
                        for a in attractions[start_idx:start_idx + 3]
                    ]

                result.append({
                    "title": title or f"Día {b['num']} en {destination}",
                    "description": description or f"Exploración del día {b['num']} en {destination}",
                    "suggested_activities": cleaned_activities,
                })
        else:
            for i in range(days):
                acts = [
                    a.get("name", a.get("nombre", str(a)))
                    for a in attractions[i * 3:(i + 1) * 3]
                ] if attractions else []
                result.append({
                    "title": f"Día {i + 1} en {destination}",
                    "description": f"Exploración del día {i + 1} en {destination}",
                    "suggested_activities": acts,
                })

        while len(result) < days:
            result.append({
                "title": f"Día {len(result) + 1} en {destination}",
                "description": f"Exploración del día {len(result) + 1} en {destination}",
                "suggested_activities": [],
            })

        return result[:days]
