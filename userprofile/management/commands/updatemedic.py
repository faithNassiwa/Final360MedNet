from django.core.management import BaseCommand
from userprofile.models import Record


class Command(BaseCommand):
    def handle(self, *args, **options):
        added = Record.get_record_file()
        self.stdout.write(self.style.SUCCESS('Successfully added  %s medics ' % added))
