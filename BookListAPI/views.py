from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Bookitem
from .serializers import BookSerializer
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

# Create your views here.
@api_view(['GET','POST'])
def books(request): 
    return Response('list of the books', status=status.HTTP_200_OK)

class BookList(APIView): 
    def get(self, request): 
        author = request.GET.get('author')
        # visit eg http://localhost:8000/api/books/?author=hammingway
        if(author):
            return Response({"message":"list of the books by " + author}, status.HTTP_200_OK)
        return Response({"message":"list of the books"}, status.HTTP_200_OK)
    def post(self, request): 
        return Response({"message":"new book created"}, status.HTTP_201_CREATED)

class Book(APIView): 
    def get(self, request, pk): 
        return Response({"message":"single book with id " + str(pk)}, status.HTTP_200_OK)
    def put(self, request, pk): 
        return Response({"title":request.data.get('title')}, status.HTTP_200_OK)

# class BookView(generics.ListCreateAPIView):
#     queryset = Bookitem.objects.select_related('category').all()
#     serializer_class = BookSerializer

class SingleBookView(generics.RetrieveUpdateAPIView):
    queryset = Bookitem.objects.all()
    serializer_class = BookSerializer

@api_view()
def BookView(request): 
    items = Bookitem.objects.select_related('category').all()
    serialized_items = BookSerializer(items, many=True)
    return Response(serialized_items.data)
    
@csrf_exempt
def books(request):
    if request.method == 'GET':
        books = Bookitem.objects.all().values()
        return JsonResponse({"books":list(books)})
    elif request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        book = Book(
            title = title,
            author = author,
            price = price
        )
        try:
            book.save()
        except IntegrityError:
            return JsonResponse({'error':'true','message':'required field missing'},status=400)

        return JsonResponse(model_to_dict(book), status=201)