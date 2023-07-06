from django.contrib import admin

from .models import User, Tag, Subscription, Blog, Post, Comment, Like


class UserAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('username',  'is_admin')
    search_fields = ('username', 'is_admin')
    list_filter = ('username',  'is_admin')
    readonly_fields = ('created_at',)


class TagAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)
    readonly_fields = ('created_at',)


class BlogAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('title',)
    readonly_fields = ('created_at',)


class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'get_author', 'get_blog')
    search_fields = ('title', 'description', 'get_author', 'get_blog')
    list_filter = ('title',)

    def get_author(self, obj):
        return obj.author

    def get_blog(self, obj):
        return obj.blog


class LikeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('user', 'post',)
    search_fields = ('user', 'post',)
    list_filter = ('user', 'post',)
    readonly_fields = ('created_at',)


class SubscriptionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('user', 'blog',)
    search_fields = ('user', 'blog',)
    list_filter = ('user', 'blog',)
    readonly_fields = ('created_at',)


class CommentAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('user', 'post', 'body')
    search_fields = ('user', 'post', 'body')
    list_filter = ('user', 'post', 'body')
    readonly_fields = ('created_at',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Post, PostAdmin)