from django.db import migrations

def update_template_references(apps, schema_editor):
    MenuLink = apps.get_model('menu', 'MenuLink')
    MenuTemplate = apps.get_model('menu', 'MenuTemplate')
    
    # Map old template names to new template files
    template_map = {
        'classic': 'classic.html',
        'modern': 'modern.html',
        'minimal': 'minimal.html'
    }
    
    # Update each MenuLink
    for menu_link in MenuLink.objects.all():
        if menu_link.old_template in template_map:
            template = MenuTemplate.objects.get(template_file=template_map[menu_link.old_template])
            menu_link.template = template
            menu_link.save()

def reverse_update(apps, schema_editor):
    MenuLink = apps.get_model('menu', 'MenuLink')
    
    for menu_link in MenuLink.objects.all():
        if menu_link.template:
            menu_link.old_template = menu_link.template.template_file.replace('.html', '')
            menu_link.save()

class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0013_menutemplate_alter_menulink_template'),
    ]

    operations = [
        migrations.RunPython(update_template_references, reverse_update),
    ] 
