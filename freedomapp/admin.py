from django.contrib import admin
from .models import Category, Post, Comment, Like, Subscription

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_date', 'last_updated')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('category', 'author', 'publication_date')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_at', 'updated_at')
    search_fields = ('author', 'text', 'post__title')
    list_filter = ('created_at', 'updated_at', 'post')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at', 'post')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    date_hierarchy = 'date_subscribed'
    ordering = ('-date_subscribed',)
