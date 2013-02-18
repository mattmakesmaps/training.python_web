# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from djangor_app.models import Entries

from braces.views import LoginRequiredMixin

class EntryCreate(LoginRequiredMixin, CreateView):
    """A Class Based View For Creation of An Entry"""
    model = Entries

class EntryListView(ListView):
    """
    A Class Based View for Displaying A Rundown of Entries
    """
    model = Entries
