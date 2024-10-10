from pprint import pprint
from django.contrib import admin
from quiz.models import Tag, Question


class TagInline(admin.TabularInline):
    model = Tag


class TagAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    list_display = ('name',)
    search_fields = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'right_answer',)
    search_fields = ('question',)

    def save_related(self, request, form, formsets, change):
        pprint(form.cleaned_data)
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
        print(_tags)
        form.cleaned_data['tags'] = _tags
        super(QuestionAdmin, self).save_model(request, form, formsets, change)


admin.site.register(Tag, TagAdmin)
admin.site.register(Question, QuestionAdmin)
