# spatialbound/location_analyser.py
import logging

logger = logging.getLogger(__name__)

class LocationAnalyser:
    def __init__(self, api_handler):
        self.api_handler = api_handler
        
    def analyse_location(self, location_type, address=None, postcode=None, location=None,
                         transaction_type=None, business_type=None, radius=500):
        """
        Analyses the location based on the provided parameters.
        
        Args:
            location_type (str): The type of the location (e.g., "residential", "commercial").
            address (str, optional): The address of the location.
            postcode (str, optional): The postcode of the location.
            location (dict, optional): The latitude and longitude of the location.
            transaction_type (str, optional): The transaction type (e.g., "buy", "rent").
            business_type (str, optional): The business type for commercial locations.
            radius (int, optional): Radius in meters for analysis (default is 500).
            
        Returns:
            dict: Location analysis details.
        """
        endpoint = "/api/analyse-location"
        
        # Looking at the router, we need to format the request correctly
        location_data = {
            "locationType": location_type,
            "transactionType": transaction_type,
            "businessType": business_type,
            "address": address,
            "postcode": postcode,
            "radius": radius
        }
        
        # If location is provided, format it according to what the API expects
        if location:
            # The API expects a LocationCoordinates object with lat/lng properties
            if isinstance(location, dict) and 'lat' in location and 'lng' in location:
                location_data["location"] = location
            elif isinstance(location, (list, tuple)) and len(location) == 2:
                location_data["location"] = {"lat": location[0], "lng": location[1]}
        
        try:
            return self.api_handler.make_authorised_request(endpoint, method='POST', json=location_data)
        except Exception as e:
            logger.error(f"Error analyzing location: {e}")
            return {"error": str(e)}