from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def models(request):
    return render(request, 'models.html')


def reviews(request):
    return render(request, 'reviews.html')


def team(request):
    return render(request, 'team.html')


def contacts(request):
    return render(request, 'contacts.html')


def account(request):
    return render(request, 'account.html')
