from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.management import call_command
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group # این خط را اضافه کنید
from .models import Category, NewsArticle

class CustomAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-github/', self.admin_view(self.sync_data), name='sync-github'),
        ]
        return custom_urls + urls

    def sync_data(self, request):
        if request.method == 'POST':
            try:
                from io import StringIO
                out = StringIO()
                call_command('sync_to_github', stdout=out)
                messages.success(request, 'همگام‌سازی با موفقیت انجام شد: ' + out.getvalue())
            except Exception as e:
                messages.error(request, f'خطا در هنگام همگام‌سازی: {e}')
            
            return redirect('admin:index')
        
        return render(request, 'admin/sync_confirm.html', context={'site_header': self.site_header, 'site_title': self.site_title})

admin_site = CustomAdminSite(name='custom_admin')

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NewsArticle, site=admin_site)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'publish_date', 'is_published')
    list_filter = ('is_published', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    raw_id_fields = ('author',)
    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, "اخبار انتخاب شده با موفقیت منتشر شدند.")
    make_published.short_description = "انتشار اخبار انتخاب شده"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, "اخبار انتخاب شده از حالت انتشار خارج شدند.")
    make_unpublished.short_description = "لغو انتشار اخبار انتخاب شده"

# ثبت مدل‌های User و Group با admin_site سفارشی
admin_site.register(User)
admin_site.register(Group)
