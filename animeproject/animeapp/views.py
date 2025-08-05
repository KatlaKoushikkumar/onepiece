from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Anime, Comment, WatchList
from .forms import SimpleSignupForm
from django.contrib.auth.decorators import login_required

def home(request):
    query = request.GET.get('q')
    if query:
        animes = Anime.objects.filter(title__icontains=query)
        if not animes.exists():
            return render(request, 'home.html', {
                'animes': [],
                'search_query': query,
                'not_found': True
            })
    else:
        animes = Anime.objects.all()

    return render(request, 'home.html', {
        'animes': animes,
        'search_query': query,
        'not_found': False
    })

def anime_detail(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    comments = Comment.objects.filter(anime=anime)
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST['comment']
        Comment.objects.create(user=request.user, anime=anime, content=content)
        return redirect('anime_detail', anime_id=anime_id)
    return render(request, 'anime_detail.html', {'anime': anime, 'comments': comments})

def signup_view(request):
    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SimpleSignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(request, username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def watchlist_view(request):
    watchlist = WatchList.objects.filter(user=request.user)
    return render(request, 'watchlist.html', {'watchlist': watchlist})

@login_required
def add_to_watchlist(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    WatchList.objects.get_or_create(user=request.user, anime=anime)
    return redirect('anime_detail', anime_id=anime_id)

def anime_list(request):
    # Sample anime data (later you can fetch from your model)
    animes = [
        {"title": "One Piece", "image": "onepiece.jpg"},
        {"title": "Demon Slayer", "image": "demonslayer.jpg"},
        {"title": "Attack on Titan", "image": "aot2.jpg"},
        # Add more...
    ]
    return render(request, 'anime_list.html', {'animes': animes})
