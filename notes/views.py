from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, NoteForm
from .models import Note

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/notes')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/notes')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def notes(request):
    user_notes = Note.objects.filter(user=request.user)
    return render(request, 'notes.html', {'user_notes': user_notes})

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('/notes')
    else:
        form = NoteForm()
    return render(request, 'add_note.html', {'form': form})
