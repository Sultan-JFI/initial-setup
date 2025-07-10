from django.contrib import admin
from .models import Category, NewsArticle

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Auto-fill slug from name

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'publish_date', 'is_published')
    list_filter = ('is_published', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)} # Auto-fill slug from title
    date_hierarchy = 'publish_date'
    raw_id_fields = ('author',) # Use a widget to select author by ID
    actions = ['make_published', 'make_unpublished'] # Custom actions

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, "اخبار انتخاب شده با موفقیت منتشر شدند.")
    make_published.short_description = "انتشار اخبار انتخاب شده"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, "اخبار انتخاب شده از حالت انتشار خارج شدند.")
    make_unpublished.short_description = "لغو انتشار اخبار انتخاب شده"