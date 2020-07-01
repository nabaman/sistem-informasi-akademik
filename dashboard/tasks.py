from SIA.celery import app
from absen.models import Data_Absen_Siswa,Status
from siswa.models import Data_Siswa
from tahun_ajaran.models import Data_Tahun_Ajaran
from datetime import datetime

@app.task
def create_absen_ganjil():
    for siswa in Data_Siswa.objects.all():
        Data_Absen_Siswa.objects.create(
            siswa=siswa,
            status = Status.objects.get(id=2),
            tahun_ajaran= Data_Tahun_Ajaran.objects.filter(tahun=datetime.now().year).get(semester='GANJIL')
        )

def create_absen_genap():
    for siswa in Data_Siswa.objects.all():
        Data_Absen_Siswa.objects.create(
            siswa=siswa,
            status = Status.objects.get(id=2),
            tahun_ajaran= Data_Tahun_Ajaran.objects.filter(tahun=datetime.now().year).get(semester='GANJIL')
        )



