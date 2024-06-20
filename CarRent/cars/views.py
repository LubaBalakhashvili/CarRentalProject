from django.shortcuts import render, redirect, get_object_or_404
from .models import Car
from .forms import CarForm, ProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Profile, Car, StarredCar, RentedCar
from .forms import CarFilterForm

def car_list(request):
    cars = Car.objects.all()
    popular_car_ids = StarredCar.objects.values_list('car_id', flat=True).distinct()
    popular_cars = Car.objects.filter(id__in=popular_car_ids)

    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'popular_cars': popular_cars,
    })

# def car_list(request):
#     cars = Car.objects.all()
#     return render(request, 'cars/car_list.html', {'cars': cars})

@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.createdBy = request.user
            car.createdByEmail = request.user.email
            car.ownerPhoneNumber = request.user.profile.phone_number
            car.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})


@login_required
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'cars/delete_car.html', {'car': car})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'cars/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('car_list')
    else:
        form = AuthenticationForm()
    return render(request, 'cars/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('car_list')

@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cars = Car.objects.filter(createdBy=user)
    starred_cars = Car.objects.filter(starredcar__user=user)
    rented_cars = Car.objects.filter(rentedcar__user=user)
    # return render(request, 'cars/profile.html', {'profile': profile, 'cars': cars, 'starred_cars': starred_cars})
    return render(request, 'cars/profile.html', {
            'profile': profile,
            'cars': cars,
            'starred_cars': starred_cars,
            'rented_cars': rented_cars,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': profile.phone_number
        })

def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            logout_view(request)
            # return redirect('login')
            return redirect('profile')
    else:
        form = RegisterForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    
    return render(request, 'cars/edit_profile.html', {'form': form, 'profile_form': profile_form})

@login_required
def star_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    StarredCar.objects.get_or_create(user=request.user, car=car)
    return redirect('profile')

@login_required
def unstar_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    StarredCar.objects.filter(user=request.user, car=car).delete()
    return redirect('profile')

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car': car})

# @login_required
# def rent_car(request, car_id):
#     car = get_object_or_404(Car, id=car_id)
#     RentedCar.objects.get_or_create(user=request.user, car=car)
#     return redirect('profile')

@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        days = int(request.POST.get('days'))
        total_price = days * car.price

        # Create the rented car entry
        rented_car = RentedCar.objects.get_or_create(
            user=request.user,
            car=car,
            rent_days=days,
            total_price=total_price
        )
        return redirect('rent_confirmation', rented_car_id=rented_car[0].id)
    
    # else: RentedCar.objects.get_or_create(user=request.user, car=car)
    
    return redirect('profile')

@login_required
def rent_confirmation(request, rented_car_id):
    rented_car = get_object_or_404(RentedCar, id=rented_car_id)
    
    return render(request, 'cars/rent_confirmation.html', {
        'rented_car': rented_car,
    })

@login_required
def unrent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    rented_car = RentedCar.objects.filter(user=request.user, car=car)
    if rented_car.exists():
        rented_car.delete()
    return redirect('profile')

def car_filter(request):
    cars = Car.objects.all()
    filtered_cars = cars

    if request.method == 'GET':
        form = CarFilterForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            min_year = form.cleaned_data.get('min_year')
            max_year = form.cleaned_data.get('max_year')
            capacity = form.cleaned_data.get('capacity')

            if city:
                filtered_cars = filtered_cars.filter(city__icontains=city)
            if min_year:
                filtered_cars = filtered_cars.filter(year__gte=min_year)
            if max_year:
                filtered_cars = filtered_cars.filter(year__lte=max_year)
            if capacity:
                filtered_cars = filtered_cars.filter(capacity=capacity)

    else:
        form = CarFilterForm()

    context = {
        'form': form,
        'filtered_cars': filtered_cars
    }

    return render(request, 'cars/car_filter.html', context)