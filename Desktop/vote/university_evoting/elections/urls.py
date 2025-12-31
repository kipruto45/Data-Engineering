from django.urls import path
from .views import ElectionListView, PositionListView, PositionCreateView, PositionDetailView

urlpatterns = [
    path("", ElectionListView.as_view(), name="api-elections"),
    path("<int:election_id>/positions/", PositionListView.as_view(), name="api-election-positions"),
    path("<int:election_id>/positions/<int:pk>/", PositionDetailView.as_view(), name="api-election-position-detail"),
]
