from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.forms import ModelForm, widgets
from time import timezone
from django import forms
from .models import *
from siswa.models import Data_Siswa
from kbm.models import *
from tahun_ajaran.models import *
from datetime import datetime
from guru.models import *
from django.db.models import Q


class Date_Time_Picker(forms.Form):
    tanggal = forms.DateField(widget=forms.SelectDateWidget(
        years=range(2015, int(datetime.now().year + 1), 1)))


class Tambah_Murid_Form(forms.ModelForm):
    class Meta:
        model = Data_Siswa
        fields = '__all__'
        exclude = ['user', 'nis']

        widgets = {
            'tgl_lahir': forms.SelectDateWidget(years=range(1990, int(datetime.now().year + 1), 1))
        }


class Update_Murid_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['nis'].disabled = True
            self.fields['nisn'].disabled = True

    class Meta:
        model = Data_Siswa
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'tgl_lahir': forms.SelectDateWidget(years=range(1990, int(datetime.now().year + 1), 1))
        }


class Tambah_Guru_Form(forms.ModelForm):
    class Meta:
        model = Data_Guru
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'tgl_lahir': forms.SelectDateWidget(years=range(1990, int(datetime.now().year + 1), 1))
        }


class Update_Guru_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['nip'].disabled = True

    class Meta:
        model = Data_Guru
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'tgl_lahir': forms.SelectDateWidget(years=range(1990, int(datetime.now().year + 1), 1))
        }


class Input_Jadwal_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['tahun_ajaran'].queryset = Data_Tahun_Ajaran.objects.filter(
            tahun=datetime.now().year)
        self.fields['mapel'].queryset = Data_Jadwal.objects.none()

        if 'kelas' in self.data:
            try:
                kelas_id = int(self.data.get('kelas'))
                jenis_mapel = Data_Kelas.objects.get(id=kelas_id)
                self.fields['mapel'].queryset = Data_Mapel.objects.filter(
                    Q(jenis='UMUM') | Q(jenis=jenis_mapel.jurusan.kd_jurusan))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['mapel'].queryset = Data_Mapel.objects.filter(
                Q(jenis='UMUM') | Q(jenis=self.instance.kelas.jurusan.kd_jurusan))

    class Meta:
        model = Data_Jadwal
        fields = '__all__'


class Tambah_Mata_Pelajaran_Form(forms.ModelForm):
    class Meta:
        model = Data_Mapel
        fields = '__all__'


class Tambah_Kelas_Form(forms.ModelForm):
    class Meta:
        model = Data_Kelas
        fields = '__all__'

class Tambah_Jurusan_Form(forms.ModelForm):
    class Meta:
        model = Data_Jurusan
        fields = '__all__'