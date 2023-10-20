# Generated by Django 4.2.6 on 2023-10-18 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactoEmergencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
                ('parentesco', models.CharField(max_length=50)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contactos_emergencia', to='pacientes.paciente')),
            ],
        ),
    ]
