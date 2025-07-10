from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import NewsArticle, Category

class NewsArticleListView(ListView):
    model = NewsArticle
    template_name = 'news/news_list.html' # Path to your template file
    context_object_name = 'articles' # Name of the variable to use in template
    paginate_by = 10 # Number of articles per page
    queryset = NewsArticle.objects.filter(is_published=True).select_related('category', 'author') # Prefetch related objects for performance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() # Pass categories to template
        return context

class NewsArticleDetailView(DetailView):
    model = NewsArticle
    template_name = 'news/news_detail.html' # Path to your template file
    context_object_name = 'article'
    queryset = NewsArticle.objects.filter(is_published=True).select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add related articles here if needed
        return context

class CategoryArticleListView(ListView):
    model = NewsArticle
    template_name = 'news/category_articles.html' # Path to your template file
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return NewsArticle.objects.filter(category=self.category, is_published=True).select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all() # Pass categories to template
        return context