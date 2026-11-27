from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class AIAssistantPageView(LoginRequiredMixin, View):
    template_name = 'ai_assistant/index.html'

    def get(self, request):
        return render(request, self.template_name)
