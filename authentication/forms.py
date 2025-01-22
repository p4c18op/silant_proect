from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import Group
from authentication import models
from django.contrib.auth.password_validation import validate_password


"""USERS FORMS"""
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    patronymic = forms.CharField(required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # Получение значения роли из формы
        role = 'Пользователь'

        if commit:
            user.save()

            # Получение или создание группы на основе выбранной роли
            user_group, created = Group.objects.get_or_create(name=role)
            # Добавление пользователя в группу
            user.groups.add(user_group)

        return user

    class Meta:
        model = models.CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'email',
        )


class UserPasswordChangeForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput())

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError({"password1": "Пароли должны совпадать!"})

        return super().clean()

    def save(self, commit=False):
        id = self.cleaned_data['id']
        password1 = self.cleaned_data['password1']

        models.CustomUser.objects.change_password(id, password1)

        return super(UserPasswordChangeForm, self).save(commit=False)

    class Meta:
        model = models.CustomUser
        fields = ('id', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'patronymic', 'email',]
