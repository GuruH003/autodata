from django.contrib.auth.models import User
from api.models import Job
from django.core.management.base import BaseCommand
import csv
from datetime import  date

class Command(BaseCommand):
    help = 'Description of your script'

    def handle(self, *args, **options):
        file_path = 'C:/Users/LENOVO/Downloads/user_id_with_username.csv'
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['User ID', 'Username']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            start_date = date(2024, 4, 28)
            end_date = date(2024, 5, 4)
            
            users = User.objects.all()
            for user in users:
                # jobs = Job.objects.filter(createdBy=user.id, createdAt__range=(start_date, end_date))
                # for job in jobs:
                    writer.writerow({'User ID': user.id, 'Username': user.username,})

                    # self.stdout.write(f"{job.serverJobId} {user.username} {job.createdAt}")
        self.stdout.write(self.style.SUCCESS(f"Output saved to {file_path}"))
