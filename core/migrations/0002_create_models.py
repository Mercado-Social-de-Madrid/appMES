import django.db.models.deletion
import helpers.filesystem
import imagekit.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Título')),
            ],
            options={
                'verbose_name': 'Galería',
                'verbose_name_plural': 'Galerías',
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('shortname', models.CharField(max_length=10)),
                ('latitude', models.FloatField(default=0, verbose_name='Latitud')),
                ('longitude', models.FloatField(default=0, verbose_name='Longitud')),
            ],
            options={
                'verbose_name': 'Mercado',
                'verbose_name_plural': 'Mercados',
            },
        ),
        migrations.CreateModel(
            name='GalleryPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, verbose_name='Orden')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Título')),
                ('photo', imagekit.models.fields.ProcessedImageField(upload_to=helpers.filesystem.RandomFileName('photos/'))),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('gallery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='core.gallery')),
            ],
            options={
                'verbose_name': 'Foto',
                'verbose_name_plural': 'Fotos',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manages_multi', models.BooleanField(default=False, verbose_name='Maneja entidades en más de un mercado')),
                ('preferred_locale', models.CharField(default='es-ES', max_length=10, verbose_name='Idioma preferido de la interfaz')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.market', verbose_name='Mercado que gestiona')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'permissions': (('mespermission_can_manage_users', 'Puede ver la lista de usuarios'), ('mespermission_can_change_passwords', 'Puede cambiar la contraseña de un usuario'), ('mespermission_can_view_user_history', 'Puede consultar el historial de un usuario'), ('mespermission_can_update_users', 'Puede modificar usuarios'), ('mespermission_can_view_user_detail', 'Puede ver los detalles de un usuario'), ('mespermission_can_create_users', 'Puede añadir usuarios')),
            },
        ),
    ]