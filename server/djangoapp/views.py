# Uncomment the required imports before adding the code

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json

from .populate import initiate
from .models import CarMake, CarModel  # Add this import
from .restapis import get_request, analyze_review_sentiments, post_review  # Import methods from restapis.py

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['userName']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response_data = {"userName": username, "status": "Authenticated"}
            else:
                response_data = {"status": "Invalid credentials"}
        except KeyError:
            response_data = {"status": "Missing credentials"}
        return JsonResponse(response_data)
    return JsonResponse({"status": "Invalid request method"}, status=405)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    if request.method == 'POST':
        # Perform the logout operation
        username = request.user.username if request.user.is_authenticated else ""
        logout(request)
        # Return a JSON response
        response_data = {"userName": username, "status": "Logged out successfully"}
        return JsonResponse(response_data)
    return JsonResponse({"status": "Invalid request method"}, status=405)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['userName']
            password = data['password']
            first_name = data['firstName']
            last_name = data['lastName']
            email = data['email']
            username_exist = False
            email_exist = False
            try:
                # Check if user already exists
                User.objects.get(username=username)
                username_exist = True
            except User.DoesNotExist:
                # If not, simply log this is a new user
                logger.debug("{} is new user".format(username))
            # If it is a new user
            if not username_exist:
                # Create user in auth_user table
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
                # Login the user
                login(request, user)
                data = {"userName": username, "status": "Authenticated"}
            else:
                data = {"userName": username, "error": "Already Registered"}
        except KeyError:
            data = {"status": "Missing information"}
        return JsonResponse(data)
    return JsonResponse({"status": "Invalid request method"}, status=405)

# Create the `get_cars` view to return a list of car models
def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.make.name} for car_model in car_models]
    return JsonResponse({"CarModels": cars})

# Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = post_review(data)
            return JsonResponse({"status": 200, "message": "Review added successfully"})
        except Exception as e:
            logger.error(f"Error: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 405, "message": "Method not allowed"})
