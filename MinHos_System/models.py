from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    # Corrected indentation and fixed typo
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    # Corrected indentation
    def __str__(self):
        return f"{self.name} (Age: {self.age})"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.CharField(max_length=255)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed')])

    # Corrected indentation
    def __str__(self):
        return f"Appointment for {self.patient.name} with {self.doctor.name} on {self.appointment_date}"
