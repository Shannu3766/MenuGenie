from django.db import migrations, models
import django.db.models.deletion

def remove_templates(apps, schema_editor):
    MenuLink = apps.get_model('menu', 'MenuLink')
    # Delete any MenuLink records that don't have a restaurant
    MenuLink.objects.filter(restaurant__isnull=True).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0017_alter_restaurant_image'),
    ]

    operations = [
        # First, remove the template field
        migrations.RemoveField(
            model_name='menulink',
            name='template',
        ),
        # Then, make the restaurant field non-nullable
        migrations.AlterField(
            model_name='menulink',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.restaurant'),
        ),
        # Finally, remove the MenuTemplate model
        migrations.DeleteModel(
            name='MenuTemplate',
        ),
        # Run the data migration to clean up any invalid records
        migrations.RunPython(remove_templates),
    ] 