from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'likes')
    search_fields = ('content',)
    list_filter = ('created_at', 'likes')

admin.site.register(Post,PostAdmin)