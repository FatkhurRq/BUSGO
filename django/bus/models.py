
from django.db import models
from django.contrib.auth.models import User

class Operator(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True) # Untuk URL yang lebih bersih (e.g., /transjatim/)

    def __str__(self):
        return self.name

class Bus(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    bus_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    # dll (misal: tipe bus)

    def __str__(self):
        return f"{self.operator.name} - {self.bus_number}"

class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    # origin = models.CharField(max_length=100)
    # destination = models.CharField(max_length=100)
    # departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField()
    origin = models.CharField(max_length=100, db_index=True) 
    destination = models.CharField(max_length=100, db_index=True)
    departure_time = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.bus.bus_number} - {self.origin} to {self.destination} ({self.departure_time.strftime('%Y-%m-%d %H:%M')})"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Opsional, jika ada sistem user
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=200)
    passenger_email = models.EmailField()
    number_of_tickets = models.IntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    def get_total_price(self):
        return self.number_of_tickets * self.schedule.price
    # Mungkin tambahkan kolom untuk kode booking, dll.

    def __str__(self):
        return f"Booking for {self.passenger_name} on {self.schedule}"
