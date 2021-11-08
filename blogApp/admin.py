from django.contrib import admin
from .models import Article,Comment,Category

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on','author')
    list_filter = ("slug","status")
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

# models registerd here
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category)