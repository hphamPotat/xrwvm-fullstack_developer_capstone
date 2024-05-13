from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarMake, CarModel


logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    logout(request)
    return JsonResponse({'userName': ''})


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
        return JsonResponse(
            {
                'userName': username,
                'error': 'Already Registered'
            }
        )

    user = User.objects.create_user(
        username=username,
        first_name=f_name,
        last_name=l_name,
        password=pwd,
        email=email
    )
    login(request, user)
    return JsonResponse({'userName': username, 'status': 'Authenticated'})


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f'/fetchReviews/dealer/{dealer_id}'
        reviews = get_request(endpoint)
        for review in reviews:
            res = analyze_review_sentiments(review['review'])
            review['sentiment'] = res['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        dealership = get_request(f'/fetchDealer/{dealer_id}')
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as err:
            return JsonResponse({"status": 401, "message": f"{err}"})

    return JsonResponse({"status": 403, "message": "Unauthorized"})


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if not count:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append(
            {
                "CarModel": car_model.name,
                "CarMake": car_model.car_make.name
            }
        )
    return JsonResponse({"CarModels": cars})
