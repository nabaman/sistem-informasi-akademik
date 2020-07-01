from django.db import models
from datetime import datetime
from sequences import get_next_value
from kbm.models import Data_Kelas
from django.contrib.auth.models import User
from tahun_ajaran.models import Data_Tahun_Ajaran

# Create your models here.


class Data_Siswa(models.Model):

      pilihan_jk = (
          ('Laki-Laki', 'Laki-Laki'),
          ('Perempuan','Perempuan'),
      )
      user                = models.OneToOneField(User,blank=True, limit_choices_to={'groups__name': "siswa"},null=True, on_delete=models.CASCADE)
      nis                 = models.IntegerField(null=True, unique=True)
      nisn                = models.IntegerField(null=True, unique=True)
      nama                = models.CharField(max_length=50, null=True)
      kelas               = models.ForeignKey(Data_Kelas, null=True, on_delete=models.SET_NULL)
      tgl_lahir           = models.DateField(null=True)
      alamat              = models.CharField(max_length=255, null=True, blank=True)
      jenis_kelamin       = models.CharField(max_length=30, choices=pilihan_jk, null=True)
      sekolah_sebelumnya  = models.CharField(max_length=50)
      foto                = models.ImageField(default='profil.png', null=True, blank=True)



      def __str__(self):
          return self.nama

      def save(self):
            if not self.id:
                  thn_ajaran = Data_Tahun_Ajaran.objects.filter(tahun=datetime.now().year).order_by('-id')[0]
                  x = Data_Siswa.objects.all().order_by('-id')[0]
                  generate_nis = str(datetime.now().year)+'0000'

                  self.nis = int(generate_nis) + int(get_next_value(str(thn_ajaran.tahun)))
            super(Data_Siswa,self).save()
