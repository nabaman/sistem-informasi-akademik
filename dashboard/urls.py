from django.urls import path, include
from django.conf.urls import url
from .views import *

app_name = 'dashboard'

urlpatterns = [

    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name='logout'),


    #UNTUK GURU
    path('nilai/',nilaiView, name='nilai'),
    path('nilai/mata_pelajaran/<str:pk>/',nilaiDetailView, name='nilai_detail'), #GURU WALI KELAS
    path('update_nilai',update_nilai, name='update_nilai'),#GURU WALI KELAS
    path('informasi-pribadi-guru/',informasi_pribadi_guru, name='informasi-pribadi-guru'),
    path('jadwal-mengajar/',jadwal_mengajar, name='jadwal-mengajar'),




    #UNTUK MURID
    path('rangkuman-nilai/',rangkuman_nilai, name='rangkuman-nilai'),
    path('informasi-pribadi-siswa/',informasi_pribadi_siswa, name='informasi-pribadi-siswa'),
    path('informasi-pembayaran/',informasi_pembayaran, name='informasi-pembayaran'),
    path('jadwal-pelajaran/',jadwal_pelajaran, name='jadwal-pelajaran'),




    #UNTUK STAFF
    #manajemen murid
    path('data-murid', semua_murid, name='data-murid'),
    path('data-murid/tambah-murid', tambah_murid, name='tambah-murid'),
    path('data-murid/detail-murid/<str:pk>', detail_murid, name='detail-murid'),
    path('data-murid/update-murid/<str:pk>', update_murid, name='update-murid'),
    path('data-murid/hapus-murid/<str:pk>', hapus_murid, name='hapus-murid'),
    #manajemen guru
    path('data-guru', semua_guru, name='data-guru'),
    path('data-guru/tambah-guru', tambah_guru, name='tambah-guru'),
    path('data-guru/detail-guru/<str:pk>', detail_guru, name='detail-guru'),
    path('data-guru/update-guru/<str:pk>', update_guru, name='update-guru'),
    path('data-guru/hapus-guru/<str:pk>', hapus_guru, name='hapus-guru'),
    #manajemen mapel
    path('data-mapel', semua_mapel, name='data-mapel'),
    path('data-mapel/tambah-mapel', tambah_mapel, name='tambah-mapel'),
    path('data-mapel/update-mapel/<str:pk>', update_mapel, name='update-mapel'),
    path('data-mapel/hapus-mapel/<str:pk>', hapus_mapel, name='hapus-mapel'),
    #manajemen kelas
    path('data-kelas', semua_kelas, name='data-kelas'),
    path('data-kelas/tambah-kelas', tambah_kelas, name='tambah-kelas'),
    path('data-kelas/update-kelas/<str:pk>', update_kelas, name='update-kelas'),
    path('data-kelas/hapus-kelas/<str:pk>', hapus_kelas, name='hapus-kelas'),
    #manajemen jurusan
    path('data-jurusan', semua_jurusan, name='data-jurusan'),
    path('data-jurusan/tambah-jurusan', tambah_jurusan, name='tambah-jurusan'),
    path('data-jurusan/update-jurusan/<str:pk>', update_jurusan, name='update-jurusan'),
    path('data-jurusan/hapus-jurusan/<str:pk>', hapus_jurusan, name='hapus-jurusan'),
    
    path('data-pembayaran', data_murid_pembayaran, name='data-murid-pembayaran'),
    path('data-pembayaran/murid/<str:pk>',pembayaran_siswa, name='pembayaran-siswa'),

    #manajemen jadwal
    path('data-jadwal', semua_jadwal, name='data-jadwal'),
    path('data-jadwal/tambah-jadwal', tambah_jadwal, name='tambah-jadwal'),
    path('data-jadwal/update-jadwal/<str:pk>', update_jadwal, name='ubah-jadwal'),
    path('data-jadwal/hapus-jadwal/<str:pk>', hapus_jadwal, name='hapus-jadwal'),
    path('ajax-mapel', load_mapel, name='load-mapel'),


    path('test',pdf ),

    path('', login_required(IndexView.as_view()), name="index"),
    url(r'^blank/$', BlankView.as_view(), name="blank"),
    url(r'^buttons/$', ButtonsView.as_view(), name="buttons"),
    url(r'^flot/$', FlotView.as_view(), name="flot"),
    url(r'^forms/$', FormsView.as_view(), name="forms"),
    url(r'^grid/$', GridView.as_view(), name="grid"),
    url(r'^icons/$', IconsView.as_view(), name="icons"),
    url(r'^morris/$', MorrisView.as_view(), name="morris"),
    url(r'^notifications/$', NotificationsView.as_view(), name="notifications"),
    url(r'^panels/$', PanelsView.as_view(), name="panels"),
    url(r'^tables/$', TablesView.as_view(), name="tables"),
    url(r'^typography/$', TypographyView.as_view(), name="typography"),

]