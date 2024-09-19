# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += key + "=" + value + "&"
    request_url = backend_url + endpoint + "?" + params
    print("GET from {}".format(request_url))
    try:
        # Call the get method of requests library with URL and parameters
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # If any network or request-related error occurs
        print(f"Network exception occurred: {e}")
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call the get method of requests library with URL and parameters
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # If any network or request-related error occurs
        print(f"Unexpected {e=}, {type(e)=}")
        print("Network exception occurred")
        return None


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        # If any network or request-related error occurs
        print(f"Network exception occurred: {e}")
        return None
