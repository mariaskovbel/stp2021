from django.urls import path
from .views import QuoteListView

urlpatterns = [
    path('', QuoteListView.as_view(), name='home'),
]
