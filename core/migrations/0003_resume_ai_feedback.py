from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='analysis_summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='improvement_suggestions',
            field=models.TextField(blank=True),
        ),
    ]
