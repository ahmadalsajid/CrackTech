from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from users.models import User
from icecream import ic
from pprint import pprint
from django.db import connection, reset_queries


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='tags', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Question(models.Model):
    question = models.TextField(db_index=True)
    option_1 = models.CharField(max_length=255, null=True, blank=True)
    option_2 = models.CharField(max_length=255, null=True, blank=True)
    option_3 = models.CharField(max_length=255, null=True, blank=True)
    option_4 = models.CharField(max_length=255, null=True, blank=True)
    correct_answer = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    users = models.ManyToManyField(User, related_name='questions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-created_at']

@receiver(pre_save, sender=Question)
def set_question_tags(sender, instance, **kwargs):
    try:
        _tags = []
        reset_queries()
        for t in instance.tags.select_related('parent').all():
            while t:
                _tags.append(t)
                if not t.parent:
                    break
                t = t.parent
        instance.tags.set(list(set(_tags)))
    except Exception as e:
        pass
