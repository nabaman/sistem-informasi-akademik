import json
import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorator import unauthenticated_user
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from .utility import render_to_pdf


from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User, Group
from datetime import timedelta, datetime


from .filters import *
from kbm.models import *
from siswa.models import *
from guru.models import *
from absen.models import *
from .models import *
from .forms import *

# Create your views here.


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            messages.info(request, 'Username atau Password salah')
            return render(request, 'components/login.html')

    context = {}
    return render(request, 'components/login.html', context)


def logoutUser(request):

    logout(request)
    return redirect('index')


# UNTUK GURU
@user_passes_test(lambda user: Group.objects.get(name='guru') in user.groups.all())
def nilaiView(request):

    jadwal_mapel = Data_Mapel.objects.all().filter(Q(jenis='UMUM') | Q(
        jenis=request.user.data_guru.data_kelas.jurusan.kd_jurusan))

    if request.method == 'POST':
        mapel_id = request.POST['mapel_id']
        return redirect('dashboard:nilai_detail', mapel_id)

    context = {
        'mapel_guru': jadwal_mapel
    }

    return render(request, 'guru/nilai/nilai.html', context)


@user_passes_test(lambda user: Group.objects.get(name='guru') in user.groups.all())
def nilaiDetailView(request, pk):
    mapel = Data_Mapel.objects.get(pk=pk)
    thn_ajaran_ganjil = Data_Tahun_Ajaran.objects.filter(
        tahun=datetime.now().year).first()
    thn_ajaran_genap = Data_Tahun_Ajaran.objects.filter(
        tahun=datetime.now().year).last()
    ganjil = range(1, 7)
    genap = range(6, 13)

    if datetime.now().month in list(ganjil):
        nilai = Data_Nilai.objects.filter(
            mapel_id=mapel.id, tahun_ajaran=thn_ajaran_ganjil, wali_kelas_id=request.user.data_guru.id)

    if datetime.now().month in list(genap):
        nilai = Data_Nilai.objects.filter(
            mapel_id=mapel.id, tahun_ajaran=thn_ajaran_genap, wali_kelas_id=request.user.data_guru.id)

    context = {
        'nilai': nilai,
    }

    return render(request, 'guru/nilai/nilai_detail.html', context)


@user_passes_test(lambda user: Group.objects.get(name='guru') in user.groups.all())
@csrf_exempt
def update_nilai(request):
    data = request.POST.get("data")
    dict_data = json.loads(data)

    for dic_single in dict_data:
        nilai = Data_Nilai.objects.get(id=dic_single['id'])
        if int(dic_single['tugas']) >= 0 and int(dic_single['tugas']) <= 100:
            nilai.tugas = int(dic_single['tugas'])
            nilai.save()
        if int(dic_single['uts']) >= 0 and int(dic_single['uts']) <= 100:
            nilai.uts = int(dic_single['uts'])
            nilai.save()
        if int(dic_single['uas']) >= 0 and int(dic_single['uas']) <= 100:
            nilai.uas = int(dic_single['uas'])
            nilai.save()
        if int(dic_single['keterampilan']) >= 0 and int(dic_single['keterampilan']) <= 100:
            nilai.keterampilan = int(dic_single['keterampilan'])
            nilai.save()
    return redirect(request.path)


@user_passes_test(lambda user: Group.objects.get(name='guru') in user.groups.all())
def informasi_pribadi_guru(request):
    guru = Data_Guru.objects.get(id=request.user.data_guru.id)
    id_mapel = Data_Jadwal.objects.filter(guru_id=request.user.data_guru.id).order_by(
        'mapel').values_list('mapel').distinct()
    mapel = Data_Mapel.objects.filter(id__in=id_mapel)
    context = {
        'guru': guru,
        'mapel': mapel,
    }

    return render(request, 'guru/informasi_pribadi/informasi_pribadi.html', context)


@user_passes_test(lambda user: Group.objects.get(name='guru') in user.groups.all())
def jadwal_mengajar(request):

    jadwal_guru = Data_Jadwal.objects.filter(guru=request.user.data_guru.id)

    context = {
        'jadwal': jadwal_guru
    }

    return render(request, 'guru/jadwal_mengajar/jadwal_mengajar.html', context)


# UNTUK SISWA
@user_passes_test(lambda user: Group.objects.get(name='siswa') in user.groups.all())
def rangkuman_nilai(request):
    thn_ajaran_ganjil = Data_Tahun_Ajaran.objects.filter(
        tahun=datetime.now().year).first()
    thn_ajaran_genap = Data_Tahun_Ajaran.objects.filter(
        tahun=datetime.now().year).last()
    ganjil = range(1, 7)
    genap = range(6, 13)

    a = Data_Mapel.objects.all

    if datetime.now().month in list(ganjil):
        siswa = Data_Nilai.objects.filter(
            siswa_id=request.user.data_siswa.id, tahun_ajaran=thn_ajaran_ganjil)

    if datetime.now().month in list(genap):
        siswa = Data_Nilai.objects.filter(
            siswa_id=request.user.data_siswa.id, tahun_ajaran=thn_ajaran_genap)

    context = {
        'data_siswa': siswa,
    }
    return render(request, 'siswa/nilai/rangkuman_nilai.html', context)


@user_passes_test(lambda user: Group.objects.get(name='siswa') in user.groups.all())
def informasi_pribadi_siswa(request):
    siswa = Data_Siswa.objects.get(id=request.user.data_siswa.id)
    context = {
        'siswa': siswa,

    }
    return render(request, 'siswa/informasi_pribadi/informasi_pribadi.html', context)


@user_passes_test(lambda user: Group.objects.get(name='siswa') in user.groups.all())
def informasi_pembayaran(request):

    siswa = Data_Siswa.objects.get(id=request.user.data_siswa.id)
    waktu = Data_Siswa.objects.get(id=request.user.data_siswa.id).tgl_lahir

    spp = siswa.data_pembayaran_spp_set.all().filter(jenis_pembayaran=1)
    uts = siswa.data_pembayaran_uts_set.all().filter(
        jenis_pembayaran=2).order_by('tahun_ajaran')
    uas = siswa.data_pembayaran_uas_set.all().filter(
        jenis_pembayaran=3).order_by('tahun_ajaran')

    context = {
        'pembayaran': spp,
        'bayar_uts': uts,
        'bayar_uas': uas
    }
    return render(request, 'siswa/pembayaran/pembayaran.html', context)


@user_passes_test(lambda user: Group.objects.get(name='siswa') in user.groups.all())
def jadwal_pelajaran(request):
    jadwal_senin = Data_Jadwal.objects.filter(tahun_ajaran__tahun=datetime.now().year,
                                              kelas=request.user.data_siswa.kelas, hari='senin')
    jadwal_selasa = Data_Jadwal.objects.filter(tahun_ajaran__tahun=datetime.now().year,
                                               kelas=request.user.data_siswa.kelas, hari='selasa')
    jadwal_rabu = Data_Jadwal.objects.filter(tahun_ajaran__tahun=datetime.now().year,
                                             kelas=request.user.data_siswa.kelas, hari='rabu')
    jadwal_kamis = Data_Jadwal.objects.filter(tahun_ajaran__tahun=datetime.now().year,
                                              kelas=request.user.data_siswa.kelas, hari='kamis')
    jadwal_jumat = Data_Jadwal.objects.filter(tahun_ajaran__tahun=datetime.now().year,
                                              kelas=request.user.data_siswa.kelas, hari="jum'at")
    jadwal_sabtu = Data_Jadwal.objects.filter(tahun_ajaran__tahun=datetime.now().year,
                                              kelas=request.user.data_siswa.kelas, hari='sabtu')
    jadwal = Data_Jadwal.objects.filter(tahun_ajaran__tahun=datetime.now().year,
                                        kelas=request.user.data_siswa.kelas)

    context = {'jadwal_senin': jadwal_senin,
               'jadwal_selasa': jadwal_selasa,
               'jadwal_rabu': jadwal_rabu,
               'jadwal_kamis': jadwal_kamis,
               'jadwal_jumat': jadwal_jumat,
               'jadwal_sabtu': jadwal_sabtu,
               'jadwal': jadwal
               }

    return render(request, 'siswa/jadwal_pelajaran/jadwal_pelajaran.html', context)


def absen_siswa(request):

    context = {}
    return render(request, 'dashboard/absen.html', context)


def absen_guru(request):

    context = {}
    return render(request, 'dashboard/absen.html', context)


# STAFF TU
# manajemen murid
@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def semua_murid(request):
    murid_all = Data_Siswa.objects.all().order_by('id')
    my_filter = MuridFilter(request.GET, queryset=murid_all)
    murid_all = my_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(murid_all, 5)

    try:
        murid = paginator.page(page)
    except PageNotAnInteger:
        murid = paginator.page(1)
    except EmptyPage:
        murid = paginator.page(paginator.num_pages)

    context = {'murid': murid, 'my_filter': my_filter}
    return render(request, 'staff/data_murid/data_murid.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def detail_murid(request, pk):

    siswa = Data_Siswa.objects.get(id=pk)
    print(siswa)
    context = {'siswa': siswa}

    return render(request, 'staff/data_murid/detail_murid.html', context)


def hapus_murid(request, pk):
    murid = Data_Siswa.objects.get(id=pk).delete()

    return redirect(reverse('dashboard:data-murid') + '?kelas=&nis=&nisn=&nama=')


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def update_murid(request, pk):
    siswa = Data_Siswa.objects.get(id=pk)

    data_siswa = {
        'nis': siswa.nis,
        'nisn': siswa.nisn,
        'nama': siswa.nama,
        'kelas': siswa.kelas,
        'tgl_lahir': siswa.tgl_lahir,
        'alamat': siswa.alamat,
        'jenis_kelamin': siswa.jenis_kelamin,
        'sekolah_sebelumnya': siswa.sekolah_sebelumnya,
        'foto': siswa.foto,
    }
    form_tambah_murid = Update_Murid_Form(
        request.POST or None, initial=data_siswa, instance=siswa)
    if request.method == 'POST':
        if form_tambah_murid.is_valid():
            form_tambah_murid.save()
            return redirect(reverse('dashboard:data-murid') + '?kelas=&nis=&nisn=&nama=')

    context = {'form': form_tambah_murid, 'tombol': 'Update'}
    return render(request, 'staff/data_murid/tambah_murid.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def tambah_murid(request):
    form_tambah_murid = Tambah_Murid_Form

    if request.method == 'POST':
        form_tambah_murid = form_tambah_murid(request.POST)
        if form_tambah_murid.is_valid():

            form_tambah_murid.save()

            return redirect(reverse('dashboard:data-murid') + '?kelas=&nis=&nisn=&nama=')
    context = {'form': form_tambah_murid, 'tombol': 'Tambah'}
    return render(request, 'staff/data_murid/tambah_murid.html', context)

# manajemen guru


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def semua_guru(request):
    guru_all = Data_Guru.objects.all().order_by('id')
    my_filter = GuruFilter(request.GET, queryset=guru_all)
    guru_all = my_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(guru_all, 5)

    try:
        guru = paginator.page(page)
    except PageNotAnInteger:
        guru = paginator.page(1)
    except EmptyPage:
        guru = paginator.page(paginator.num_pages)

    context = {'guru': guru, 'my_filter': my_filter}
    return render(request, 'staff/data_guru/data_guru.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def detail_guru(request, pk):

    guru = Data_Guru.objects.get(id=pk)
    context = {'guru': guru}

    return render(request, 'staff/data_guru/detail_guru.html', context)


def hapus_guru(request, pk):
    murid = Data_Guru.objects.get(id=pk).delete()

    return redirect(reverse('dashboard:data-guru')+'?nip=&nama=')


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def update_guru(request, pk):
    guru = Data_Guru.objects.get(id=pk)

    data_guru = {
        'nip': guru.nip,
        'nama': guru.nama,
        'tgl_lahir': guru.tgl_lahir,
        'alamat': guru.alamat,
        'jenis_kelamin': guru.jenis_kelamin,
        'foto': guru.foto,
    }
    form_ubah_guru = Update_Guru_Form(
        request.POST or None, initial=data_guru, instance=guru)
    if request.method == 'POST':
        if form_ubah_guru.is_valid():
            form_ubah_guru.save()
            return redirect(reverse('dashboard:data-guru') + '?nip=&nama=')

    context = {'form': form_ubah_guru, 'tombol': 'Update'}
    return render(request, 'staff/data_guru/tambah_guru.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def tambah_guru(request):
    form_tambah_guru = Tambah_Guru_Form

    if request.method == 'POST':
        form_tambah_guru = form_tambah_guru(request.POST)
        if form_tambah_guru.is_valid():

            form_tambah_guru.save()

            return redirect(reverse('dashboard:data-guru') + '?nip=&nama=')
    context = {'form': form_tambah_guru, 'tombol': 'Tambah'}
    return render(request, 'staff/data_guru/tambah_guru.html', context)

# manajemen pembayaran


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def data_murid_pembayaran(request):
    murid_all = Data_Siswa.objects.all().order_by('id')
    my_filter = MuridFilter(request.GET, queryset=murid_all)
    murid_all = my_filter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(murid_all, 5)

    try:
        murid = paginator.page(page)
    except PageNotAnInteger:
        murid = paginator.page(1)
    except EmptyPage:
        murid = paginator.page(paginator.num_pages)

    context = {'murid': murid, 'my_filter': my_filter}
    return render(request, 'staff/pembayaran/data_murid.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def pembayaran_siswa(request, pk):
    siswa = Data_Siswa.objects.get(id=pk)
    spp = siswa.data_pembayaran_spp_set.all().filter(jenis_pembayaran=1)
    uts = siswa.data_pembayaran_uts_set.all().filter(jenis_pembayaran=2)
    uas = siswa.data_pembayaran_uas_set.all().filter(jenis_pembayaran=3)

    if request.method == 'POST':
        if request.POST.get('bayar-spp'):
            target = Data_Pembayaran_SPP.objects.get(
                id=request.POST.get('bayar-spp'))
            target.status = 'Lunas'
            target.save()
            return redirect('dashboard:pembayaran-siswa', pk)
        if request.POST.get('bayar-uts'):
            target = Data_Pembayaran_UTS.objects.get(
                id=request.POST.get('bayar-uts'))
            target.status = 'Lunas'
            target.save()
            return redirect('dashboard:pembayaran-siswa', pk)
        if request.POST.get('bayar-uas'):
            target = Data_Pembayaran_UAS.objects.get(
                id=request.POST.get('bayar-uas'))
            target.status = 'Lunas'
            target.save()
            return redirect('dashboard:pembayaran-siswa', pk)
    context = {
        'pembayaran': spp,
        'bayar_uts': uts,
        'bayar_uas': uas
    }
    return render(request, 'staff/pembayaran/pembayaran.html', context)

# manajemen jadwal


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def semua_jadwal(request):
    list_jadwal = Data_Jadwal.objects.all().order_by('id', 'jam')
    my_filter = JadwalFilter(request.GET, queryset=list_jadwal)
    list_jadwal = my_filter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(list_jadwal, 10)
    try:
        jadwal = paginator.page(page)
    except PageNotAnInteger:
        jadwal = paginator.page(1)
    except EmptyPage:
        jadwal = paginator.page(paginator.num_pages)

    context = {'jadwal': jadwal, 'my_filter': my_filter}
    return render(request, 'staff/data_jadwal/data_jadwal.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def tambah_jadwal(request):
    form = Input_Jadwal_Form
    if request.method == 'POST':
        form = form(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect(reverse('dashboard:data-jadwal') + '?kelas=&guru=')
    context = {
        'form': form,
        'tombol': 'Buat Jadwal'
    }

    return render(request, 'staff/data_jadwal/tambah_jadwal.html', context)


def update_jadwal(request, pk):
    jadwal = Data_Jadwal.objects.get(id=pk)
    data_jadwal = {
        'hari': jadwal.hari,
    }
    form = Input_JadwalForm(request.POST or None,
                            initial=data_jadwal, instance=jadwal)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect(reverse('dashboard:data-jadwal') + '?kelas=&guru=')

    context = {'form': form, 'tombol': 'Update Jadwal'}

    return render(request, 'staff/data_jadwal/tambah_jadwal.html', context)


def hapus_jadwal(request, delete_id):

    jadwal = Data_Jadwal.objects.get(id=delete_id).delete()

    return redirect(reverse('dashboard:data-jadwal') + '?kelas=&guru=')


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def load_mapel(request):
    kelas = request.GET.get('kelas')
    jenis_mapel = Data_Kelas.objects.get(id=kelas)

    mapel = Data_Mapel.objects.filter(
        Q(jenis='UMUM') | Q(jenis=jenis_mapel.jurusan.kd_jurusan))

    context = {
        'mapel': mapel
    }
    return render(request, 'staff/jadwal/drop_down_mapel.html', context)

# manajemen mapel


def semua_mapel(request):
    list_mapel = Data_Mapel.objects.all().order_by('id')
    my_filter = MapelFilter(request.GET, queryset=list_mapel)
    list_mapel = my_filter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(list_mapel, 10)
    try:
        mapel = paginator.page(page)
    except PageNotAnInteger:
        mapel = paginator.page(1)
    except EmptyPage:
        mapel = paginator.page(paginator.num_pages)

    context = {'mapel': mapel, 'my_filter': my_filter}
    return render(request, 'staff/data_mapel/data_mapel.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def tambah_mapel(request):
    form = Tambah_Mata_Pelajaran_Form
    if request.method == 'POST':
        form = form(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect(reverse('dashboard:data-mapel') + '?kd_mapel=&nama_mapel=')
    context = {
        'form': form,
        'tombol': 'Buat MAPEL'
    }

    return render(request, 'staff/data_mapel/tambah_mapel.html', context)


def update_mapel(request, pk):
    mapel = Data_Mapel.objects.get(id=pk)
    data_mapel = {
        'kd_mapel': mapel.kd_mapel,
        'nama_mapel': mapel.nama_mapel,
        'bobot': mapel.bobot,
        'jenis': mapel.jenis,
        'kkm': mapel.kkm
    }
    form = Tambah_Mata_PelajaranForm(request.POST or None,
                                     initial=data_mapel, instance=mapel)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect(reverse('dashboard:data-mapel') + '?kd_mapel=&nama_mapel=')

    context = {'form': form, 'tombol': 'Update Mapel'}

    return render(request, 'staff/data_mapel/tambah_mapel.html', context)


def hapus_mapel(request, pk):

    jadwal = Data_Mapel.objects.get(id=pk).delete()

    return redirect(reverse('dashboard:data-mapel') + '?kd_mapel=&nama_mapel=')

# manajemen kelas


def semua_kelas(request):
    list_kelas = Data_Kelas.objects.all().order_by('id')
    my_filter = KelasFilter(request.GET, queryset=list_kelas)
    list_kelas = my_filter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(list_kelas, 10)
    try:
        kelas = paginator.page(page)
    except PageNotAnInteger:
        kelas = paginator.page(1)
    except EmptyPage:
        kelas = paginator.page(paginator.num_pages)

    context = {'kelas': kelas, 'my_filter': my_filter}
    return render(request, 'staff/data_kelas/data_kelas.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def tambah_kelas(request):
    form = Tambah_Kelas_Form
    if request.method == 'POST':
        form = form(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect(reverse('dashboard:data-kelas') + '?kelas=&jurusan=')
    context = {
        'form': form,
        'tombol': 'Buat Kelas'
    }

    return render(request, 'staff/data_kelas/tambah_kelas.html', context)


def update_kelas(request, pk):
    kelas = Data_Kelas.objects.get(id=pk)
    data_kelas = {
        'kelas': kelas.kelas,
        'jurusan': kelas.jurusan,
        'ruang': kelas.ruang,
        'wali_kelas': kelas.wali_kelas,
    }
    form = Tambah_Kelas_Form(request.POST or None,
                             initial=data_kelas, instance=kelas)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect(reverse('dashboard:data-kelas') + '?kelas=&jurusan=')

    context = {'form': form, 'tombol': 'Update Kelas'}

    return render(request, 'staff/data_kelas/tambah_kelas.html', context)


def hapus_kelas(request, pk):

    jadwal = Data_Kelas.objects.get(id=pk).delete()

    return redirect(reverse('dashboard:data-kelas') + '?kelas=&jurusan=')

# manajemen jurusan


def semua_jurusan(request):
    list_jurusan = Data_Jurusan.objects.all().order_by('id')
    my_filter = JurusanFilter(request.GET, queryset=list_jurusan)
    list_jurusan = my_filter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(list_jurusan, 10)
    try:
        jurusan = paginator.page(page)
    except PageNotAnInteger:
        jurusan = paginator.page(1)
    except EmptyPage:
        jurusan = paginator.page(paginator.num_pages)

    context = {'jurusan': jurusan, 'my_filter': my_filter}
    return render(request, 'staff/data_jurusan/data_jurusan.html', context)


@user_passes_test(lambda user: Group.objects.get(name='staff_tu') in user.groups.all())
def tambah_jurusan(request):
    form = Tambah_Jurusan_Form
    if request.method == 'POST':
        form = form(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect(reverse('dashboard:data-jurusan') + '?kd_jurusan=&jurusan=')
    context = {
        'form': form,
        'tombol': 'Buat Jurusan'
    }

    return render(request, 'staff/data_jurusan/tambah_jurusan.html', context)


def update_jurusan(request, pk):
    jurusan = Data_Jurusan.objects.get(id=pk)
    data_jurusan = {
        'kd_jurusan': jurusan.kd_jurusan,
        'jurusan': jurusan.jurusan,
    }
    form = Tambah_Jurusan_Form(request.POST or None,
                               initial=data_jurusan, instance=jurusan)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect(reverse('dashboard:data-jurusan') + '?kd_jurusan=&jurusan=')

    context = {'form': form, 'tombol': 'Update Jurusan'}

    return render(request, 'staff/data_jurusan/tambah_jurusan.html', context)


def hapus_jurusan(request, pk):

    jadwal = Data_Jurusan.objects.get(id=pk).delete()

    return redirect(reverse('dashboard:data-jurusan') + '?kd_jurusan=&jurusan=')


class IndexView(TemplateView):
    template_name = "components/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Dashboard", 'tahun_ajaran': Data_Tahun_Ajaran.objects.filter(
            tahun=datetime.now().year).first().tahun})
        return context


class BlankView(TemplateView):
    template_name = "components/blank.html"

    def get_context_data(self, **kwargs):
        context = super(BlankView, self).get_context_data(**kwargs)
        context.update({'title': "Blank Page"})
        return context


class ButtonsView(TemplateView):
    template_name = "components/buttons.html"

    def get_context_data(self, **kwargs):
        context = super(ButtonsView, self).get_context_data(**kwargs)
        context.update({'title': "Buttons"})
        return context


class FlotView(TemplateView):
    template_name = "components/flot.html"

    def get_context_data(self, **kwargs):
        context = super(FlotView, self).get_context_data(**kwargs)
        context.update({'title': "Flot Charts"})
        return context


class FormsView(TemplateView):
    template_name = "components/forms.html"

    def get_context_data(self, **kwargs):
        context = super(FormsView, self).get_context_data(**kwargs)
        context.update({'title': "Forms"})
        return context


class GridView(TemplateView):
    template_name = "components/grid.html"

    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)
        context.update({'title': "Grid"})
        return context


class IconsView(TemplateView):
    template_name = "components/icons.html"

    def get_context_data(self, **kwargs):
        context = super(IconsView, self).get_context_data(**kwargs)
        context.update({'title': "Icons"})
        return context


class MorrisView(TemplateView):
    template_name = "components/morris.html"

    def get_context_data(self, **kwargs):
        context = super(MorrisView, self).get_context_data(**kwargs)
        context.update({'title': "Morris Charts"})
        return context


class NotificationsView(TemplateView):
    template_name = "components/notifications.html"

    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context.update({'title': "Notifications"})
        return context


class PanelsView(TemplateView):
    template_name = "components/panels-wells.html"

    def get_context_data(self, **kwargs):
        context = super(PanelsView, self).get_context_data(**kwargs)
        context.update({'title': "Panels and Wells"})
        return context


class TablesView(TemplateView):
    template_name = "components/tables.html"

    def get_context_data(self, **kwargs):
        context = super(TablesView, self).get_context_data(**kwargs)
        context.update({'title': "Tables"})
        return context


class TypographyView(TemplateView):
    template_name = "components/typography.html"

    def get_context_data(self, **kwargs):
        context = super(TypographyView, self).get_context_data(**kwargs)
        context.update({'title': "Typography"})
        return context


def pdf(request, *args, **kwargs):
    template = get_template('siswa/nilai/rapot.html')
    context = {
        'nama': "NABA ULVIYAN",
        'id': 161011400060
    }
    html = template.render(context)
    pdf_render = render_to_pdf('siswa/nilai/rapot.html', context)
    return HttpResponse(pdf_render, content_type='application/pdf')