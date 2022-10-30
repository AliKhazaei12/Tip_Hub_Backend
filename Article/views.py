from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from .models import Article, Category
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .mixins import FieldMixin, FormValidMixin, UserAccessMixin, AccessMixin, TeacherAccessMixin
from hitcount.views import HitCountDetailView
from Account.models import User

class Videodetail(HitCountDetailView):
    model = Article
    template_name = 'Article/video_detail.html'
    count_hit = True

    # def post(self, request, *args, **kwargs):
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         Article = self.get_object()
    #         form.instance.user = request.user
    #         form.instance.Article = Article
    #         form.save()
    #
    #     return HttpResponseRedirect(reverse('Article:video_detail', kwargs={
    #         'pk': Article.pk
    #     }))

    # def get_context_data1(self,**kwargs):
    #     article_comments_count = Comment.objects.all().filter(Article=self.object.id).count()
    #     article_comments = Comment.objects.all().filter(Article=self.object.id)
    #     print("HHHHHHHHHHHHHHHHHHHHH",article_comments_count)
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'form': self.form,
    #         'article_comments': article_comments,
    #         'article_comments_count': article_comments_count
    #
    #     })
    #     return context

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # connected_comments = Comment.objects.filter(Article=self.get_object())
        # number_of_comments = connected_comments.count()
        # data['comments'] = connected_comments
        # data['no_of_comments'] = number_of_comments
        # data['comment_form'] = CommentForm()
        likes_connected = get_object_or_404(Article, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True

        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked

        return data

    # def post(self, request, *args, **kwargs):
    #     if self.request.method == 'POST':
    #         comment_form = CommentForm(self.request.POST)
    #         if comment_form.is_valid():
    #             text = comment_form.cleaned_data['text']
    #             try:
    #                 patern = comment_form.cleaned_data['patern']
    #             except:
    #                 patern = None
    #
    #         new_comment = Comment(text=text, user=self.request.user, Article=self.get_object(),
    #                               patern=patern)
    #         new_comment.save()
    #         return redirect(self.request.path_info)


def VideoLike(request, pk):
    video = get_object_or_404(Article, id=request.POST.get('Article_id'))
    if video.likes.filter(id=request.user.id).exists():
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)

    return HttpResponseRedirect(reverse('Article:video_detail', args=[str(pk)]))


class VideoList(TemplateView):
    model = Article
    template_name = 'Article/video_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(VideoList, self).get_context_data(**kwargs)
        list_Article = Article.objects.order_by('-created','status=p')
        paginator = Paginator(list_Article, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            list_article = paginator.page(page)
        except PageNotAnInteger:
            list_article = paginator.page(1)
        except EmptyPage:
            list_article = paginator.page(paginator.num_pages)

        context['articles'] = list_article
        return context


class MostViewVideoList(TemplateView):
    model = Article
    template_name = 'Article/mostview_video_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(MostViewVideoList, self).get_context_data(**kwargs)
        list_Article = Article.objects.order_by('views','status')
        # print(list_Article)
        paginator = Paginator(list_Article, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            list_article = paginator.page(page)
        except PageNotAnInteger:
            list_article = paginator.page(1)
        except EmptyPage:
            list_article = paginator.page(paginator.num_pages)

        context.update({
            'article': list_article,

        })
        return context


class SearchResultsView(ListView):
    model = Article
    template_name = "Article/shearch_rsult.html"
    paginate_by = 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Article.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context


class Category_Detail(DetailView):
    model = Category
    template_name = 'Article/category_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     category = Category.objects.filter(parent=None)
    #     video_category = Article.objects.filter(category=category)
    #     return context.update({
    #         'category':category,
    #         'video_category':video_category
    #     })

# class CategoryList(ListView):
#     model = Category
#     template_name = 'include/navbar.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Category'] = Category.objects.filter(parent=None)
#         return context
#
def CategoryList(request,pk):
    cat = get_object_or_404(Category, pk=Category.pk)
    category_list = Category.objects.filter(parent=None)
    video_category = Article.objects.filter(category=category_list)
    context = {
        "Category": cat.objects.filter(parent=None),
        "category_list":category_list,
        "video_category":video_category


    }
    return render(request, 'include/navbar.html', context)


def paneladmin(request):
    return render(request, 'Article/Admin_panel.html', {})


class ArticleList(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'Article/article_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(teacher=self.request.user)


class ArticleCreate(LoginRequiredMixin, FormValidMixin, FieldMixin, CreateView):
    model = Article
    template_name = 'Article/article_create.html'

    def get_success_url(self):
        return reverse_lazy('Article:Article_admin')


class ArticleUpdate(UserAccessMixin, AccessMixin, FormValidMixin, FieldMixin, UpdateView):
    model = Article
    template_name = 'Article/article_create.html'

    def get_success_url(self):
        return reverse_lazy('Article:Article_admin')


class ArticleDelete(DeleteView):
    model = Article
    template_name = 'Article/article_delete.html'

    def get_success_url(self):
        return reverse_lazy('Article:Article_admin')


class Videopriview(TeacherAccessMixin, DetailView):
    model = Article
    template_name = 'Article/video_detail.html'

