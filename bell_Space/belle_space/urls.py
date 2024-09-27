from django.urls import path
from . import views
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="employee"),
]