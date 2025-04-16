from django.core.management.base import BaseCommand
from account.models import Account
from property.models import Visit
from django.utils.timezone import make_aware
from faker import Faker

class Command(BaseCommand):
    help = 'Genera 300,000 visitas aleatorias para un usuario'

    def handle(self, *args, **kwargs):
        fake = Faker()

        user = Account.objects.get(user__username='userPrueba')

        self.stdout.write("⏳ Generando visitas aleatorias...")

        visitas = [
            Visit(
                visited_user=user,
                date=make_aware(fake.date_time_this_century())
            ) for _ in range(300000)
        ]

        Visit.objects.bulk_create(visitas, batch_size=5000)

        self.stdout.write(self.style.SUCCESS("✅ 300,000 visitas creadas exitosamente."))
