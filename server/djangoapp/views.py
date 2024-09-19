from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from .populate import initiate
from .models import CarMake, CarModel
from .restapis import (
    get_request,
    analyze_review_sentiments,
    post_review
)

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
                response_data = {
                    "userName": username,
                    "status": "Authenticated"
                }
            else:
                response_data = {"status": "Invalid credentials"}
        except KeyError:
            response_data = {"status": "Missing credentials"}
        return JsonResponse(response_data)
    return JsonResponse({"status": "Invalid request method"}, status=405)

@csrf_exempt
def logout_request(request):
    if request.method == 'POST':
        username = request.user.username if request.user.is_authenticated else ""
        logout(request)
        response_data = {
            "userName": username,
            "status": "Logged out successfully"
        }
        return JsonResponse(response_data)
    return JsonResponse({"status": "Invalid request method"}, status=405)

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
            try:
                User.objects.get(username=username)
                username_exist = True
            except User.DoesNotExist:
                logger.debug(f"{username} is new user")
            if not username_exist:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    email=email
                )
                login(request, user)
                data = {
                    "userName": username,
                    "status": "Authenticated"
                }
            else:
                data = {
                    "userName": username,
                    "error": "Already Registered"
                }
        except KeyError:
            data = {"status": "Missing information"}
        return JsonResponse(data)
    return JsonResponse({"status": "Invalid request method"}, status=405)

def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('make')
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.make.name
        }
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({
        "status": 200,
        "dealers": dealerships
    })

def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({
            "status": 200,
            "dealer": dealership
        })
    return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({
            "status": 200,
            "reviews": reviews
        })
    return JsonResponse({"status": 400, "message": "Bad Request"})

@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_review(data)
            return JsonResponse({
                "status": 200,
                "message": "Review added successfully"
            })
        except Exception:
            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"
            })
    return JsonResponse({"status": 405, "message": "Method not allowed"})
