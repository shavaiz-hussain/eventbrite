# eventbrite_integration/urls.py
from django.urls import path

from .views import CreateEventView, EventListView

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    path("<str:event_id>", EventListView.as_view(), name="event_detail"),
    path("create/", CreateEventView.as_view(), name="create_event"),
]
