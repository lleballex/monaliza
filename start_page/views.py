from django.shortcuts import render
from django.views.generic import TemplateView

class MainView(TemplateView):
	template_name = 'start_page/main_view.html'
