from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Ticket
from .forms import TicketForm

class IndexView(CreateView):
	model = Ticket
	form_class = TicketForm
	template_name = 'support/index.html'
	success_url = reverse_lazy('support:index')
