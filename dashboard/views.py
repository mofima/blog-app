from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View 

from item.models import Article

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        ctx = {
            'articles': articles 
        }

        return render(request, 'dashboard/index.html', ctx)

