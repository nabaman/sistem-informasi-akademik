from django.db import models
from django.contrib.auth.models import User
from guru.models import Data_Guru,Data_Mapel
# Create your models here.
from tahun_ajaran.models import Data_Tahun_Ajaran

class Data_Jurusan(models.Model):
      kd_jurusan = models.CharField(max_length=5, null=True)
      jurusan = models.CharField(max_length=30, null=True)

      def __str__(self):
          return self.jurusan



class Data_Kelas(models.Model):
      list_kelas = (
        ('X ( Sepuluh )', 'X ( Sepuluh )'),
        ('XI ( Sebelas )', 'XI ( Sebelas )'),
        ('XII ( Dua Belas )', 'XII ( Dua Belas )'),
      )
      list_ruang = (
          ('1','1'),
          ('2','2'),
          ('3','3'),
          ('4','4'),
          ('5','5')
      )
      kelas = models.CharField(max_length=20, choices=list_kelas , null=True)
      jurusan = models.ForeignKey(Data_Jurusan, null=True, on_delete=models.CASCADE)
      ruang = models.CharField(max_length=3, choices=list_ruang,null=True)
      wali_kelas = models.OneToOneField(Data_Guru, null=True, on_delete=models.SET_NULL, blank=True)
      def __str__(self):
          return '{} - {} - {}'.format(self.kelas, self.jurusan, self.ruang)




class Data_Jadwal(models.Model):
      daftar_hari = (
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ("Jum'at", "Jum'at"),
        ('Sabtu', 'Sabtu'),
      )

      pilihan_jam = (
          ('12.30 - 13.30','12.30 - 13.30'),
          ('13.30 - 14.30','13.30 - 14.30'),
          ('12.30 - 14.30','12.30 - 14.30'),
          ('14.30 - 15.30','14.30 - 15.30'),
          ('16.00 - 17.00','16.00 - 17.00'),
      )

      tahun_ajaran = models.ForeignKey(Data_Tahun_Ajaran, on_delete=models.CASCADE, null=True)
      hari = models.CharField(max_length=20, choices=daftar_hari, null=True)
      kelas = models.ForeignKey(Data_Kelas, null=True, on_delete=models.CASCADE)
      mapel = models.ForeignKey(Data_Mapel, null=True, on_delete=models.CASCADE)
      jam = models.CharField(max_length=15, choices=pilihan_jam, null=True)
      guru = models.ForeignKey(Data_Guru, null=True, on_delete=models.CASCADE)







      def __str__(self):
           return "{} - {} - {} - oleh {}".format(self.hari, self.kelas, self.mapel, self.guru)
      class Meta:
          ordering=['-hari','jam']


