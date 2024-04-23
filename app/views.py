from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, RecordCreateForm
from .models import Record

# Create your views here.


def home(request):
    # if request.user.is_authenticated:
    records = Record.objects.all()

    return render(request, 'home.html', {'records': records})


def user_login(request):
    # if request.user.is_authenticated:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In ')
            return redirect('home')
        else:
            messages.error(request, 'User Not Found')
            return redirect('login')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You Have Been Logged Out')
    return redirect('home')


def user_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You Have Been Successfully Registered')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.warning(request, 'You Must Be Logged In to View That Page')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        if customer_record.delete():
            messages.success(request, 'Record Successfully Deleted')
            return redirect('home')
        else:
            messages.success(request, 'Something Went Wrong!')
            return redirect('home')
    else:
        messages.success(request, 'Authorizatio Needed For This Operation')
        return redirect('home')


def add_record(request):
    form = RecordCreateForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record Added')
                return redirect('home')
        return render(request, 'add_record.html', {"form": form})
    else:
        messages.success(request, 'Authorizatio Needed For This Operation')
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = RecordCreateForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Has Been Updated')
            return redirect('home')

        return render(request, 'update_record.html', {"form": form})
    else:
        messages.success(request, 'Authorizatio Needed For This Operation')
        return redirect('home')
