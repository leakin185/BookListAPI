from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Bookitem
from .serializers import BookSerializer
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Category 
from .serializers import CategorySerializer
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes

# Create your views here.

@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data) 

# class BookView(generics.ListCreateAPIView):
#     queryset = Bookitem.objects.select_related('category').all()
#     serializer_class = BookSerializer

@api_view(['GET', 'POST'])
def BookView(request): 
    if request.method == 'GET':
        items = Bookitem.objects.select_related('category').all()
        serialized_items = BookSerializer(items, many=True, context={'request': request})
        return Response(serialized_items.data)
    if request.method == 'POST': 
        serialized_items = BookSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status=status.HTTP_201_CREATED)

class SingleBookView(generics.RetrieveUpdateAPIView):
    queryset = Bookitem.objects.all()
    serializer_class = BookSerializer

@api_view() 
@renderer_classes ([TemplateHTMLRenderer])
def Book(request):
    items = Bookitem.objects.select_related('category').all()
    serialized_item = BookSerializer(items, many=True)
    return Response({'data':serialized_item.data}, template_name='book-item.html')

# old ways of doing it
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

# class Book(APIView): 
#     def get(self, request, pk): 
#         return Response({"message":"single book with id " + str(pk)}, status.HTTP_200_OK)
#     def put(self, request, pk): 
#         return Response({"title":request.data.get('title')}, status.HTTP_200_OK)