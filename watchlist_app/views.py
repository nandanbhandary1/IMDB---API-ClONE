from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
from .models import Movie


def movie_list(request):
    movies = Movie.objects.all()
    data = {"movies": list(movies.values())}
    return JsonResponse(data)


def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    data = {
        "name": movie.name,
        "desc": movie.description,
        "active": movie.active,
    }
    return JsonResponse(data)
