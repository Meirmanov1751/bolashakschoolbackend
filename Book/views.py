from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from .serializer import BookSerializer
from .models import BookImages, Book


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

# Create your views here.
