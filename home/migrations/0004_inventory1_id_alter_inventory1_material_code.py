# Generated by Django 4.1 on 2022-09-08 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_inventory1_id_alter_inventory1_material_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory1',
            name='id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='inventory1',
            name='material_code',
            field=models.CharField(max_length=100),
        ),
    ]