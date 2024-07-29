# Django Rep

<img src="./cat-in-box.svg" style="height:500px; width:500px;">

## Road Map

1. Setup
2. Toy Resource

## 1. Setup

This lesson continues to build-out Cat Collector right where the [One to Many Models](/catcollector/one-to-many-models/README.md) lesson left off.

Navigate to the django-catcollector directory, enter your virtual environment pipenv shell, then start the web server with python manage.py runserver.

You may notice this lesson looks rather short...that's because you are going to do most of the work. The more reps we do, the deeper our understanding becomes. Don't worry, you're not alone!

## 2. Toy Resource

For this lesson we will add a `Toy` model and associated Serializer/CBV’s/URLs.

### Toy Model

Start by adding the `Toy` model to our project. This model has a name and a color field. Set the fields to models.CharField data type with a max_length of 50 and 20, respectively. Don't forget to override the __str__ method to display the toy's name property.

<details>
<summary>
💡 Give it a try! We will review the code in 5 minutes - don't peek!
</summary>

```python
# Add the Toy model
class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name
```
  
</details>

### Admin
A new model means new entry in `**admin.py**`.

<details>
<summary>
💡 Give it a try! We will review the code in 5 minutes - don't peek!
</summary>

```python
from django.contrib import admin

from .models import Cat, Feeding, Toy

admin.site.register(Cat)
admin.site.register(Feeding)
# add the Toy model
admin.site.register(Toy)
```
  
</details>

### Migrations
A new model also means we need to make migrations and migrate.

<details>
<summary>
💡 Do you remember how to do that in our terminal? We will review the code in 5 minutes - don't peek!
</summary>

```bash
python manage.py makemigrations
python manage.py migrate
```
  
</details>

### Serializer
Next stop, serializers.py!

<details>
<summary>
💡 Take a look at the Cat serializer as a reference. We will review the code in 5 minutes - don't peek!
</summary>

```python
from .models import Cat, Feeding, Toy

class ToySerializer(serializers.ModelSerializer):
  class Meta:
    model = Toy
    fields = '__all__'
```
  
</details>

### URLs
You know the drill.

<details>
<summary>
💡 Take a look at the Cat url patterns as a reference - you can follow a similar routing methodology. We will review the code in 5 minutes - don't peek!
</summary>

```python
from .views import Home, CatList, CatDetail, FeedingListCreate, FeedingDetail, ToyList, ToyDetail

urlpatterns = [
  # additional url patterns below
  path('toys/', ToyList.as_view(), name='toy-list'),
  path('toys/<int:id>/', ToyDetail.as_view(), name='toy-detail'),
]
```
  
</details>

### Views
Last but not least, our associated class-based views.

<details>
<summary>
💡 Take a look at the Cat views as a reference. We will review the code in 5 minutes - don't peek!
</summary>

```python
from .models import Cat, Feeding, Toy
from .serializers import CatSerializer, FeedingSerializer, ToySerializer

class ToyList(generics.ListCreateAPIView):
  queryset = Toy.objects.all()
  serializer_class = ToySerializer

class ToyDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Toy.objects.all()
  serializer_class = ToySerializer
  lookup_field = 'id'
```
  
</details>

### Summary
Not too bad!
  
As it stands, our `Toy` model is not associated with any of the other model. In our next lesson, we introduce a new kind of relationship - a many-to-many connection between a `Cat` and `Toy`.
