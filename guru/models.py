from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Data_Mapel(models.Model):
    jenis_mapel = (
        ('UMUM', 'UMUM'),
        ('AP', 'AP'),
        ('TKJ', 'TKJ')
    )
    kd_mapel = models.CharField(max_length=6, null=True, unique=True)
    nama_mapel = models.CharField(max_length=50, null=True)
    bobot = models.PositiveSmallIntegerField(null=True)
    jenis = models.CharField(max_length=10, choices=jenis_mapel, null=True)
    kkm = models.CharField(max_length=2, null=True)

    def __str__(self):
        return '{}'.format(self.nama_mapel)


class Data_Guru(models.Model):
    pilihan_jk = (
        ('Laki-Laki', 'Laki-Laki'),
        ('Perempuan', 'Perempuan'),
    )

    user = models.OneToOneField(User, limit_choices_to={
                                'groups__name': "guru"}, null=True, on_delete=models.CASCADE, blank=True)
    nip = models.IntegerField(null=True, unique=True)
    nama = models.CharField(max_length=255, null=True)
    jenis_kelamin = models.CharField(
        max_length=20, choices=pilihan_jk, null=True)
    tgl_lahir = models.DateField()
    alamat = models.CharField(max_length=255, null=True)
    foto = models.ImageField(default='profile.png', null=True, blank=True)

    def __str__(self):
        return self.nama


class Data_Staff(models.Model):
    user = models.OneToOneField(User, limit_choices_to={
                                'groups__name': "staff_tu"}, on_delete=models.CASCADE,)
    nip = models.IntegerField(null=True, unique=True)
    nama = models.CharField(max_length=255, null=True)
    tgl_lahir = models.DateField()
    alamat = models.CharField(max_length=255, null=True)
    foto = models.ImageField(default='profile.png', null=True, blank=True)
    mapel = models.ManyToManyField(Data_Mapel, blank=True)

    def __str__(self):
        return self.nama
