from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Path for user login
    path(route='login', view=views.login_user, name='login'),

    # Path for user logout
    path(route='logout/', view=views.logout_request, name='logout'),

    # Path for user registration
    path(route='register', view=views.registration, name='register'),

    # Path for dealer reviews view
    # path(route='reviews/', view=views.get_dealer_reviews, name='reviews'),

    # Path for adding a review
    # path(route='add_review/', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

