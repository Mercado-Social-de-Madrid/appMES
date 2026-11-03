
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0016_remove_provider_num_workers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='city',
            new_name='old_city',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='address',
            new_name='old_address',
        ),
        migrations.AlterField(
            model_name='account',
            name='old_address',
            field=models.TextField(blank=True, null=True, verbose_name='Dirección (antigua)'),
        ),
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='account', to='core.address', verbose_name='Dirección'),
        ),
    ]
