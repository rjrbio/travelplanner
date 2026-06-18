
def get_tours(destination: str) -> list[dict]:
    return [{"provider": "GetYourGuide", "destination": destination, "duration": "3h"}]
