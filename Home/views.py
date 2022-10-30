from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView,TemplateView

from Article.models import Article, Category


class Homepage(TemplateView):
    model=Article
    template_name = 'Home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.order_by('-created')[:5]
        popural_video=Article.objects.order_by('views')[:5]
        category_list=Category.objects.all()


        context.update({
        'most_viewer_article': popural_video,
            'article': articles,
            'category': category_list,



        })
        return context



# Create your views here.
