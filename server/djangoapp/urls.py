from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path to register
    path(route='register', view=views.registration, name='register'),
    # path to login
    path(route='login', view=views.login_user, name='login'),
    # path to logout
    path(route='logout', view=views.logout_request, name='logout'),
    # path to get dealers
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    # path to get dealers based on state
    path(
        route='get_dealers/<str:state>',
        view=views.get_dealerships,
        name='get_dealers_by_state'
    ),
    # path to get dealers based on dealer id
    path(
        route='dealer/<int:dealer_id>',
        view=views.get_dealer_details,
        name='dealer_details'
    ),
    # path to get reviews from a specific dealer
    path(
        route='reviews/dealer/<int:dealer_id>',
        view=views.get_dealer_reviews,
        name='dealer_details'
    ),
    # path to add review
    path(route='add_review', view=views.add_review, name='add_review'),
    # path to get cars
    path(route='get_cars', view=views.get_cars, name='getcars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
