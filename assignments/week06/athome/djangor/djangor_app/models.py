from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class Entries(models.Model):
    """
    An entry in our blog application.
    """
    title = models.CharField('Title', max_length=1024)
    text = models.CharField('Text', max_length=1024)
    publication_date = models.DateTimeField('Publication Date', auto_now_add=True)
    author = models.ForeignKey(User)

    def get_absolute_url(self):
        return reverse('entry_list')

    def __unicode__(self):
        return self.title
