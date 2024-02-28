from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request,'home.html')
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains = searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies':movies})

def about(request):
    return render(request,'about.html')
def statistics_view(request):
    matplotlib.use("Agg")
    years = Movie.objects.values_list('year',flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull = True)
            year = None
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(bar_positions,movie_counts_by_year.values(),width=bar_width,align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions,movie_counts_by_year.keys(), rotation = 90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    #grafico 2
    matplotlib.use("Agg")
    genres = Movie.objects.values_list('genre',flat=True)
    genres = [first.split(',')[0] for first in genres]
    movie_counts_by_genre = {}
    for genre in genres:
        if genre:
            movies_by_genre = Movie.objects.filter(genre__startswith=genre)
        else:
            movies_by_genre = Movie.objects.filter(genre__isnull = True)
            year = None
        count = movies_by_genre.count()
        movie_counts_by_genre[genre] = count
    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_genre))

    plt.bar(bar_positions,movie_counts_by_genre.values(),width=bar_width,align='center')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions,movie_counts_by_genre.keys(), rotation = 90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic2 = base64.b64encode(image_png)
    graphic2 = graphic2.decode('utf-8')

    return render(request,'statistics.html',{'graphic':graphic,"graphic2":graphic2})
def signup(request):
    email = request.GET.get('email')
    return render(request,'signup.html',{'email':email})