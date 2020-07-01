from django.db import models

# Create your models here.
class Data_Tahun_Ajaran(models.Model):
    daftar_semester = (
        ('GANJIL', 'GANJIL'),
        ('GENAP', 'GENAP')
    )

    tahun = models.IntegerField(null=True)
    semester = models.CharField(max_length=30, choices=daftar_semester, null=True)

    def __str__(self):
        return '{}/{}'.format(self.tahun, self.semester)