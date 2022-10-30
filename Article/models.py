from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.text import slugify
from hitcount.models import HitCountBase
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from Account.models import User
from extensions.utils import jalali_converter


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status='a')


class Category(models.Model):
    STATUS_CHOICES = (
        ('a', "فعال شده"),  # active
        ('i', "غیر فعال شده"),  # Inactive
    )

    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='Children', verbose_name='زیر دسته')
    title = models.CharField(max_length=35, unique=True, verbose_name="موضوع")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created').all()
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False




    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی "
        verbose_name_plural = "دسته بندی  ها"
        ordering = ['parent__id', '-created']

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش‌نویس'),  # draft
        ('p', "منتشر شده"),  # publish
        ('i', "در حال بررسی"),  # investigation
        ('b', "برگشت داده شده"),  # back
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Articles', verbose_name='استاد')
    category = models.ManyToManyField(Category, related_name='c_articles', verbose_name='دسته بندی ها')
    title = models.CharField(max_length=50, verbose_name='موضوع')
    body = models.TextField(verbose_name='توضیحات')
    video = models.FileField(upload_to='videos/articls', verbose_name='فیلم ها')
    image = models.ImageField(upload_to='images/articls', verbose_name='تصویر')
    views = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation',
                            verbose_name='بازدید ها')
    time = models.IntegerField(default=1, verbose_name='زمان فیلم')
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(User, related_name='blogpost_like')
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = ('ویدئو')
        verbose_name_plural = ('ویدئو ها')

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title)
        super(Article, self).save()

    def get_absolute_ulr(self):
        return reverse('Article:Article_admin')

    def __str__(self):
        return f'{self.title} - {self.body[:30]}'

    def number_of_likes(self):
        return self.likes.count()

    def jacraeted(self):
        return jalali_converter(self.created)

    jacraeted.short_description = 'تاریخ انتشار'

    def jupdated(self):
        return jalali_converter(self.updated)

    jupdated.short_description = 'تاریخ بروزرسانی '

    def image_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.image.url))

    objects = ArticleManager()

#
# class Comment(models.Model):
#     Article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment', verbose_name="ویدیو")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
#     created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
#     text = models.TextField(verbose_name="متن  کامنت")
#     patern = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='repleis',
#                                verbose_name="ریپلای_کامنت")
#
#     class Meta:
#         ordering = ['-created', ]
#         verbose_name = "کامنت"
#         verbose_name_plural = "کامنت ها"
#
#     def __str__(self):
#         return f'{self.user} - {self.text[:15]}'
#
#     def jcreated(self):
#         return jalali_converter(self.created)

# Create your models here.
