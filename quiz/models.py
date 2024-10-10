from django.db import models


class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='tags', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
