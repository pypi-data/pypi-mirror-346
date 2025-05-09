from .config import ALLOWED_OPTIMISATION_TYPES, ALLOWED_MODES_OF_TRAVEL
import logging

logger = logging.getLogger(__name__)

class RouteCalculator:
    def __init__(self, api_handler):
        self.api_handler = api_handler

    def navigate(self, route_type: str, origin, destinations: list, optimisation_type="shortest_path", mode_of_travel="walk"):
        endpoint = "/api/route_calculator"

        if route_type == "address" or route_type == "postcode":
            data = {
                "origin": origin,
                "destinations": destinations
            }
        elif route_type == "points":
            data = {
                "points": [origin] + destinations
            }
        else:
            return {"error": f"Invalid route_type provided: {route_type}"}

        route_payload = {
            "type": route_type,
            "data": data,
            "optimisationType": optimisation_type,
            "modeOfTravel": mode_of_travel
        }

        try:
            response = self.api_handler.make_authorised_request(endpoint, method='POST', json=route_payload)
            return response
        except Exception as e:
            logger.error(f"Failed to calculate route: {e}")
            return {'error': str(e)}