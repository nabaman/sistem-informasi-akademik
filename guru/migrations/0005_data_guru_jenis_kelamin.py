# Generated by Django 3.0.5 on 2020-06-28 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0004_remove_data_guru_mapel'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_guru',
            name='jenis_kelamin',
            field=models.CharField(choices=[('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')], max_length=20, null=True),
        ),
    ]