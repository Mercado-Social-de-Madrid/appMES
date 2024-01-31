# Generated by Django 5.0 on 2024-01-25 12:08

import authentication.models.user
import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('first_name', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Nombre')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Apellidos')),
                ('manages_multi', models.BooleanField(default=False, verbose_name='Maneja entidades en más de un mercado')),
                ('preferred_locale', models.CharField(default='es-ES', max_length=10, verbose_name='Idioma preferido de la interfaz')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.node', verbose_name='Mercado que gestiona')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'permissions': (('mespermission_can_manage_users', 'Puede ver la lista de usuarios'), ('mespermission_can_change_passwords', 'Puede cambiar la contraseña de un usuario'), ('mespermission_can_view_user_history', 'Puede consultar el historial de un usuario'), ('mespermission_can_update_users', 'Puede modificar usuarios'), ('mespermission_can_view_user_detail', 'Puede ver los detalles de un usuario'), ('mespermission_can_create_users', 'Puede añadir usuarios')),
            },
            managers=[
                ('objects', authentication.models.user.UserManager()),
            ],
        ),
    ]