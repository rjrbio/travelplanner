from dotenv import load_dotenv
load_dotenv()

from services.locations.location_service import LocationService


def test_location_api():
    result = LocationService.get_location("malaga teatinos")

    assert result is not None
    assert "lat" in result
    assert "lng" in result
    assert "name" in result

    print("Resultado:", result)


if __name__ == "__main__":
    test_location_api()
