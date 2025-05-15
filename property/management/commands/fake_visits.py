from django.core.management.base import BaseCommand
from account.models import Account
from property.models import Visit
from django.utils.timezone import make_aware
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Genera 300,000 visitas aleatorias para un usuario con sesgos en 2024 (hasta hoy), septiembre y jueves'

    def handle(self, *args, **kwargs):
        fake = Faker()
        user = Account.objects.get(user__username='userPrueba')

        self.stdout.write("⏳ Generando visitas aleatorias sesgadas...")

        now = datetime.now()
        start_date_2019 = datetime(2019, 1, 1)
        start_date_2024 = datetime(2024, 1, 1)
        end_date_2023 = datetime(2023, 12, 31, 23, 59, 59)
        end_date_2024 = now if now.year == 2024 else datetime(2024, 12, 31, 23, 59, 59)

        visitas = []

        for _ in range(300000):
            # 80% de probabilidad de que la fecha sea en 2024
            if random.random() < 0.8:
                # Fecha entre 2024-01-01 y hoy (o fin de 2024 si ya pasó)
                date = fake.date_time_between(start_date=start_date_2024, end_date=end_date_2024)
                # Sesgo: repetir si no cae en septiembre o jueves con mayor probabilidad
                for _ in range(3):  # Hasta 3 intentos de sesgo
                    month = date.month
                    weekday = date.weekday()
                    month_weight = 5 if month == 9 else 1
                    weekday_weight = 6 if weekday == 3 else 1
                    combined_weight = month_weight + weekday_weight
                    if random.random() < (combined_weight / 10):
                        break
                    # Si no pasa el sesgo, genera otra fecha
                    date = fake.date_time_between(start_date=start_date_2024, end_date=end_date_2024)
            else:
                # Fecha entre 2019-01-01 y 2023-12-31
                date = fake.date_time_between(start_date=start_date_2019, end_date=end_date_2023)

            visitas.append(
                Visit(
                    visited_user=user,
                    date=make_aware(date)
                )
            )

        Visit.objects.bulk_create(visitas, batch_size=5000)
        self.stdout.write(self.style.SUCCESS("✅ 300,000 visitas sesgadas creadas exitosamente."))
