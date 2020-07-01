from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Data_Nilai)
admin.site.register(Data_Pembayaran_SPP)
admin.site.register(Data_Pembayaran_UTS)
admin.site.register(Data_Pembayaran_UAS)
admin.site.register(Bulan_Pembayaran)
admin.site.register(Jenis_Pembayaran)