# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from djangor_app.models import Entries
from django.utils import timezone

from braces.views import LoginRequiredMixin

class EntryCreate(LoginRequiredMixin, CreateView):
    """A Class Based View For Creation of An Entry"""
    model = Entries

class EntryListView(ListView):
    """
    A Class Based View for Displaying A Rundown of Entries
    """
    model = Entries

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
