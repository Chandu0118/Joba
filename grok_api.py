# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 21:45:04 2025

@author: USER
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GrokModel:
    def __init__(self, model_name, api_key=None):
        """
        Initialize the Grok API client with a model name and API key.
        API key is loaded from environment variable for security.
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GROK_API_KEY")
        if not self.api_key:
            raise ValueError("Grok API key is required. Set it in your .env file as GROK_API_KEY.")
        self.endpoint = "https://api.grok.xai.com/v1/completions"  # Hypothetical endpoint; replace with actual Grok 2 API URL

    def __call__(self, prompt):
        """
        Make a request to the Grok API with the given prompt.
        Returns the response text.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": 500  # Adjust based on Grok 2 limits
        }
        try:
            response = requests.post(self.endpoint, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json().get("text", "No text response found")  # Adjust based on actual response structure
        except requests.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")

# Example usage (uncomment to test locally, but don’t commit this part to GitHub)
# if __name__ == "__main__":
#     grok = GrokModel(model_name="grok-2")
#     response = grok("Hello, how can you help me with CV generation?")
#     print(response)