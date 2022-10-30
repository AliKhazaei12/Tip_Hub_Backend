from django.urls import path
from .views import *

app_name = 'Article'

urlpatterns = [
    path('detail/<int:pk>', Videodetail.as_view(), name='video_detail'),
    path('video-like/<int:pk>', VideoLike, name="video_like"),
    path('list', VideoList.as_view(), name='Video_list'),
    path('list/<int:pk>', CategoryList, name='category_list'),
    path('CategoryDetail/<int:pk>', Category_Detail.as_view(), name='category_detail'),
    path('mostview/list', MostViewVideoList.as_view(), name='Most_view_Video_list'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path('admin_panel', paneladmin, name='panel_admin'),
    path('article_panel', ArticleList.as_view(), name='Article_admin'),
    path('article_create', ArticleCreate.as_view(), name='Article_create'),
    path('article_update/<int:pk>', ArticleUpdate.as_view(), name='Article_update'),
    path('article_delete/<int:pk>', ArticleDelete.as_view(), name='Article_delete'),
    path('priview/<int:pk>', Videopriview.as_view(), name='video_priview'),


]
