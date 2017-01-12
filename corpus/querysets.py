from django.db import models
from datetime import timedelta
from django.utils import timezone

from betterbot.settings import CONFIG


class SentenceQuerySet(models.QuerySet):

    def active(self):
        """
        ACTIVE SENTENCES: Sentences that can appear in choices and are candidates to be tweeted.

        Filters: tweeted = null,
                 dropped = null,
                 last_appearance < timezone.now() - timedelta(days=CONFIG['limits']['sentence_max_age'])

        Other possible criteria:
         score - max neg value
               - max neg value after min N appearances
               - as % of appearances, max neg value
         downs - max value
               - max value after min N appearances
               - as % of appearances, max value
        """
        q1 = self.extra(
            where={"created > NOW() - INTERVAL '{0} days'".format(CONFIG['limits']['sentence_max_age'])}).filter(
                score__gt=-3,
                tweeted__isnull=True)
        q2 = self.extra(
            where={"created > NOW() - INTERVAL '1 day'"}).filter(
                tweeted__isnull=True)

        return q1

    def popular_last_week(self):
        """
        Returns the 10 highest-scoring sentences from the last 7 days in dwscending order.
        Include tweeted__isnull=False to restrict this to sentences that were tweeted.
        """
        return self.extra(where={"created > NOW() - INTERVAL '7 days'"}).order_by('-score', '-ups', 'created')[:10]

    def most_popular_now(self):
        """
        Returns the most popular active sentence. Criteria are 1) is highest score, 2) most ups,
        3) oldest to youngest.
        """
        return self.active().order_by('-score', '-ups', 'created')[0]

    def newest_ten(self):
        """
        Returns the last 10 sentences created in descending age order.
        """
        return self.all().order_by('-created')[:10]

    def tweeted(self):
        """
        Returns a list of sentences tweeted ordered by the date they were tweeted.
        """
        return self.all().filter(tweeted__isnull=False).order_by('tweeted')
