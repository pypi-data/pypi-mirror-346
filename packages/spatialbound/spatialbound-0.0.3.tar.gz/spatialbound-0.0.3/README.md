
# SpatialBound API Client Library

A Python client library for the SpatialBound SDK API, providing access to spatial AI and analytics, mapping, geocoding, routing, raw video streams to structured geospatial database, and environmental data services.

## Installation

```shell
pip install spatialbound
```

## Getting Started

Initialize the client with your API key:

```shell
from spatialbound import Spatialbound
```

## Initialize with your API key

```shell
spatialbound = Spatialbound(api_key)
```

## View login response

```shell
print("Login Response:", spatialbound.login_response)
Features and Examples
```

##  Map Generation
Create grid maps for specific areas:

```shell
# Generate a map ID
map_id_response = spatialbound.generate_map_id()
map_id = map_id_response.get('map_id')
print(f"Generated map ID: {map_id}")
```

## Create a grid map for Central London

```shell
london_bbox = "51.505,-0.155,51.520,-0.130"  # Central London bounding box
grid_map = spatialbound.create_map(
    map_id=f"{map_id}_grid",
    layers=["green_spaces", "water", "residential"],
    grid_or_vector="grid",
    grid_type="square",
    resolution=100,
    boundary_type="bbox",
    boundary_details=london_bbox,
    operation="visualisation"
)
print(f"Grid map created: {grid_map.get('message')}")
print(f"Number of features: {len(grid_map.get('data', {}).get('features', []))}")
```

## Geocoding
Convert addresses to coordinates:

```shell
# Convert address to lat/lon
address = "SW1A 0AA"  # Houses of Parliament
address_coords = spatialbound.address_to_latlon(address)
print(f"Coordinates for {address}: {address_coords}")
```

## Conversational AI
Ask questions about locations:

```shell
# Ask a question via chat
chat_response = spatialbound.chat("no what did i ask most recently after the joke")
print(f"Chat response: {chat_response}")
```

## Navigation and Routing
Calculate routes between locations:

```shell
# Create a route between multiple points
origin_address = "London Eye, London, UK"
destination_addresses = [
    "British Museum, London, UK",
    "Tower of London, London, UK"
]

address_route = spatialbound.navigate(
    route_type="address",
    origin=origin_address,
    destinations=destination_addresses,
    optimisation_type="shortest_path",  # Route through parks and green areas
    mode_of_travel="walk"
)
print('route', address_route)
```


## Location Analysis
Analyze residential locations:

```shell
# Analyze residential location by address
residential_analysis = spatialbound.analyse_location(
    location_type="residential",
    address="221B Baker Street, London",
    transaction_type="buy",
    radius=400  # 400 meters radius
)
print(residential_analysis)
```
## Weather Data
Get current weather information:

```shell
# Get weather data for London
london_coords = (51.5074, -0.1278)  # London coordinates
weather_data = spatialbound.get_weather(london_coords[0], london_coords[1])
print(f"Current weather in {weather_data.get('name', 'Unknown')}:")
print(f"Temperature: {weather_data.get('temp_c', 'Unknown')}°C / {weather_data.get('temp_f', 'Unknown')}°F")
print(f"Condition: {weather_data.get('condition_text', 'Unknown')}")
print(f"Wind Speed: {weather_data.get('wind_kph', 'Unknown')} kph")
print(f"Humidity: {weather_data.get('humidity', 'Unknown')}%")
```

## Air Quality Data
Retrieve air quality metrics:

```shell
# Get air quality data for New York
ny_coords = (40.7128, -74.0060)  # New York coordinates
air_quality = spatialbound.get_air_quality(ny_coords[0], ny_coords[1])
print(f"Air quality in {air_quality.get('location_name', 'Unknown')}:")
print(f"US EPA Index: {air_quality.get('us_epa_index', 'Unknown')}")
print(f"PM2.5: {air_quality.get('pm2_5', 'Unknown')}")
print(f"PM10: {air_quality.get('pm10', 'Unknown')}")
print(f"Ozone (O3): {air_quality.get('o3', 'Unknown')}")
print(f"Nitrogen Dioxide (NO2): {air_quality.get('no2', 'Unknown')}")
```


## Library Structure

```shell
spatialbound/
│
├── MANIFEST.in
├── spatialbound/
│ ├── __init__.py
│ ├── spatialbound.py
│ ├── api_handler.py
│ ├── route_calculator.py
│ ├── location_analyser.py
│ ├── video_analyser.py
│ ├── geocode_functions.py
│ ├── poi_handler.py
│ ├── chat_handler.py
│ ├── map_generator.py
│ ├── weather_handler.py
│ └── config.py
│
├── setup.py
└── README.md
```

## License

SpatialBound License

This proprietary software is the sole property of the copyright holder. You are granted permission to use this software solely in accordance to the terms and conditions of SpatialBound.
Under no circumstances may this software be copied, distributed, modified, or reused for any commercial purposes without explicit prior written consent from the copyright holder.
All rights reserved, including but not limited to distribution, modification, and use for commercial benefit outside the terms and conditions of SpatialBound.

## Support

For support, please contact contact@spatialbound.com