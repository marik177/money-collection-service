import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from collection_project.money_collections.models import Collection, Occasion, Payment
from collection_project.users.models import BaseUser


def create_users(fake):
    users = [
        BaseUser(email=fake.email(), password="password", first_name=fake.first_name(), last_name=fake.last_name())
        for i in range(10)
    ]
    BaseUser.objects.bulk_create(users)


def create_occasions():
    occasions_name = [
        "День рождения",
        "Свадьба",
        "Юбилей",
        "Новый год",
        "Благотворительность",
        "Новоселье",
    ]
    occasions = [Occasion(name=occasion) for occasion in occasions_name]
    Occasion.objects.bulk_create(occasions, ignore_conflicts=True)


def create_payments():
    users = BaseUser.objects.all()
    collections = Collection.objects.all()
    payments = []
    for _ in range(1000):
        contributor = random.choice(users)
        collect = random.choice(collections)
        payments.append(
            Payment(
                collection=collect,
                contributor=contributor,
                amount=random.randint(10, 100),
            )
        )
    Payment.objects.bulk_create(payments)


def create_collections_and_payments(fake):
    users = BaseUser.objects.all()
    occasions = Occasion.objects.all()
    collections = []
    for occasion in occasions:
        author = random.choice(users)
        collect = Collection(
            author=author,
            title=fake.job(),
            occasion=occasion,
            description=fake.text(),
            planned_amount=random.randint(100, 1000),
            cover_image=f"collection_covers/cover{fake.random_int(min=0, max=9999)}.jpg",
            end_collection_date=timezone.now() + timedelta(days=random.randint(1, 30)),
        )
        collections.append(collect)
    Collection.objects.bulk_create(collections, batch_size=50)


class Command(BaseCommand):
    help = "Fill the database with mock data"

    def handle(self, *args, **options):
        fake = Faker()

        create_users(fake)
        create_occasions()
        create_collections_and_payments(fake)
        create_payments()

        self.stdout.write(self.style.SUCCESS("Mock data has been successfully added to the database."))
