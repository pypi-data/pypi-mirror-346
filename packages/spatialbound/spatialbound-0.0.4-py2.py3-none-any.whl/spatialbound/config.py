# Description: Configuration file for the Urbani API

BASE_URL = 'https://www.spatialbound.com'
# BASE_URL = 'http://127.0.0.1:8000'
ALLOWED_OPTIMISATION_TYPES = [
    'shortest_path', 'green_spaces', 'residential_avoidance',
    'maximise_toilets', 'improve_walkability', 'avoid_crowds'
]
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi']
ALLOWED_MODES_OF_TRAVEL = ['walk', 'drive', 'bike']