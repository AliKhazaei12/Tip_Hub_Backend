from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Article


class FieldMixin():

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = [
                'teacher', 'slug', 'category', 'title'
                , 'body', 'video', 'image', 'status'
            ]
        elif request.user.is_teacher:
            self.fields = [
                'title', 'slug', 'category'
                , 'body', 'video', 'image'
            ]
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.teacher = self.request.user
            self.obj.satatus = 'd'
        return super().form_valid(form)


class UserAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.teacher == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("همچین صفحه ایی وجود ندارد")


class AccessMixin():
    def form_valid(self, form):
        if Article.status == 'p':
            print('ji')
            if self.request.user.is_superuser:
                form.save()
            else:
                self.obj = form.save(commit=False)
                self.obj.teacher = self.request.user
                self.obj.satatus = 'd'

        return super().form_valid(form)


class TeacherAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.teacher == request.user and article.status in ['b', 'd'] or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("همچین صفحه ای وجود ندارد")
