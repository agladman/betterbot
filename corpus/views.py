from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.db.models import Count, Min, Sum, Avg

from .models import BaseText, Sentence

from random import choice, sample
from betterbot.settings import CONFIG


class HomeView(View):

    def get(self, request):
        pool = list(Sentence.objects.active())
        if len(pool) == 0:
            candidate1 = Sentence.create()
            candidate2 = Sentence.create()
        elif len(pool) == 1:
            candidate1 = Sentence.create()
            candidate2 = pool[0]
        else:
            candidate1, candidate2 = sample(pool, 2)

        # but if the pool is still small create a new candidate
        # in order to keep growing the pool to the desired size
        if len(pool) < CONFIG['limits']['candidate_pool_min_size']:
            candidate2 = Sentence.create()

        ctx = {
            'strapline': choice(CONFIG['straplines']),
            'candidate1': candidate1,
            'candidate2': candidate2,
            'dismissal': choice(CONFIG['dismissals'])
        }

        return render(request, template_name='index.html', context=ctx)

    def post(self, request):
        chosen = int(request.POST.get('chosen'))
        c1 = int(request.POST.get('candidate1'))
        c2 = int(request.POST.get('candidate2'))
        my_tuple = (c1, c2)
        for i, id_val in enumerate(my_tuple):
            s = Sentence.objects.get(pk=id_val)
            if chosen == 2:
                s.lose()
            elif chosen == i:
                s.win()
            s.appearances += 1
            s.save()

        return HttpResponseRedirect('/')


class AboutView(View):

    def get(self, request):

        ups_sum = sum(i.ups for i in Sentence.objects.all())
        downs_sum = int(sum(i.downs for i in Sentence.objects.all()) / 2)

        ctx = {
            'strapline': choice(CONFIG['straplines']),
            'mostpop': Sentence.objects.most_popular_now(),
            '7days': Sentence.objects.popular_last_week(),
            'newest10': Sentence.objects.newest_ten(),
            'total_basetext': len(BaseText.objects.all()),
            'active_basetext': len([x for x in BaseText.objects.all() if x.check_age()]),
            'total_sentence': len(Sentence.objects.all()),
            'active_sentence': len(Sentence.objects.active()),
            'number_tweeted': len(Sentence.objects.tweeted()),
            'ups_cast': ups_sum,
            'downs_cast': downs_sum,
            'total_votes': ups_sum + downs_sum
        }
        return render(request, template_name='about.html', context=ctx)


class FAQView(View):

    def get(self, request):
        ctx = {
            'strapline': choice(CONFIG['straplines'])
        }
        return render(request, template_name='faq.html', context=ctx)
