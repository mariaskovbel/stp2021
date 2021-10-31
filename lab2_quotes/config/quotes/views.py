from django.views.generic import ListView
from .models import Quote


class QuoteListView(ListView):
    model = Quote
    template_name = 'quote_list.html'
