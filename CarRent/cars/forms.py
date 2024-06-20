from django import forms
from .models import Car
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'imageUrl1', 'imageUrl2', 'imageUrl3',
                  'image1', 'image2', 'image3', 'price', 'multiplier', 'capacity',
                  'transmission', 'fuelCapacity', 'city', 'latitude', 'longitude']
        widgets = {
            'createdBy': forms.HiddenInput(),
            'createdByEmail': forms.HiddenInput(),
        }
    
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')
        # fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # user.profile.phone_number = self.cleaned_data['phone_number']
            # user.profile.save()
            if hasattr(user, 'profile'):
                user.profile.phone_number = self.cleaned_data['phone_number']
                user.profile.save()
            else:
                Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)


class CarFilterForm(forms.Form):
    city = forms.CharField(required=False)
    min_year = forms.IntegerField(label='Min Year', required=False)
    max_year = forms.IntegerField(label='Max Year', required=False)
    capacity = forms.IntegerField(required=False)
