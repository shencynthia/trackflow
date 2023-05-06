from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.

def home(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "sucessful login")
            return redirect('home')
        else: 
            messages.success(request, "invalid login, please try again")
            return redirect('home')

    return render(request, 'home.html', {'records': records})


def logout_user(request):
	logout(request)
	messages.success(request, "you have been logged out")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def single_record(request, pk):
	if request.user.is_authenticated:
		single_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'single_record': single_record})
	else:
		messages.success(request, "user not logged in")
		return redirect('home')

def delete_record(request, pk):
	if request.user.is_authenticated:
		deleting = Record.objects.get(id=pk)
		deleting.delete()
		messages.success(request, "record deleted")
		return redirect('home')
	else:
		return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == 'POST':
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "record added")
				return redirect('home')		
		return render(request, 'add.html', {'form': form})
	else:
		messages.success(request, "please login")
		return redirect('home')	
	
def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "your changes have been applied")
			return redirect('home')
		return render(request, 'update.html', {'form':form})
	else:
		messages.success(request, "please login first")
		return redirect('home')
		    
