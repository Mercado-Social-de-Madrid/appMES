# Generated by Django 5.0 on 2024-07-23 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_remove_provider_phone_number_account_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_ca',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_es',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_eu',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_gl',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ca',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_es',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_eu',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_gl',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='provider',
            name='description_ca',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='provider',
            name='description_es',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='provider',
            name='description_eu',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='provider',
            name='description_gl',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='provider',
            name='legal_form_ca',
            field=models.TextField(blank=True, null=True, verbose_name='Forma legal'),
        ),
        migrations.AddField(
            model_name='provider',
            name='legal_form_es',
            field=models.TextField(blank=True, null=True, verbose_name='Forma legal'),
        ),
        migrations.AddField(
            model_name='provider',
            name='legal_form_eu',
            field=models.TextField(blank=True, null=True, verbose_name='Forma legal'),
        ),
        migrations.AddField(
            model_name='provider',
            name='legal_form_gl',
            field=models.TextField(blank=True, null=True, verbose_name='Forma legal'),
        ),
        migrations.AddField(
            model_name='provider',
            name='name_ca',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='provider',
            name='name_es',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='provider',
            name='name_eu',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='provider',
            name='name_gl',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='provider',
            name='short_description_ca',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción corta'),
        ),
        migrations.AddField(
            model_name='provider',
            name='short_description_es',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción corta'),
        ),
        migrations.AddField(
            model_name='provider',
            name='short_description_eu',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción corta'),
        ),
        migrations.AddField(
            model_name='provider',
            name='short_description_gl',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción corta'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='legal_form',
            field=models.TextField(blank=True, null=True, verbose_name='Forma legal'),
        ),
    ]
