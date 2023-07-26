from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from auth_app.models import ViaPraetoriaUserProfile

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from .models import ViaPraetoriaUserProfile

UserModel = get_user_model()


class UserRegisterForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=ViaPraetoriaUserProfile.FIRST_NAME_MAX_LENGTH)
    last_name = forms.CharField(max_length=ViaPraetoriaUserProfile.LAST_NAME_MAX_LENGTH)
    phone_number = PhoneNumberField()
    date_of_birth = forms.DateField()
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=ViaPraetoriaUserProfile.GENDERS)

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = ViaPraetoriaUserProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            phone_number=self.cleaned_data['phone_number'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender'],
            user=user,
        )
        if commit:
            profile.save()
        return user

    class Meta:
        model = UserModel
        fields = ('password1', 'password2', 'first_name', 'last_name', 'phone_number', 'gender')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'date_of_birth': forms.DateInput(attrs={'min': '1920-01-01'}),
        }


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['gender'] = ViaPraetoriaUserProfile.DO_NOT_SHOW

    class Meta:
        model = ViaPraetoriaUserProfile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'date_of_birth': forms.DateInput(attrs={'min': '1920-01-01'}),
        }


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        pass
        # Not good
        # # should be done with signals
        # # because this breaks the abstraction of the auth app
        # pets = list(self.instance.pet_set.all())
        # PetPhoto.objects.filter(tagged_pets__in=pets).delete()
        # self.instance.delete()
        #
        # return self.instance

    class Meta:
        model = ViaPraetoriaUserProfile
        fields = ()
