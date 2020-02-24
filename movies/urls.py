from django.urls import path

from .views import MovieViewSet

movie_list = MovieViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
movie_detail = MovieViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path("api/movies/", movie_list),
    path("api/movies/<int:pk>/", movie_detail),
]
