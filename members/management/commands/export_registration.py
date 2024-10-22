import csv
from django.core.management.base import BaseCommand
from members.models import Registration

class Command(BaseCommand):
    help = 'Exports registration data to CSV'

    def handle(self, *args, **kwargs):
        file_name = 'registrations.csv'
        with open(file_name, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['First Name', 'Last Name', 'Gender', 'Phone Number', 'Residence', 'Occupation', 'Date Registered'])
            
            # Query all registrations
            registrations = Registration.objects.all()

            for registration in registrations:
                writer.writerow([registration.first_name, registration.last_name, registration.gender, 
                                 registration.phone_number, registration.residence, registration.occupation, 
                                 registration.date_registered])

        self.stdout.write(self.style.SUCCESS(f'Successfully exported registrations to {file_name}'))
