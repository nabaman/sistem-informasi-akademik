import django_filters
from django_filters import CharFilter, ModelChoiceFilter

from siswa.models import *
from kbm.models import *
from .models import *


class MuridFilter(django_filters.FilterSet):
    nama = django_filters.CharFilter(
        field_name='nama', lookup_expr='icontains', label='NAMA')
    nisn = django_filters.CharFilter(
        field_name='nisn', lookup_expr='icontains', label='NISN')
    nis = django_filters.CharFilter(
        field_name='nis', lookup_expr='icontains', label='NIS')

    class Meta:
        model = Data_Siswa
        fields = ['nis', 'nisn', 'nama', 'kelas']


class GuruFilter(django_filters.FilterSet):
    nama = django_filters.CharFilter(
        field_name='nama', lookup_expr='icontains', label='NAMA')
    nip = django_filters.CharFilter(
        field_name='nip', lookup_expr='icontains', label='NIP')

    class Meta:
        model = Data_Guru
        fields = ['nama', 'nip']


class JadwalFilter(django_filters.FilterSet):
    # tahun_ajaran = django_filters.CharFilter(field_name='tahun_ajaran', lookup_expr='icontains', label='Tahun Ajaran')
    # kelas = django_filters.CharFilter(field_name='kelas', lookup_expr='icontains', label='Kelas')
    guru = django_filters.CharFilter(
        field_name='guru__nama', lookup_expr='icontains', label='Guru')

    class Meta:
        model = Data_Jadwal
        fields = ['kelas', 'guru']


class MapelFilter(django_filters.FilterSet):
    kd_mapel = django_filters.CharFilter(
        field_name='kd_mapel', lookup_expr='icontains', label='KODE MAPEL')
    nama_mapel = django_filters.CharFilter(
        field_name='nama_mapel', lookup_expr='icontains', label='NAMA MAPEL')
    class Meta:
        model = Data_Mapel
        fields = ['kd_mapel','nama_mapel']


class KelasFilter(django_filters.FilterSet):
    kelas = django_filters.CharFilter(
        field_name='kelas', lookup_expr='icontains', label='KELAS')
    jurusan = django_filters.CharFilter(
        field_name='jurusan', lookup_expr='icontains', label='JURUSAN')
    class Meta:
        model = Data_Mapel
        fields = ['kelas','jurusan']

class JurusanFilter(django_filters.FilterSet):
    kd_jurusan = django_filters.CharFilter(
        field_name='kd_jurusan', lookup_expr='icontains', label='KODE JURUSAN')
    jurusan = django_filters.CharFilter(
        field_name='jurusan', lookup_expr='icontains', label='JURUSAN')
    class Meta:
        model = Data_Jurusan
        fields = ['kd_jurusan','jurusan']