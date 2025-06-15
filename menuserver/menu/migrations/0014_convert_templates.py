from django.db import migrations

def convert_templates(apps, schema_editor):
    MenuLink = apps.get_model('menu', 'MenuLink')
    MenuTemplate = apps.get_model('menu', 'MenuTemplate')
    
    # Create default templates
    templates = {
        'classic': {
            'name': 'Classic',
            'description': 'Traditional menu layout',
            'template_file': 'classic.html'
        },
        'modern': {
            'name': 'Modern',
            'description': 'Contemporary design',
            'template_file': 'modern.html'
        },
        'minimal': {
            'name': 'Minimal',
            'description': 'Clean and simple',
            'template_file': 'minimal.html'
        }
    }
    
    # Create template records
    template_objects = {}
    for key, data in templates.items():
        template = MenuTemplate.objects.create(
            name=data['name'],
            description=data['description'],
            template_file=data['template_file']
        )
        template_objects[key] = template
    
    # Update MenuLink records
    for menu_link in MenuLink.objects.all():
        if menu_link.template in template_objects:
            menu_link.template = template_objects[menu_link.template]
            menu_link.save()

def reverse_convert(apps, schema_editor):
    MenuLink = apps.get_model('menu', 'MenuLink')
    MenuTemplate = apps.get_model('menu', 'MenuTemplate')
    
    # Convert back to old format
    for menu_link in MenuLink.objects.all():
        if menu_link.template:
            menu_link.template = menu_link.template.template_file.replace('.html', '')
            menu_link.save()

class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0013_menutemplate_alter_menulink_template'),
    ]

    operations = [
        migrations.RunPython(convert_templates, reverse_convert),
    ] 