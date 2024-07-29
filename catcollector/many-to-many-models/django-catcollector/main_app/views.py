from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cat, Feeding, Toy
from .serializers import CatSerializer, FeedingSerializer, ToySerializer

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the cat-collector api home route!'}
    return Response(content)

class CatList(generics.ListCreateAPIView):
  queryset = Cat.objects.all()
  serializer_class = CatSerializer

class CatDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Cat.objects.all()
  serializer_class = CatSerializer
  lookup_field = 'id'

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    # Get the list of toys not associated with this cat
    toys_not_associated = Toy.objects.exclude(id__in=instance.toys.all())
    toys_serializer = ToySerializer(toys_not_associated, many=True)

    return Response({
        'cat': serializer.data,
        'toys_not_associated': toys_serializer.data
    })

class FeedingListCreate(generics.ListCreateAPIView):
  serializer_class = FeedingSerializer

  def get_queryset(self):
    cat_id = self.kwargs['cat_id']
    return Feeding.objects.filter(cat_id=cat_id)
  
  def perform_create(self, serializer):
    cat_id = self.kwargs['cat_id']
    cat = Cat.objects.get(id=cat_id)
    serializer.save(cat=cat)

class FeedingDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = FeedingSerializer
  lookup_field = 'id'

  def get_queryset(self):
    cat_id = self.kwargs['cat_id']
    return Feeding.objects.filter(cat_id=cat_id)

class ToyList(generics.ListCreateAPIView):
  queryset = Toy.objects.all()
  serializer_class = ToySerializer

class ToyDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Toy.objects.all()
  serializer_class = ToySerializer
  lookup_field = 'id'

class AddToyToCat(APIView):
  def post(self, request, cat_id, toy_id):
    cat = Cat.objects.get(id=cat_id)
    toy = Toy.objects.get(id=toy_id)
    cat.toys.add(toy)
    return Response({'message': f'Toy {toy.name} added to Cat {cat.name}'})

class RemoveToyFromCat(APIView):
  def post(self, request, cat_id, toy_id):
    cat = Cat.objects.get(id=cat_id)
    toy = Toy.objects.get(id=toy_id)
    cat.toys.remove(toy)
    return Response({'message': f'Toy {toy.name} removed from Cat {cat.name}'})
