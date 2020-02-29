from rest_framework import viewsets

from .models import Movie
from .serializers import MovieSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "genre": openapi.Schema(type=openapi.TYPE_STRING),
            "year": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)
class MovieViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
