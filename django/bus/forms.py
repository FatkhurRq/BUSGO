from django import forms
from .models import Booking, Schedule

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger_name', 'passenger_email', 'number_of_tickets']

    # Constructor untuk menerima objek schedule
    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop('schedule', None) # Ambil objek schedule dari kwargs
        super().__init__(*args, **kwargs)
        # Opsional: Atur widget untuk number_of_tickets
        self.fields['number_of_tickets'].widget = forms.NumberInput(attrs={'min': 1, 'max': self.schedule.available_seats if self.schedule else 1})

    def clean_number_of_tickets(self):
        num_tickets = self.cleaned_data.get('number_of_tickets')

        if num_tickets is None: # Pastikan ada nilai
            raise forms.ValidationError("Jumlah tiket tidak boleh kosong.")

        if num_tickets <= 0:
            raise forms.ValidationError("Jumlah tiket minimal adalah 1.")

        if self.schedule and num_tickets > self.schedule.available_seats:
            raise forms.ValidationError(f"Maaf, hanya tersedia {self.schedule.available_seats} kursi untuk jadwal ini.")

        return num_tickets

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data