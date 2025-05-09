from spatialbound.api_handler import APIHandler
from spatialbound.route_calculator import RouteCalculator
from spatialbound.location_analyser import LocationAnalyser
from spatialbound.video_analyser import VideoAnalyser
from spatialbound.geocode_functions import GeocodeFunctions
from spatialbound.poi_handler import POIHandler
from spatialbound.chat_handler import ChatHandler
from spatialbound.map_generator import MapGenerator
from spatialbound.weather_handler import WeatherHandler
from spatialbound.version import __version__
import logging

logger = logging.getLogger(__name__)

class Spatialbound:
    """
    Spatialbound class that serves as an API client to access various functionalities such as route calculation,
    location analysis, video analysis, geocoding functions, POI retrieval, LLM chat, map generation,
    and weather data.

    Attributes:
        api_handler (APIHandler): The API handler for making authorised requests.
        login_response (dict): The response received after logging in with the API key.
        route_calculator (RouteCalculator): An instance of the RouteCalculator class.
        location_analyser (LocationAnalyser): An instance of the LocationAnalyser class.
        video_analyser (VideoAnalyser): An instance of the VideoAnalyser class.
        geocode_functions (GeocodeFunctions): An instance of the GeocodeFunctions class.
        poi_handler (POIHandler): An instance of the POIHandler class.
        chat_handler (ChatHandler): An instance of the ChatHandler class.
        map_generator (MapGenerator): An instance of the MapGenerator class.
        weather_handler (WeatherHandler): An instance of the WeatherHandler class.
    """
    # Add version as a class attribute
    __version__ = __version__
    
    def __init__(self, api_key):
        """
        Initializes the Spatialbound class with the provided API key and sets up the necessary instances.

        Args:
            api_key (str): The API key to authenticate requests.
        """
        self.api_handler = APIHandler(api_key)
        self.login_response = self.api_handler.login_response
        
        # Add version to login response
        if isinstance(self.login_response, dict):
            self.login_response["client_version"] = self.__class__.__version__
            
        self.route_calculator = RouteCalculator(self.api_handler)
        self.location_analyser = LocationAnalyser(self.api_handler)
        self.video_analyser = VideoAnalyser(self.api_handler)
        self.geocode_functions = GeocodeFunctions(self.api_handler)
        self.poi_handler = POIHandler(self.api_handler)
        self.chat_handler = ChatHandler(self.api_handler)
        self.map_generator = MapGenerator(self.api_handler)
        self.weather_handler = WeatherHandler(self.api_handler)
        
        # Try to get server version
        self.server_version = self._get_server_version()

    def _get_server_version(self):
        """
        Get the version of the server API
        
        Returns:
            str: The server version or None
        """
        try:
            response = self.api_handler.make_authorised_request("/api/version", method='GET')
            
            if response and isinstance(response, dict) and 'version' in response:
                server_version = response['version']
                logger.info(f"Server API version: {server_version}")
                
                # Add to login response
                if isinstance(self.login_response, dict):
                    self.login_response["server_version"] = server_version
                    
                return server_version
            return None
        except Exception as e:
            logger.warning(f"Failed to get server version: {e}")
            return None

    def get_version(self):
        """
        Get version information for the client and server.
        
        Returns:
            dict: Dictionary containing version information
        """
        version_info = {
            "client_version": self.__class__.__version__,
        }
        
        if hasattr(self, 'server_version') and self.server_version:
            version_info["server_version"] = self.server_version
            
        return version_info

    def get_weather(self, lat, lon):
        """
        Get current weather and air quality data for a specific location.
        
        Args:
            lat (float): Latitude of the location
            lon (float): Longitude of the location
            
        Returns:
            dict: Weather and air quality data for the specified location
        """
        return self.weather_handler.get_weather(lat, lon)
    
    def get_air_quality(self, lat, lon):
        """
        Get current air quality data for a specific location.
        
        Args:
            lat (float): Latitude of the location
            lon (float): Longitude of the location
            
        Returns:
            dict: Air quality data for the specified location
        """
        return self.weather_handler.get_air_quality(lat, lon)
    

    def navigate(self, route_type: str, origin, destinations: list, optimisation_type="shortest_path", mode_of_travel="walk"):
        """
        Calculates the route based on the provided parameters.

        Args:
            route_type (str): The type of the route (e.g., "address", "postcode", or "points").
            origin (str or list): The origin of the route.
            destinations (list): The list of destinations for the route.
            optimisation_type (str, optional): The optimisation type for the route calculation (default is "shortest_path").
            mode_of_travel (str, optional): The mode of travel for the route (default is "walk").

        Returns:
            dict: The calculated route details.
        """
        return self.route_calculator.navigate(route_type, origin, destinations, optimisation_type, mode_of_travel)

    def analyse_location(self, location_type, address=None, postcode=None, location=None, transaction_type=None, business_type=None, radius=300):
  
        """
        Analyses the location based on the provided parameters.

        Args:
            location_type (str): The type of the location (e.g., "residential", "commercial").
            address (str, optional): The address of the location.
            postcode (str, optional): The postcode of the location.
            location (dict, optional): The latitude and longitude of the location as a dict with 'lat' and 'lng' keys.
            transaction_type (str, optional): The transaction type (e.g., "buy", "rent").
            business_type (str, optional): The business type for commercial locations.
            radius (int, optional): Radius in meters for analysis (default is 500).

        Returns:
            dict: The location analysis details.
        """
        
        return self.location_analyser.analyse_location(
            location_type, address, postcode, location, transaction_type, business_type, radius
        )     

    def upload_video(self, file_path):
        """
        Upload a video file for analysis.

        Args:
            file_path (str): Path to the video file on the local system.

        Returns:
            dict: Response containing the uploaded video URL.
        """
        return self.video_analyser.upload_video(file_path)

    def analyse_video(self, video_url, user_prompt, fps):
        """
        Analyses the video based on the provided parameters.

        Args:
            video_url (str): The URL of the previously uploaded video to be analysed.
            user_prompt (str): The prompt for AI analysis.
            fps (int): The frames per second for video processing.

        Returns:
            dict: The video analysis details.
        """
        return self.video_analyser.analyse_video(video_url, user_prompt, fps)

    def search_video(self, query, video_url, limit=10, search_mode="semantic"):
        """
        Search for specific content within a video based on natural language queries.
        
        Args:
            query (str): Search query to find video moments.
            video_url (str): URL of the video to search.
            limit (int, optional): Maximum number of results to return (default 10).
            search_mode (str, optional): Search mode, "semantic" or "exact" (default "semantic").
            
        Returns:
            dict: Search results matching the query.
        """
        return self.video_analyser.search_video(query, video_url, limit, search_mode)

    def find_similarities(self, video_url, timestamp, limit=10, threshold=0.7):
        """
        Find moments in videos that are similar to a specific timestamp in a source video.
        
        Args:
            video_url (str): URL of the video to compare against database.
            timestamp (float): Timestamp in seconds to find similar moments.
            limit (int, optional): Maximum number of results to return (default 10).
            threshold (float, optional): Similarity threshold from 0.0 to 1.0 (default 0.7).
            
        Returns:
            dict: Similar moments found across videos.
        """
        return self.video_analyser.find_similarities(video_url, timestamp, limit, threshold)
    
    def find_image_in_video(self, image_path, video_url, threshold=0.7):
        """
        Find an uploaded image within frames of a video.
        
        Args:
            image_path (str): Path to the image file on the local system.
            video_url (str): URL of the video to search within.
            threshold (float, optional): Minimum similarity threshold (default 0.7).
            
        Returns:
            dict: Found timestamps and frames with similarity scores.
        """
        return self.video_analyser.find_image_in_video(image_path, video_url, threshold)
    
    def analyze_video_location(self, video_url, fps=2):
        """
        Analyze a video to determine its geographical location.
        
        Args:
            video_url (str): URL of the video to analyze.
            fps (int, optional): Frames per second to extract (default 2).
            
        Returns:
            dict: Geolocation analysis results.
        """
        return self.video_analyser.analyze_video_location(video_url, fps)

    def create_map(self, map_id, layers, grid_or_vector="grid", boundary_type="bbox", boundary_details=None, 
                  grid_type="h3", resolution="auto", operation="visualisation", layer_group=None):
        """
        Creates a map based on the provided parameters.

        Args:
            map_id (str): Unique identifier for the map.
            layers (list): List of layer names to include in the map.
            grid_or_vector (str, optional): Type of map, either "grid" or "vector" (default is "grid").
            boundary_type (str, optional): Type of boundary (address, postcode, latlon, bbox, etc.) (default is "bbox").
            boundary_details (str, optional): Details of the boundary in format appropriate for boundary_type.
            grid_type (str, optional): Type of grid, if grid_or_vector is "grid" (default is "h3").
            resolution (str or int, optional): Resolution of the grid (default is "auto").
            operation (str, optional): Operation to perform (default is "visualisation").
            layer_group (str, optional): Name of a predefined layer group, if using vector map.

        Returns:
            dict: The created map data.
        """
        return self.map_generator.create_map(
            map_id, layers, grid_or_vector, boundary_type, boundary_details,
            grid_type, resolution, operation, layer_group
        )

    def get_vector_layer_names(self):
        """
        Retrieves all available vector layer names.

        Returns:
            dict: Available vector layer names.
        """
        return self.map_generator.get_vector_layer_names()

    def get_grid_layer_names(self):
        """
        Retrieves all available grid layer names.

        Returns:
            dict: Available grid layer names.
        """
        return self.map_generator.get_grid_layer_names()

    def get_vector_layer_groups(self):
        """
        Retrieves all available vector layer groups.

        Returns:
            dict: Available vector layer groups.
        """
        return self.map_generator.get_vector_layer_groups()

    def generate_map_id(self):
        """
        Generates a unique map ID.

        Returns:
            dict: Object containing the generated map ID.
        """
        return self.map_generator.generate_map_id()
        
    def fetch_pois_from_polygon(self, coordinates, poi_types=None):
        """
        Fetches Points of Interest (POIs) within a polygon defined by coordinates.

        Args:
            coordinates (list): List of coordinate tuples [(lon, lat), ...] defining a polygon.
            poi_types (list, optional): List of POI types to filter by (e.g., ["restaurant", "school"])

        Returns:
            dict: Dictionary containing POIs found within the polygon.
        """
        return self.poi_handler.fetch_pois_from_polygon(coordinates, poi_types)

    def fetch_pois_from_buffer(self, center_point, radius_meters, poi_types=None):
        """
        Fetches POIs within a circular buffer around a point.

        Args:
            center_point (tuple): Center point (lon, lat) of the buffer.
            radius_meters (float): Radius of the buffer in meters.
            poi_types (list, optional): List of POI types to filter by.

        Returns:
            dict: Dictionary containing POIs found within the polygon.
        """
        return self.poi_handler.fetch_pois_from_buffer(center_point, radius_meters, poi_types)

    def chat(self, query):
        """
        Send a query to the LLM triage chat API.

        Args:
            query (str): The user's query or message.

        Returns:
            dict: The chat response.
        """
        return self.chat_handler.chat(query)

    def address_to_latlon(self, address: str):
        """
        Converts an address to latitude and longitude.

        Args:
            address (str): The address to be converted.

        Returns:
            dict: The latitude and longitude of the address.
        """
        return self.geocode_functions.address_to_latlon(address)

    def postcode_to_latlon(self, postcode: str):
        """
        Converts a postcode to latitude and longitude.

        Args:
            postcode (str): The postcode to be converted.

        Returns:
            dict: The latitude and longitude of the postcode.
        """
        return self.geocode_functions.postcode_to_latlon(postcode)

    def latlon_to_postcode(self, lat: float, lon: float):
        """
        Converts latitude and longitude to a postcode.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.

        Returns:
            str: The postcode for the given latitude and longitude.
        """
        return self.geocode_functions.latlon_to_postcode(lat, lon)

    def latlon_to_address(self, lat: float, lon: float):
        """
        Converts latitude and longitude to an address.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.

        Returns:
            str: The address for the given latitude and longitude.
        """
        return self.geocode_functions.latlon_to_address(lat, lon)

    def latlon_to_admin_boundary(self, lat: float, lon: float):
        """
        Converts latitude and longitude to administrative boundaries.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.

        Returns:
            dict: The administrative boundaries for the given latitude and longitude.
        """
        return self.geocode_functions.latlon_to_admin_boundary(lat, lon)

    def latlon_to_city_country(self, lat: float, lon: float):
        """
        Converts latitude and longitude to city and country.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.

        Returns:
            dict: The city and country for the given latitude and longitude.
        """
        return self.geocode_functions.latlon_to_city_country(lat, lon)