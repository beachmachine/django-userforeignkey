import datetime

from django.db import models
from django.utils import timezone
from django_userforeignkey.models.fields import UserForeignKey


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="Publication date of poll")
    created_by = UserForeignKey(auto_user_add=True, verbose_name="The user that created the poll",
                                related_name="polls")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Publication date of poll")

    def __str__(self):
        return self.question

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'



class Choice(models.Model):
    poll = models.ForeignKey(Poll, verbose_name="Which poll?", related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.choice_text



class ActualVote(models.Model):
    poll = models.ForeignKey(Poll, verbose_name="Which question has been voted for?", on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, verbose_name="Which choice was chosen?", on_delete=models.CASCADE)
    user = UserForeignKey(auto_user_add=True, verbose_name="Which user has voted?", related_name="actual_votes")

