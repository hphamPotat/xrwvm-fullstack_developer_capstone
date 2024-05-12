# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarMake, CarModel


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return JsonResponse({'userName': ''})

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data['userName']
    pwd = data['password']
    f_name = data['firstName']
    l_name = data['lastName']
    email = data['email']

    exists = User.objects.filter(username=username)
    if exists:
        return JsonResponse({'userName': username, 'error': 'Already Registered'})

    user = User.objects.create_user(username=username, first_name=f_name, last_name=l_name,password=pwd, email=email)
    login(request, user)
    return JsonResponse({'userName': username, 'status': 'Authenticated'})

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f'/fetchReviews/dealer/{dealer_id}'
        reviews = get_request(endpoint)
        
        for review in reviews:
            res = analyze_review_sentiments(review['review'])
            review['sentiment'] = res['sentiment']

        return JsonResponse({"status":200, "reviews":reviews})

    return JsonResponse({"status":400,"message":"Bad Request"})
    

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        dealership = get_request(f'/fetchDealer/{dealer_id}')
        return JsonResponse({"status": 200, "dealer": dealership})
    
    return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `add_review` view to submit a review
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            res = post_review(data)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401,"message": "Error in posting review"})

    return JsonResponse({"status": 403,"message": "Unauthorized"})


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})
