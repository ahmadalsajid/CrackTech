from icecream import ic
from django.core.management.base import BaseCommand
from users.models import Student, User
from faker import Faker
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Creates teachers, students, & courses non-interactively"

    def handle(self, *args, **options):
        try:
            fake = Faker()
        except Exception as e:
            ic(e)
