from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify # For creating slugs automatically

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ (URL دوستانه)") # allow_unicode for Persian slugs

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', verbose_name="دسته‌بندی")
    title = models.CharField(max_length=200, verbose_name="عنوان خبر")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ (URL دوستانه)")
    content = models.TextField(verbose_name="محتوای خبر")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_articles', verbose_name="نویسنده")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="تصویر اصلی")
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_published = models.BooleanField(default=False, verbose_name="منتشر شده")

    class Meta:
        ordering = ['-publish_date']
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True) # Generate slug from title
        super().save(*args, **kwargs)