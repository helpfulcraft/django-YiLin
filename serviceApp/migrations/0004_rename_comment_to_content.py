from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('serviceApp', '0003_alter_servicereview_service'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicereview',
            old_name='comment',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='servicereview',
            old_name='created_time',
            new_name='created_at',
        ),
    ]
