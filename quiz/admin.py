from pprint import pprint
from django.contrib import admin
from quiz.models import Tag, Question, FavoriteQuestion, ReadQuestion


class TagInline(admin.TabularInline):
    model = Tag


class TagAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    list_display = ('name',)
    search_fields = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'correct_answer',)
    search_fields = ('question',)

    def save_related(self, request, form, formsets, change):
        _selected_tags = form.cleaned_data['tags']
        _tags = []
        if _selected_tags:
            for t in _selected_tags:
                while t:
                    _tags.append(t)
                    if not t.parent:
                        break
                    t = t.parent
        _tags = list(set(_tags))
        form.cleaned_data['tags'] = _tags
        super(QuestionAdmin, self).save_model(request, form, formsets, change)


class FavoriteQuestionAdmin(admin.ModelAdmin):
    # list_display = ('get_question', 'get_user',)
    list_display = ('get_user', 'get_questions')
    search_fields = ('question__question', 'user__username', 'user__email', 'user__first_name', 'user__last_name')


class ReadQuestionAdmin(admin.ModelAdmin):
    # list_display = ('get_question', 'get_user',)
    list_display = ('get_user', 'get_questions')
    search_fields = ('question__question', 'user__username', 'user__email', 'user__first_name', 'user__last_name')


admin.site.register(Tag, TagAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(FavoriteQuestion, FavoriteQuestionAdmin)
admin.site.register(ReadQuestion, ReadQuestionAdmin)
