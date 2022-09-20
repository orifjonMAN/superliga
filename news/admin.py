from django.contrib import admin
from .models import New, Review, Category

admin.site.register(Review)
admin.site.register(Category)


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'new_author', 'created', 'category')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'new_author', 'created', 'category')
# Register your models here.
