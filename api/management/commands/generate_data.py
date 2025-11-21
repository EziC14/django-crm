from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from faker import Faker
import random
from datetime import timedelta

from api.models import Company, Customer, Interaction


class Command(BaseCommand):
    help = 'Generate fake data: users, companies, customers and interactions'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=3)
        parser.add_argument('--companies', type=int, default=50)
        parser.add_argument('--customers', type=int, default=1000)
        parser.add_argument('--interactions-per-customer', type=int, default=500)

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()
        users_n = options['users']
        companies_n = options['companies']
        customers_n = options['customers']
        interactions_per = options['interactions_per_customer']

        self.stdout.write('Generating users...')
        users = []
        for i in range(users_n):
            u = User.objects.create_user(username=f'sales{i+1}', password='password')
            users.append(u)

        self.stdout.write('Generating companies...')
        companies = []
        for i in range(companies_n):
            c = Company.objects.create(name=fake.company())
            companies.append(c)

        self.stdout.write(f'Generating {customers_n} customers...')
        customers = []
        for i in range(customers_n):
            fn = fake.first_name()
            ln = fake.last_name()
            company = random.choice(companies)
            sales = random.choice(users)
            bday = fake.date_of_birth(minimum_age=18, maximum_age=80)
            customers.append(Customer(first_name=fn, last_name=ln, company=company, sales_rep=sales, birthday=bday))
        Customer.objects.bulk_create(customers, batch_size=1000)

        all_customers = list(Customer.objects.all())

        self.stdout.write(f'Generating interactions: ~{len(all_customers)*interactions_per} total...')

        types = [t[0] for t in Interaction.TYPE_CHOICES]
        batch = []
        CHUNK = 5000
        created = 0
        start_time = timezone.now()
        for idx, cust in enumerate(all_customers):
            # generate interactions_per interactions per customer
            for k in range(interactions_per):
                days_ago = random.randint(0, 365 * 3)
                ts = timezone.now() - timedelta(days=days_ago, seconds=random.randint(0, 86400))
                tp = random.choice(types)
                batch.append(Interaction(customer=cust, sales_rep=cust.sales_rep, interaction_type=tp, timestamp=ts, notes=''))
                if len(batch) >= CHUNK:
                    Interaction.objects.bulk_create(batch, batch_size=CHUNK)
                    created += len(batch)
                    batch = []
                    self.stdout.write(f'Created {created} interactions so far...')

        if batch:
            Interaction.objects.bulk_create(batch, batch_size=CHUNK)
            created += len(batch)

        elapsed = timezone.now() - start_time
        self.stdout.write(self.style.SUCCESS(f'Finished: created {created} interactions in {elapsed}'))
