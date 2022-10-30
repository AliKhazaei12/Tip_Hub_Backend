from django.contrib import admin
from .models import Article, Category
from django.utils.translation import ngettext
from django.contrib import messages


def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d  مقاله  منتشر شد.',
        '%d مقاله  منتشر شدند .',
        updated,
    ) % updated, messages.SUCCESS)

make_published.short_description = "انتشار مقالات انتخاب شده"


def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d  مقاله  پیش نویس شد.',
        '%d مقاله  پیش نویس شدند .',
        updated,
    ) % updated, messages.SUCCESS)

make_draft.short_description = "پیش‌نویس شدن مقالات انتخاب شده"


def make_investigation(modeladmin, request, queryset):
    updated = queryset.update(status='i')
    modeladmin.message_user(request, ngettext(
        '%d  مقاله  درحال بررسی قرار گرفت.',
        '%d  مقاله  درحال بررسی قرار گرفتند  .',
        updated,
    ) % updated, messages.SUCCESS)


make_investigation.short_description = "بررسی مقالات در حال برسی"


def make_back(modeladmin, request, queryset):
    updated = queryset.update(status='b')
    modeladmin.message_user(request, ngettext(
        '%d مقاله برگشت زده شد.',
        '%d مقاله برگشت زده شدند .',
        updated,
    ) % updated, messages.SUCCESS)


make_back.short_description = "مرجوع مقالات برگشت زده شده"


def make_active(modeladmin, request, queryset):
    updated = queryset.update(status='a')
    modeladmin.message_user(request, ngettext(
        '%d دسته بندی فعال شد.',
        '%d دسته بندی فعال شدند .',
        updated,
    ) % updated, messages.SUCCESS)

make_active.short_description = "فعال شدن دسته بندی های انتخاب شده"


def make_inactive(modeladmin, request, queryset):
    updated = queryset.update(status='i')
    modeladmin.message_user(request, ngettext(
        '%d  دسته بندی غیر فعال شد.',
        '%d دسته بندی غیر  فعال شدند .',
        updated,
    ) % updated, messages.SUCCESS)

make_inactive.short_description = "غیر فعال شدن دسته بندی های انتخاب شده"

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'status', 'parent'
    )
    search_fields = (['title'])

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    actions = [make_active,make_inactive]


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'teacher', 'title','image_tag' , 'time', 'jacraeted', 'jupdated', 'status'
    )
    search_fields = ('teacher', 'category', 'title')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    readonly_fields = ['created']
    actions = [make_published, make_draft, make_investigation, make_back]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)


# Register your models here.
