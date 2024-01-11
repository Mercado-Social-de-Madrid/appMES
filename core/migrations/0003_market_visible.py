from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_create_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='visible',
            field=models.BooleanField(default=False, help_text='Por defecto, un nuevo mercado empieza oculto hasta que esté listo para incluir en la aplicación', verbose_name='Visible en listado público'),
        ),
    ]
