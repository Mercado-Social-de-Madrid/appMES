# Generated by Django 4.1.5 on 2023-01-31 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIToken',
            fields=[
            ],
            options={
                'verbose_name': 'API Token',
                'verbose_name_plural': 'API Tokens',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('authtoken.tokenproxy',),
        )
    ]
