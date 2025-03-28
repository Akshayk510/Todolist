# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10),
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(blank=True, choices=[('work', 'Work'), ('personal', 'Personal'), ('health', 'Health'), ('education', 'Education'), ('finance', 'Finance'), ('home', 'Home'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]