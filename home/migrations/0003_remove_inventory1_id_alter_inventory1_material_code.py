# Generated by Django 4.1 on 2022-09-08 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_inventory1_id_alter_inventory1_material_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory1',
            name='id',
        ),
        migrations.AlterField(
            model_name='inventory1',
            name='material_code',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]