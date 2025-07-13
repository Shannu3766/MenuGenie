from django.core.management.base import BaseCommand
from menu.models import MenuTemplate
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Initialize default menu templates'

    def handle(self, *args, **options):
        self.stdout.write('Initializing default templates...')
        
        # Create templates directory if it doesn't exist
        template_dir = os.path.join(settings.BASE_DIR, 'menu', 'templates', 'menu', 'templates')
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        
        # Create default template
        default_template, created = MenuTemplate.objects.get_or_create(
            name='Default Template',
            defaults={
                'description': 'A clean and modern template with a focus on readability',
                'template_file': 'templates/default.html'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created default template'))
        
        # Create modern template
        modern_template, created = MenuTemplate.objects.get_or_create(
            name='Modern Template',
            defaults={
                'description': 'A contemporary template with a full-width hero section',
                'template_file': 'templates/modern.html'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created modern template'))
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized templates')) 