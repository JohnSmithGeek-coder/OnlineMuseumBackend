from django.contrib import admin

# Register your models here.

from .models import CulturalRelicsData, Dynamic, ImgUrlTable
from .models import User, Star, Comment

admin.site.site_header = '掌上博物馆管理后台'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'email', 'gender', 'location', 'desc', 'date_joined', 'is_active', 'is_staff')

@admin.register(ImgUrlTable)
class ImgUrlTableAdmin(admin.ModelAdmin):
    list_display = ('img_id', 'url')

@admin.register(CulturalRelicsData)
class CulturalRelicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_name', 'museum', 'geography', 'dimensions', 'medium', 'cat1', 'cat2', 'time_period', 'cat3', 'url', 'img_url', 'object_id')

@admin.register(Dynamic)
class DynamicAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'files_urls', 'time')

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('user', 'cltrrlcs', 'dynamic', 'comment', 'time')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'cltrrlcs', 'dynamic', 'comment', 'user', 'reply_user', 'time', 'text', 'images')

