from django.shortcuts import render
from .models import Operator, Schedule, Booking
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from django.db.models import Q 
from datetime import datetime, time 
from django.template.loader import get_template
get_template('bus/search_schedules.html')

def home(request):
    operators = Operator.objects.all() # Ambil semua operator dari database
    context = {
        'operators': operators
    }
    return render(request, 'bus/home.html', context)

def operator_detail(request, operator_slug):
    operator = get_object_or_404(Operator, slug=operator_slug)
    schedules = Schedule.objects.filter(bus__operator=operator).order_by('departure_time')
    context = {
        'operator': operator,
        'schedules': schedules,
    }
    return render(request, 'bus/operator_detail.html', context)

def book_ticket(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if schedule.available_seats <= 0:
        # Opsional: Redirect ke halaman error atau tampilkan pesan
        return render(request, 'bus/book_ticket.html', {
            'schedule': schedule,
            'form': None, # Atau form kosong tanpa tombol submit
            'error_message': 'Maaf, tiket untuk jadwal ini sudah habis.'
        })

    if request.method == 'POST':
        form = BookingForm(request.POST, schedule=schedule) # Teruskan objek schedule
        if form.is_valid():
            booking = form.save(commit=False)
            booking.schedule = schedule
            # Jika ada sistem user login
            booking.save()
            # Kurangi kursi yang tersedia SETELAH booking berhasil disimpan
            schedule.available_seats -= booking.number_of_tickets
            schedule.save()
            return redirect('bus:booking_success', booking_id=booking.id)
    else:
        form = BookingForm(schedule=schedule) # Teruskan objek schedule juga saat GET

    context = {
        'schedule': schedule,
        'form': form,
    }
    return render(request, 'bus/book_ticket.html', context)

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bus/booking_success.html', {'booking': booking})

def ticket_detail(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    context = {
        'schedule': schedule,
    }
    return render(request, 'bus/ticket_detail.html', context)

def search_schedules(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    date_str = request.GET.get('date') # Format YYYY-MM-DD

    schedules = Schedule.objects.all()

    if origin:
        schedules = schedules.filter(origin__icontains=origin) 
    if destination:
        schedules = schedules.filter(destination__icontains=destination)
    if date_str:
        try:
            search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            schedules = schedules.filter(
                departure_time__date=search_date
            )
        except ValueError:
            pass # Atau tambahkan pesan error ke user

    # Urutkan hasil
    schedules = schedules.order_by('departure_time')

    context = {
        'schedules': schedules,
        'origin_query': origin or '', 
        'destination_query': destination or '',
        'date_query': date_str or '',
    }
    return render(request, 'bus/search_results.html', context)

