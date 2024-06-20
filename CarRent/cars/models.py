from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=100, default='Default Brand')
    model = models.CharField(max_length=100, default='Default Model')
    year = models.IntegerField(default=2000)
    imageUrl1 = models.URLField(max_length=200, blank=True, default='')
    imageUrl2 = models.URLField(max_length=200, blank=True, default='')
    imageUrl3 = models.URLField(max_length=200, blank=True, default='')
    image1 = models.ImageField(upload_to='images/', blank=True, default='default.jpg')
    image2 = models.ImageField(upload_to='images/', blank=True, default='default.jpg')
    image3 = models.ImageField(upload_to='images/', blank=True, default='default.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    capacity = models.IntegerField(default=4)
    transmission = models.CharField(max_length=50, default='Manual')
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars', default=1)
    createdByEmail = models.EmailField(default='example@example.com')
    fuelCapacity = models.DecimalField(max_digits=5, decimal_places=2, default=50.0)
    city = models.CharField(max_length=100, default='Default City')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    ownerPhoneNumber = models.CharField(max_length=15, default='0000000000')

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Rental of {self.car} by {self.customer_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='username')
    last_name = models.CharField(max_length=30, default='lastname')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class StarredCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'car')


class RentedCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rent_days = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    rent_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} rented {self.car.brand} {self.car.model}"        