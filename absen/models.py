from django.db import models
from guru.models import *
from siswa.models import *
from tahun_ajaran.models import Data_Tahun_Ajaran
# Create your models here.

class Status(models.Model):
    status = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.status

class Data_Absen_Guru(models.Model):
    guru = models.ForeignKey(Data_Guru, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    jam = models.DateTimeField(auto_now_add=True)
    tahun_ajaran = models.ForeignKey(Data_Tahun_Ajaran, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}".format(self.guru)

class Data_Absen_Siswa(models.Model):
    siswa = models.ForeignKey(Data_Siswa, null=True, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    jam = models.DateTimeField(auto_now_add=True)
    tahun_ajaran = models.ForeignKey(Data_Tahun_Ajaran, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}".format(self.siswa)


