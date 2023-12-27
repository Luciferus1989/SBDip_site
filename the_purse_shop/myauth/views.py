from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django import forms
from django.http import HttpResponse, HttpRequest
from django.views.generic import CreateView
from django.contrib import messages


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('shopapp:home')

        return render(request, 'myauth/login.html')

    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        user = authenticate(request, username=username_or_email, password=password)
        if not user:
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                pass

        if user:
            login(request, user)
            return redirect('shopapp:home')
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'myauth/login.html', {'messages': messages.get_messages(request)})

    # return render(request, 'login.html')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse('shopapp:home'))


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', forms.ValidationError("Passwords does not matched"))

        return cleaned_data

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #
    #     if commit:
    #         user.save()
    #         group, created = Group.objects.get_or_create(name='Users')
    #         user.groups.add(group)
    #
    #     return user


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('shopapp:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(request=self.request, user=user)
            group, created = Group.objects.get_or_create(name='Users')
            user.groups.add(group)
        # login(request=self.request, user=user)
        # self.object.save()
        # group, created = Group.objects.get_or_create(name='Users')
        # self.object.groups.add(group)
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid form. Please input correct data')
        return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url


