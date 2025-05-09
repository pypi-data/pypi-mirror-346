# spatialbound/weather_handler.py
import logging
import pandas as pd
import requests

logger = logging.getLogger(__name__)

class WeatherHandler:
    """
    Handler for weather and air quality data.
    """
    def __init__(self, api_handler):
        """
        Initialize the weather handler with the API handler.
        
        Args:
            api_handler: The API handler for making authorized requests.
        """
        self.api_handler = api_handler
    
    def get_weather(self, lat, lon):
        """
        Get current weather and air quality data for a specific location.
        
        Args:
            lat (float): Latitude of the location
            lon (float): Longitude of the location
            
        Returns:
            dict: Weather and air quality data for the specified location
        """
        # Construct the endpoint with query parameters
        endpoint = f"/api/weather?lat={lat}&lon={lon}"
        
        try:
            # Call the API handler with the existing method parameters it accepts
            response = self.api_handler.make_authorised_request(endpoint, method='GET')
            return response
        except Exception as e:
            logger.error(f"Failed to get weather data: {e}")
            return {'error': str(e)}
    
    def get_air_quality(self, lat, lon):
        """
        Get current air quality data for a specific location.
        This is a convenience method that extracts just the air quality data
        from the weather response.
        
        Args:
            lat (float): Latitude of the location
            lon (float): Longitude of the location
            
        Returns:
            dict: Air quality data for the specified location
        """
        weather_data = self.get_weather(lat, lon)
        
        if 'error' in weather_data:
            return weather_data
            
        # Extract just the air quality fields
        air_quality_fields = ['co', 'o3', 'no2', 'so2', 'pm2_5', 'pm10', 'us_epa_index']
        air_quality_data = {field: weather_data.get(field) for field in air_quality_fields if field in weather_data}
        
        # Add location information
        air_quality_data['lat'] = weather_data.get('lat')
        air_quality_data['lon'] = weather_data.get('lon')
        air_quality_data['location_name'] = weather_data.get('name')
        
        return air_quality_data