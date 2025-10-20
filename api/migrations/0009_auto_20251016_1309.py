from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
    ('api', '0008_task_completed'),
]
    
    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
