from django.core.management.base import BaseCommand
from menu.models import MenuTemplate
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates default menu templates'

    def handle(self, *args, **kwargs):
        templates = [
            {
                'name': 'Classic',
                'template_file': 'classic.html',
                'description': 'A traditional layout with elegant design, perfect for fine dining restaurants.',
                'thumbnail': 'classic.jpg'
            },
            {
                'name': 'Modern',
                'template_file': 'modern.html',
                'description': 'A contemporary design with dynamic layout, ideal for trendy cafes and bistros.',
                'thumbnail': 'modern.jpg'
            },
            {
                'name': 'Minimal',
                'template_file': 'minimal.html',
                'description': 'A clean and simple design that focuses on your menu items, great for casual dining.',
                'thumbnail': 'minimal.jpg'
            }
        ]

        for template_data in templates:
            template, created = MenuTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    'template_file': template_data['template_file'],
                    'description': template_data['description'],
                    'is_active': True
                }
            )

            if created:
                # Set thumbnail if it exists
                thumbnail_path = os.path.join(settings.STATIC_ROOT, 'menu', 'images', 'templates', template_data['thumbnail'])
                if os.path.exists(thumbnail_path):
                    with open(thumbnail_path, 'rb') as f:
                        template.thumbnail.save(template_data['thumbnail'], File(f), save=True)
                
                self.stdout.write(self.style.SUCCESS(f'Successfully created template "{template.name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Template "{template.name}" already exists')) 