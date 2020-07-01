from .models import Bulan_Pembayaran,Jenis_Pembayaran,Data_Pembayaran_SPP,Data_Pembayaran_UTS,Data_Pembayaran_UAS,Data_Nilai
from siswa.models import Data_Siswa
from django.contrib.auth.models import User,Group
from django.db.models import Q
from guru.models import Data_Mapel, Data_Guru
from django.db.models.signals import post_save
from tahun_ajaran.models import Data_Tahun_Ajaran
from datetime import datetime


def create_user_siswa(sender, instance,created,**kwargs):
    if created:
        pwd = instance.tgl_lahir
        User.objects.create_user(
            username=instance.nis,
            password=pwd.strftime('%m%d%Y')
        )
        user = User.objects.get(username=instance.nis)
        group_siswa = Group.objects.get(name='siswa')
        group_siswa.user_set.add(user)
        siswa = Data_Siswa.objects.get(nis=instance.nis)
        siswa.user = user
        siswa.save()

post_save.connect(create_user_siswa, sender=Data_Siswa)

def create_user_guru(sender, instance,created,**kwargs):
    if created:
        pwd = instance.tgl_lahir
        User.objects.create_user(
            username=instance.nip,
            password=pwd.strftime('%m%d%Y')
        )
        user = User.objects.get(username=instance.nip)
        group_guru = Group.objects.get(name='guru')
        group_guru.user_set.add(user)
        guru = Data_Guru.objects.get(nip=instance.nip)
        guru.user = user
        guru.save()

post_save.connect(create_user_guru, sender=Data_Guru)

def create_pembayaran_spp(sender ,instance ,created ,**kwargs):
    if created:
        for bln in Bulan_Pembayaran.objects.all()[:6]:
            Data_Pembayaran_SPP.objects.create(
                bulan=bln,
                jenis_pembayaran=Jenis_Pembayaran.objects.get(jenis_pembayaran='SPP'),
                siswa=instance,
                status='Belum Lunas',
                tahun_ajaran=Data_Tahun_Ajaran.objects.all().first()
            )
        for bln in Bulan_Pembayaran.objects.all()[6:12]:
            Data_Pembayaran_SPP.objects.create(
                bulan=bln,
                jenis_pembayaran=Jenis_Pembayaran.objects.get(jenis_pembayaran='SPP'),
                siswa=instance,
                status='Belum Lunas',
                tahun_ajaran=Data_Tahun_Ajaran.objects.all().last()
            )
post_save.connect(create_pembayaran_spp, sender=Data_Siswa)

def create_pembayaran_uts(sender, instance, created, **kwargs):
    if created:
        for thn in Data_Tahun_Ajaran.objects.filter(tahun=datetime.now().year):
            Data_Pembayaran_UTS.objects.create(
                jenis_pembayaran=Jenis_Pembayaran.objects.get(jenis_pembayaran='UTS'),
                siswa=instance,
                status='Belum Lunas',
                tahun_ajaran=thn
            )
post_save.connect(create_pembayaran_uts, sender=Data_Siswa)


def create_pembayaran_uas(sender, instance, created, **kwargs):
    if created:
        for thn in Data_Tahun_Ajaran.objects.filter(tahun=datetime.now().year):
            Data_Pembayaran_UAS.objects.create(
                jenis_pembayaran=Jenis_Pembayaran.objects.get(jenis_pembayaran='UAS'),
                siswa=instance,
                status='Belum Lunas',
                tahun_ajaran=thn
            )

post_save.connect(create_pembayaran_uas, sender=Data_Siswa)

def create_nilai(sender ,instance ,created ,**kwargs):
    if created:
        for thn in Data_Tahun_Ajaran.objects.filter(tahun=datetime.now().year):
            for mpl in Data_Mapel.objects.filter(Q(jenis='UMUM') | Q(jenis=instance.kelas.jurusan.kd_jurusan)):
                Data_Nilai.objects.create(
                    wali_kelas=instance.kelas.wali_kelas ,
                    mapel=mpl,
                    siswa=instance,
                    tugas=0,
                    uts=0,
                    uas=0,
                    tahun_ajaran = thn
                )
            print('Data Pembayaran Dibuat')

post_save.connect(create_nilai, sender=Data_Siswa)




