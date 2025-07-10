from django.urls import path, re_path # re_path رو اینجا اضافه کردیم
from .views import NewsArticleListView, NewsArticleDetailView, CategoryArticleListView

app_name = 'news' # Namespace for URLs

urlpatterns = [
    path('', NewsArticleListView.as_view(), name='list'), # Home page - list all news
    path('category/<slug:slug>/', CategoryArticleListView.as_view(), name='category_articles'), # Filter by category
    re_path(r'^(?P<slug>[-\w]+)/$', NewsArticleDetailView.as_view(), name='detail'), # <-- خط اصلاح شده برای پشتیبانی از اسلاگ فارسی
]