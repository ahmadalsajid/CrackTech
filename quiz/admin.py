from django.contrib import admin
from quiz.models import Tag


class TagInline(admin.TabularInline):
    model = Tag


class TagAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
