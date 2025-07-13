from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.management import call_command
from django.contrib.admin import AdminSite
from .models import Category, NewsArticle

# تعریف یک AdminSite سفارشی برای اضافه کردن URLهای جدید
class CustomAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        # تعریف URL برای صفحه همگام‌سازی
        custom_urls = [
            path('sync-github/', self.admin_view(self.sync_data), name='sync-github'),
        ]
        return custom_urls + urls

    # تابع برای اجرای دستور sync_to_github
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
        
        # رندر کردن صفحه تایید قبل از اجرا
        return render(request, 'admin/sync_confirm.html', context={'site_header': self.site_header, 'site_title': self.site_title})


# حالا admin.site پیش‌فرض را با CustomAdminSite جایگزین می‌کنیم
# اگر این خط از قبل در settings.py شما برای admin.site وجود ندارد، نیازی نیست اینجا تغییر دهید.
# اما اگر از admin.site در جای دیگری استفاده کرده‌اید، مطمئن شوید که به admin_site اشاره کنید.
admin_site = CustomAdminSite(name='custom_admin')


@admin.register(Category, site=admin_site) # تغییر: site=admin_site اضافه شد
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(NewsArticle, site=admin_site) # تغییر: site=admin_site اضافه شد
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
