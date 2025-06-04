# bus/admin.py
from django.contrib import admin
from .models import Operator, Bus, Schedule, Booking

# --- Operator Admin ---
@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'slug') # Tampilkan field ini di daftar
    prepopulated_fields = {'slug': ('name',)} # Otomatis mengisi slug dari nama
    search_fields = ('name', 'description') # Aktifkan pencarian

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description' # Nama kolom di admin

# --- Bus Admin ---
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'operator', 'capacity')
    list_filter = ('operator',) # Filter berdasarkan operator
    search_fields = ('bus_number',)
    raw_id_fields = ('operator',) # Untuk memilih operator jika daftarnya sangat panjang

# --- Schedule Admin ---
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus', 'origin', 'destination', 'departure_time', 'price', 'available_seats')
    list_filter = ('origin', 'destination', 'departure_time', 'bus__operator') # Filter berdasarkan beberapa kriteria
    search_fields = ('origin', 'destination', 'bus__bus_number')
    date_hierarchy = ('departure_time') # Navigasi berdasarkan tanggal
    raw_id_fields = ('bus',) # Untuk memilih bus jika daftarnya sangat panjang
    fieldsets = ( # Mengelompokkan field
        (None, {
            'fields': ('bus', ('origin', 'destination')),
        }),
        ('Time & Price', {
            'fields': (('departure_time', 'arrival_time'), 'price', 'available_seats'),
        }),
    )

# --- Booking Admin ---
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'schedule_info', 'number_of_tickets', 'booking_date', 'is_paid')
    list_filter = ('booking_date', 'is_paid', 'schedule__bus__operator') # Filter
    search_fields = ('passenger_name', 'passenger_email', 'schedule__origin', 'schedule__destination')
    date_hierarchy = 'booking_date'
    readonly_fields = ('booking_date',) # Booking date diisi otomatis
    fieldsets = (
        (None, {
            'fields': ('schedule', ('passenger_name', 'passenger_email'), 'number_of_tickets'),
        }),
        ('Status & Info', {
            'fields': ('is_paid', 'booking_date'),
        }),
    )

    def schedule_info(self, obj):
        return f"{obj.schedule.origin} - {obj.schedule.destination} ({obj.schedule.departure_time.strftime('%Y-%m-%d %H:%M')})"
    schedule_info.short_description = 'Schedule' # Nama kolom di admin