# Generated by Django 3.0.5 on 2020-06-29 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_data_nilai_keterampilan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_nilai',
            name='keterampilan',
            field=models.CharField(default=0, max_length=3),
        ),
    ]