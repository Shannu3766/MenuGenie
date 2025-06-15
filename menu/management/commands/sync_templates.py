from django.core.management.base import BaseCommand
from menu.utils import sync_templates

class Command(BaseCommand):
    help = 'Synchronizes available menu templates with the database'

    def handle(self, *args, **options):
        self.stdout.write('Starting template synchronization...')
        sync_templates()
        self.stdout.write(self.style.SUCCESS('Successfully synchronized templates')) 