from rest_framework import generics
from quotes.models import Quote
from .serializers import QuoteSerializer


class QuoteAPIView(generics.ListAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
