from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UserChangeForm
)
from .models import Contact, User
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from core.tasks import send_registration_email_task


class AuthenticationFormWithCaptchaField(AuthenticationForm):
    captcha = ReCaptchaField(
        public_key='6Le6CNkdAAAAAM0erjmCJJ_YW_tnVDhfFmvYHEQX',
        private_key='6Le6CNkdAAAAAKUVozivgonzS4yEnlfH8Ai0Ck2Y',
    )


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(
        public_key='6Le6CNkdAAAAAM0erjmCJJ_YW_tnVDhfFmvYHEQX',
        private_key='6Le6CNkdAAAAAKUVozivgonzS4yEnlfH8Ai0Ck2Y',
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        )

    def send_registration_email(self):
        send_registration_email_task.delay(
            self.cleaned_data['first_name'],
            self.cleaned_data['last_name'],
            self.cleaned_data['username'],
            self.cleaned_data['email']
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False # REMOVE LINE TO ALLOW USERS AUTO ACCESS TO APP
        if commit:
            user.save()
            return user


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'password',
            'email'
        )

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.password = self.cleaned_data['password']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(
        public_key='6Le6CNkdAAAAAM0erjmCJJ_YW_tnVDhfFmvYHEQX',
        private_key='6Le6CNkdAAAAAKUVozivgonzS4yEnlfH8Ai0Ck2Y',
    )

    class Meta:
        model = Contact
        fields = (
            'fullname',
            'contact_email',
            'contact_subject',
            'contact_message'
        )

    def save(self, commit=True):
        contact = super(ContactForm, self).save(commit=False)
        contact.fullname = self.cleaned_data['fullname']
        contact.contact_email = self.cleaned_data['contact_email']
        contact.contact_subject = self.cleaned_data['contact_subject']
        contact.contact_message = self.cleaned_data['contact_message']
        if commit:
            contact.save()
            return contact
