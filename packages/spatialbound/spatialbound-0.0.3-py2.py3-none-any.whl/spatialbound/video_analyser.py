# spatialbound/video_analyser.py
import os
import json
import tempfile
import requests
from .config import ALLOWED_VIDEO_EXTENSIONS

class VideoAnalyser:
    def __init__(self, api_handler):
        self.api_handler = api_handler
    
    def upload_video(self, file_path):
        """
        Upload a video file to the API server.
        
        Args:
            file_path (str): Path to the video file on the local system.
            
        Returns:
            dict: Response containing the uploaded video URL.
        """
        if not os.path.isfile(file_path):
            return {"error": "File does not exist."}
        
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in ALLOWED_VIDEO_EXTENSIONS:
            return {"error": f"Invalid video file extension. Allowed extensions are: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}"}
        
        endpoint = "/api/upload_video"
        
        # Upload the video file
        with open(file_path, 'rb') as file:
            files = {'file': file}
            return self.api_handler.make_authorised_request(endpoint, method='POST', files=files)
    
    def analyse_video(self, video_url, user_prompt, fps):
        """
        Process a video file and convert it to structured data.
        
        Args:
            video_url (str): The URL of the previously uploaded video to process.
            user_prompt (str): The prompt for AI analysis.
            fps (int): Frames per second to extract.
            
        Returns:
            dict: A message and the extracted data.
        """
        # Validate inputs
        if not video_url:
            return {"error": "Video URL is required."}
        
        if not user_prompt:
            return {"error": "User prompt is required."}
        
        if fps <= 0 or fps > 25:
            return {"error": "FPS must be between 1 and 25."}
        
        endpoint = "/api/convert_video"
        
        # Prepare form data
        form_data = {
            'video_url': video_url,
            'user_prompt': user_prompt,
            'fps': fps
        }
        
        return self.api_handler.make_authorised_request(endpoint, method='POST', data=form_data)
    
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
        if not query:
            return {"error": "Search query is required."}
        
        if not video_url:
            return {"error": "Video URL is required."}
        
        endpoint = "/api/search_video"
        
        payload = {
            "query": query,
            "video_url": video_url,
            "limit": limit,
            "search_mode": search_mode
        }
        
        return self.api_handler.make_authorised_request(endpoint, method='POST', json=payload)
    
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
        if not video_url:
            return {"error": "Video URL is required."}
        
        if timestamp < 0:
            return {"error": "Timestamp must be non-negative."}
        
        if threshold < 0.1 or threshold > 1.0:
            return {"error": "Threshold must be between 0.1 and 1.0."}
        
        endpoint = "/api/find_similarities"
        
        payload = {
            "video_url": video_url,
            "timestamp": timestamp,
            "limit": limit,
            "threshold": threshold
        }
        
        return self.api_handler.make_authorised_request(endpoint, method='POST', json=payload)
    
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
        if not os.path.isfile(image_path):
            return {"error": "Image file does not exist."}
        
        if not video_url:
            return {"error": "Video URL is required."}
        
        if threshold < 0.1 or threshold > 1.0:
            return {"error": "Threshold must be between 0.1 and 1.0."}
        
        endpoint = "/api/find_image_in_video"
        
        # Prepare form data with image file
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            form_data = {
                'video_url': video_url,
                'threshold': str(threshold)
            }
            
            return self.api_handler.make_authorised_request(endpoint, method='POST', files=files, data=form_data)
    
    def analyze_video_location(self, video_url, fps=2):
        """
        Analyze a video to determine its geographical location.
        
        Args:
            video_url (str): URL of the video to analyze.
            fps (int, optional): Frames per second to extract (default 2).
            
        Returns:
            dict: Geolocation analysis results.
        """
        if not video_url:
            return {"error": "Video URL is required."}
        
        if fps <= 0 or fps > 5:
            return {"error": "FPS must be between 1 and 5."}
        
        endpoint = "/api/analyze_video_location"
        
        payload = {
            "video_url": video_url,
            "fps": fps
        }
        
        return self.api_handler.make_authorised_request(endpoint, method='POST', json=payload)