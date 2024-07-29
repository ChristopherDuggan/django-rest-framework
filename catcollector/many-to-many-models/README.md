<!-- {% raw %} -->
<img src="https://i.imgur.com/HL5YY8J.png">

# Django Many-to-Many Relationships

## Road Map

1. Setup
2. Many-to-Many Relationships in RDBMs
3. Many-to-Many Relationship in Django
4. Implement the Cat & Toy Association in Cat Collector
5. Practice Exercise
6. Lab Assignment
7. Further Study

## 1. Setup 

Many-to-many relationships require two existing data resources, i.e., two existing Models. For this lesson, we are going to associate a `Cat` Model with a `Toy` model.

Thanks to the previous lesson, [Django Rep](/catcollector/extra-rep/README.md), we can focus on how to implement the actual `Cat >--< Toy` relationship in this lesson.

Let's set ourselves up for this lesson:

1. Move into the `catcollector` project:
    ```
    cd ~/lessons/django-catcollector
    ```
2. Open the project in VS Code:
    ```
    code .
    ```
3. Enter your virtual environment :
    ```
    pipenv shell
    ```
4. Run your server:
    ```
    python manage.py runserver
    ```

## 2. Many-to-Many Relationships in Relational Databases

Unlike MongoDB, which can easily implement both one and many-to-many relationships without much fuss, SQL databases need what is known as a **join table** to implement M:M relationships.

Join tables provide the glue between two other tables in a database.

Each row in the join table contains *foreign keys* for the other two tables’ *primary keys* as diagrammed here:

<img src="https://i.imgur.com/imTYIBl.png">

Note that in practice, the “associating” of a cat and toy is a matter of adding an additional row in the join table. Similarly, to “unassociate” a cat and toy, the corresponding row in the join table is deleted - not a cat row, not a toy row!

## 3. Many-to-Many Relationship in Django

As usual, the Django framework will handle the heavy lifting when it comes to working with many-to-many relationships between Models.

To implement a many-to-many relationship in the database using Django we:

1. Add a `ManyToManyField` on **one** of the Models
2. Create the migration and migrate it to update the database

Using a `ManyToManyField` causes Django to automatically create a hidden join table used to implement the M:M association.

### Add a `ManyToManyField` on One Side of the Relationship

To create a M:M relationship between two models, we need to add a `ManyToManyField` on one of them.

Django will still ensure that we can traverse data from both models to the related model, but we get to pick the name for the relationship attribute on the model we choose to add `ManyToManyField` to.

We more commonly be accessing a cat’s toys, than a toy’s cats, so we’ll add the new attribute to the `Cat` model:

```python
class Cat(models.Model):
  name = models.CharField(max_length=100)
  breed = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  # Add the M:M relationship
  toys = models.ManyToManyField(Toy)
```

> 👀 It definitely makes sense to name that attribute plurally because a cat can have many toys.

<aside>
⚠️ If you see an error like this

![Error Message](./error_message.png)

or linting like this

![Linting Error](./linting_error.png)

You need to move your `Toy` model ABOVE your `Cat` model! You will need to do the same when we update the `Cat` serializer.

</aside>

### Make and Run the Migration

Because we've made a change to a Model that impacts the database's schema, we must make a migration and migrate it to update the database.

#### 👉 You Do - Make and Apply the Migration (1 min)

You got this!

<details>
<summary>
Try not to peek!
</summary>
<hr>

First, make the migration:

```
python manage.py makemigrations
```

Migrate the created migration to update the schema:

```
python manage.py migrate
```

<hr>
</details>

> 👀 When working in a group, only one team member would have to creat a new model and run `python manage.py makemigrations`.  Then, you would have received that new migration via syncing your code with the project repo where you would then migrate the newly received migration file.

We need a few more steps before we are ready to test drive the new relationship.

## 4. Implement the Cat & Toy Association in Cat Collector

### User Stories

> _As a User, when viewing the detail page of a cat, I want to see a list of toys the cat has._

and

> _As a User, when viewing the detail page of a cat, I want to be able to add a toy from a list of toys that the cat doesn't already have._

That is, when accessing a single cat we want to see a list of toys associated with the cat AND a list of unassociated toys.

### Displaying a List of Associated Toys

Displaying a cat's toys is just a matter of updating the `Cat` serializer:

```python
class CatSerializer(serializers.ModelSerializer):
  fed_for_today = serializers.SerializerMethodField()
  toys = ToySerializer(many=True, read_only=True) #add this line

  class Meta:
    model = Cat
    fields = '__all__'

  def get_fed_for_today(self, obj):
    return obj.fed_for_today()
```

This modification will serialize the related `Toy` instances whenever a `Cat` instance is serialized. The **read_only=True** parameter in the ToySerializer inside CatSerializer ensures that toys are not required when creating a Cat.

> Note: Make sure to move the ToySerializer above the CatSerializer to avoid any errors.

### Displaying a List of Unassociated Toys

When we query for one cat, we want to make sure we also display toys that the cat is **not** associated with. In order to do that, we will need to update the `Cat` Detail View.

To be able to display the list of unassociated toys, we'll need to query for them in the `CatDetail` view function and add them to the context (data) being passed to the template.

The following query to find all toys that a cat doesn't have is a bit complicated, but it demonstrates the power of the Django ORM.

In **views.py** update `CatDetail as follows`:

```python
class CatDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Cat.objects.all()
  serializer_class = CatSerializer
  lookup_field = 'id'

  # add (override) the retrieve method below
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
```

The object manager's `exclude` method is like `filter` except that it is used to return objects that don't meet the criteria.

The Django Query API enables [Field Lookups](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups) for every field in the model. `id__in` is one such field lookup that checks if the model's `id` is in a list and that list is being created with this code:

```python
  toys_not_associated = Toy.objects.exclude(id__in=instance.toys.all())
```

Finally, we are will respond with JSON that includes the cat instance along with information on the list of unassociated toys.

### Making the Association

The api is looking good and all that's left is to handle a way to associate a toy with the cat.

To do this, the server needs to know the `id` of **both** the cat and the toy being associated.

Let's first add a new routes with a URL pattern that includes both `id`s in **urls.py**:

```python
  path('cats/<int:cat_id>/add_toy/<int:toy_id>/', AddToyToCat.as_view(), name='add-toy-to-cat'),
```

As you can see, we've created two route parameters:  `cat_id` and `toy_id`.

Now let's make sure to generate the respective view. Keep in mind, in order to hit this route we should make **POST** request.

In **views.py**:

```python
class AddToyToCat(APIView):
  def post(self, request, cat_id, toy_id):
    cat = Cat.objects.get(id=cat_id)
    toy = Toy.objects.get(id=toy_id)
    cat.toys.add(toy)
    return Response({'message': f'Toy {toy.name} added to Cat {cat.name}'})
```

Congrats on implementing a many-to-many relationship between cats and toys!

## 5. 💪 Practice Exercise (15 minutes)

Implement the **RemoveToyFromCat** url pattern and view:

Hint:

- "Unassociating" a toy is VERY much the same process as the Associating process we just implemented.

<details>
<summary>
👀 Don't peek! Solution below.
</summary>

Create the url pattern:
```python
  path('cats/<int:cat_id>/remove_toy/<int:toy_id>/', RemoveToyFromCat.as_view(), name='remove-toy-from-cat'),
```

Create the view:
```python
class RemoveToyFromCat(APIView):
  def post(self, request, cat_id, toy_id):
    cat = Cat.objects.get(id=cat_id)
    toy = Toy.objects.get(id=toy_id)
    cat.toys.remove(toy)
    return Response({'message': f'Toy {toy.name} removed from Cat {cat.name}'})
```
  
</details>

## 6. Lab Assignment

Lab time is to be spent implementing the same feature in your Finch Collector project 🦜. 

> Note: If you had a little trouble following along with the catcollector walkthrough, please review the completed code included in this repository.

## 7. Further Study

Although Django automatically creates a "hidden" join table to implement a many-to-many relationship, there are times where it would be beneficial to be able to add additional attributes to that join table.

As an example, a `Ticket` Model provides the role of a join table between a `Concert` and a `Customer`:

```
Concert --< Ticket >-- Customer
```

In essence, a _Concert has many Customers through Tickets_

Further, a _Customer has many Concerts through Tickets_

Django includes a `through` kwarg to pull this type of relationship off.

```python
class Concert(models.Model):
    name = models.CharField(max_length=100)
    # other attributes here

class Customer(models.Model):
    name = models.CharField(max_length=50)
    # other attributes here
    concerts = models.ManyToManyField(Concert, through='Ticket')

class Ticket(models.Model):
	 seat = models.CharField(max_length=20)
	 # other attributes here
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
```

For more information regarding _many-to-many through relationships_, start [here](https://docs.djangoproject.com/en/4.1/topics/db/models/#intermediary-manytomany) in the docs.

## References

[Examples of CRUD with Many-to-Many Relationships](https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/)
<!-- {% endraw %} -->
