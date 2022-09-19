from .permissions import IsOwnerOrReadOnly
from .models import Book, BookInstance
from .serializers import BookSerializer, BookInstanceSerializer
from rest_framework import viewsets


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]


class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    # permission_classes = [IsOwnerOrReadOnly]