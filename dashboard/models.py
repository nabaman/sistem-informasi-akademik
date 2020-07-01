import uuid
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from guru.models import Data_Guru, Data_Mapel, Data_Staff
from siswa.models import Data_Siswa
from tahun_ajaran.models import Data_Tahun_Ajaran
from datetime import datetime
# Create your models here.


class Data_Nilai(models.Model):
    wali_kelas = models.ForeignKey(
        Data_Guru, on_delete=models.CASCADE, null=True)
    mapel = models.ForeignKey(Data_Mapel, on_delete=models.CASCADE, null=True)
    siswa = models.ForeignKey(Data_Siswa, on_delete=models.CASCADE, null=True)
    tugas = models.CharField(max_length=3)
    uts = models.CharField(max_length=3)
    uas = models.CharField(max_length=3)
    keterampilan = models.CharField(max_length=3, default=0)
    tahun_ajaran = models.ForeignKey(
        Data_Tahun_Ajaran, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Nilai {}: {} ".format(self.mapel, self.siswa)

    def total_nilai(self):
        pengetahuan = (float(self.tugas)*(20/100)) + \
            (float(self.uts)*(30/100)) + (float(self.uas)*(50/100))
        return round((float(pengetahuan) + float(self.keterampilan)) / 2)
    
    def predikat(self):
        if self.total_nilai() <=100 and self.total_nilai() >=90:
            return "A"
        if self.total_nilai() <90 and self.total_nilai() >=80:
            return "B"
        if self.total_nilai() <80 and self.total_nilai() >=70:
            return "C"
        if self.total_nilai() <70 and self.total_nilai() >=60:
            return "D"
        if self.total_nilai() <60 and self.total_nilai() >=50:
            return "E"


class Bulan_Pembayaran(models.Model):
    bulan = models.CharField(max_length=255)

    def __str__(self):
        return self.bulan


class Jenis_Pembayaran(models.Model):
    jenis_pembayaran = models.CharField(max_length=100)
    tagihan = models.PositiveIntegerField()

    def __str__(self):
        return self.jenis_pembayaran


class Data_Pembayaran_SPP(models.Model):
    pil_stat = (
        ('Lunas', 'Lunas'),
        ('Belum Lunas', 'Belum Lunas')
    )
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    jenis_pembayaran = models.ForeignKey(Jenis_Pembayaran, limit_choices_to={
        'jenis_pembayaran': "SPP"}, on_delete=models.CASCADE, null=True)
    bulan = models.ForeignKey(Bulan_Pembayaran, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Data_Siswa, on_delete=models.CASCADE)
    status = models.CharField(
        choices=pil_stat, max_length=255, default='Belum Lunas')
    tahun_ajaran = models.ForeignKey(
        Data_Tahun_Ajaran, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['siswa', 'bulan']

    def __str__(self):
        return "{} . {} . {} ".format(self.siswa, self.bulan, self.status)


class Data_Pembayaran_UAS(models.Model):
    pil_stat = (
        ('Lunas', 'Lunas'),
        ('Belum Lunas', 'Belum Lunas')
    )
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    jenis_pembayaran = models.ForeignKey(Jenis_Pembayaran, limit_choices_to={
        'jenis_pembayaran': "UAS"}, on_delete=models.CASCADE, null=True)
    siswa = models.ForeignKey(Data_Siswa, on_delete=models.CASCADE)
    status = models.CharField(
        choices=pil_stat, max_length=255, default='Belum Lunas')
    tahun_ajaran = models.ForeignKey(
        Data_Tahun_Ajaran, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['siswa']

    def __str__(self):
        return "{} . {} . {} ".format(self.siswa, self.jenis_pembayaran, self.status)


class Data_Pembayaran_UTS(models.Model):
    pil_stat = (
        ('Lunas', 'Lunas'),
        ('Belum Lunas', 'Belum Lunas')
    )
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    jenis_pembayaran = models.ForeignKey(Jenis_Pembayaran, limit_choices_to={
        'jenis_pembayaran': "UTS"}, on_delete=models.CASCADE, null=True)
    siswa = models.ForeignKey(Data_Siswa, on_delete=models.CASCADE)
    status = models.CharField(
        choices=pil_stat, max_length=255, default='Belum Lunas')
    tahun_ajaran = models.ForeignKey(
        Data_Tahun_Ajaran, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['siswa']

    def __str__(self):
        return "{} . {} . {} ".format(self.siswa, self.jenis_pembayaran, self.status)
