# Generated by Django 5.0.3 on 2024-03-12 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CRMContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_id', models.IntegerField()),
                ('phone', models.CharField(max_length=255)),
            ],
        ),
    ]
