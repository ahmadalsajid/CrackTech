from icecream import ic
from django.core.management.base import BaseCommand
from quiz.models import Tag, Question
from faker import Faker
from pprint import pprint
from datetime import date, timedelta
import requests
import time
from random import randint, choices, sample


class Command(BaseCommand):
    help = "Creates Data for Users, Question, Tags"

    def handle(self, *args, **options):
        try:
            fake = Faker()

            # # create Tags
            # _eng_lang = Tag.objects.create(name='English Language')
            # _parts_of_speech = Tag.objects.create(name='Parts of Speech', parent=_eng_lang)
            # _noun = Tag.objects.create(name='Noun', parent=_parts_of_speech)
            # _pn = Tag.objects.create(name='Proper Noun', parent=_noun)
            # _cn = Tag.objects.create(name='Common Noun', parent=_noun)
            # _verb = Tag.objects.create(name='Verb', parent=_parts_of_speech)
            # _av = Tag.objects.create(name='Action Verb', parent=_verb)
            # _lv = Tag.objects.create(name='Linking Verb', parent=_verb)
            # _adjective = Tag.objects.create(name='Adjective', parent=_parts_of_speech)
            # _ca = Tag.objects.create(name='Comparative', parent=_adjective)
            # _sa = Tag.objects.create(name='Superlative', parent=_adjective)
            # _tenses = Tag.objects.create(name='Tenses', parent=_eng_lang)
            # _past = Tag.objects.create(name='Past', parent=_tenses)
            # _sp = Tag.objects.create(name='Simple Past', parent=_past)
            # _pc = Tag.objects.create(name='Past Continuous', parent=_past)
            # _present = Tag.objects.create(name='Present', parent=_tenses)
            # _spp = Tag.objects.create(name='Simple Present', parent=_present)
            # _pcp = Tag.objects.create(name='Present Continuous', parent=_present)
            # _future = Tag.objects.create(name='Future', parent=_tenses)
            # _sf = Tag.objects.create(name='Simple Future', parent=_future)
            # _fc = Tag.objects.create(name='Future Continuous', parent=_future)
            # _vocabulary = Tag.objects.create(name='Vocabulary', parent=_eng_lang)
            # _sv = Tag.objects.create(name='Synonyms', parent=_vocabulary)
            # _av = Tag.objects.create(name='Antonyms', parent=_vocabulary)
            # _grammar = Tag.objects.create(name='Grammar', parent=_eng_lang)
            # _ss = Tag.objects.create(name='Sentence Structure', parent=_grammar)
            # _pnc = Tag.objects.create(name='Punctuation', parent=_grammar)
            # _syntax = Tag.objects.create(name='Syntax', parent=_eng_lang)
            # _wo = Tag.objects.create(name='Word Order', parent=_syntax)
            # _st = Tag.objects.create(name='Sentence Types', parent=_syntax)

            _all_tags = list(Tag.objects.values_list('id', flat=True))
            results = []
            for _ in range(6):
                response = requests.get('https://opentdb.com/api.php?amount=50&difficulty=easy&type=multiple')
                results.extend(response.json().get('results'))
                time.sleep(10)

            for result in results:
                # _selected_tags = choices(_all_tags)
                _selected_tags = sample(_all_tags, randint(1, 3))
                _options = result.get('incorrect_answers')
                _correct_answer = result.get('correct_answer')
                _correct_answer_position = randint(0, 3)
                _options.insert(_correct_answer_position, _correct_answer)
                question = Question.objects.create(
                    question=result.get('question').replace('&quot;', "'").replace('&#039;', "'"),
                    correct_answer=_correct_answer_position + 1,
                    option_1=_options[0].replace('&quot;', "'").replace('&#039;', "'"),
                    option_2=_options[1].replace('&quot;', "'").replace('&#039;', "'"),
                    option_3=_options[2].replace('&quot;', "'").replace('&#039;', "'"),
                    option_4=_options[3].replace('&quot;', "'").replace('&#039;', "'"),
                )
                _passed_tags = Tag.objects.filter(pk__in=_selected_tags)
                _tags = []
                for t in _passed_tags:
                    while t:
                        _tags.append(t)
                        if not t.parent:
                            break
                        t = t.parent
                question.tags.set(list(set(_tags)))
        except Exception as e:
            ic(e)
