<!-- {% raw %} -->
<img src="https://i.imgur.com/s8QeOpo.png">

# Intro to Django Models and Serializers

## Road Map

1. Setup
2. The Model Layer in the Django Architecture
3. What's a Model?
4. Models in Django
5. Making and Running Migrations
6. Performing CRUD Using Django's ORM
7. I am the Admin!
8. Serializers
9. Using the `Cat` Model in Cat Collector
10. Lab
11. Further Reading

## 1. Setup

The code for this lesson picks up right where we left off in the [Setup, URLs, & Views_](https://git.generalassemb.ly/SEB-Base-Curriculum/django-setup-urls-views) lesson.

Navigate to your django-catcollector directory and enter your virtual environment by running ```pipenv shell``` in your terminal. Make sure to open your code editor and run your django server.

## 2. The Model Layer in the Django Architecture

<img src="./mvt-pattern.png">
	
This lesson focuses on the **Model layer** which provides **Views** with access to the **database**.

## 3. What's a Model?

**Models** are used to perform CRUD data operations on a database.

Remember ***entities*** in the Entity-Relationship-Diagrams?

Well, a Django Model represents a single entity from the *ERD*.

Thus, a Model has a one-to-one mapping with a table in the database and is used to perform Create, Read, Update and Delete (CRUD) data operations on that table.

When we retrieve data from the database (using a Model of course), we will have **model objects**, each of which represents a row in a database table. Model objects are also called *instances* of the Model. We can work with these instances of the Model just like how we worked with Mongoose documents.

Here's our final ERD for Cat Collector:

![Final ERD](./final-erd.png)

We can update and render the attributes of these **objects** in the same way we worked with Mongoose documents.

## 4. Models in Django

Each Model is defined as a Python class that inherits from `django.db.models.Model`.

Here's the **Cat** entity from an ERD and the code to define the equivalent Model:

<img src="https://i.imgur.com/gwlOAXc.png">

All of the Models for an app are defined in the app’s `models.py` file.

Let’s create the `Cat` Model by adding the code from the above image in
`main_app/models.py`!

Note that each field (attribute) is represented by a Field class, e.g., `CharField`. Here are the **[docs of available Field types](https://docs.djangoproject.com/en/4.2/ref/models/fields/#model-field-types)** - there’s plenty of options.

It’s important to note that the Field types for a Model determine the column’s data type in the table.

### ❓ Review Questions (1 min)

<details>
<summary>
In Django, what is used to perform CRUD database operations?
</summary>
<hr>

**A Model**

<hr>
</details>

<details>
<summary>
How is a Model defined in Django?
</summary>
<hr>

**As a Python class that inherits from `models.Model`**

<hr>
</details>

<details>
<summary>
An ERD Entity maps to a _____ in Django, which maps to a _____ in the database.
</summary>
<hr>

An ERD Entity maps to a **Model** in Django, which maps to a **table** in the database.

<hr>
</details>

## 5. Making and Running Migrations

### What are Migrations?

[Migrations](https://docs.djangoproject.com/en/4.1/topics/migrations/) are used to synchronize a database's schema with the project's Models.

Migrations are used to evolve a database over time - as the requirements of the application change.  However, they can be "destructive" (cause a loss of data), so be careful with migrations if you're working with an application in _production_.

Migrations in Django are Python files that are created by running a command Django in Terminal and are stored in a folder named **migrations**.

### Making Migration Files

Okay, we’ve defined a `Cat` Model, but the database does not yet have a table to hold all of our furry model instances (rows).

Run the following command in the **Web Container Shell** to create migration files for all Models that have been added or changed since the last migration:

```bash
python manage.py makemigrations
```

The output in the terminal informs us that the following migration file was created: `main_app/migrations/0001_initial.py`

A `migrations` directory is created for an **app** the first time you run `makemigrations`.

You don’t have to do anything with the migration files, but since this is the first time we’ve made one, let’s open it and take a peek.

> 🤯 You shouldn’t ever need to edit migration files by hand, but it’s entirely possible to do so if you needed to.

### Running Migrations

Simply creating migration files does not update the database's schema.

To check the status of migration files, run the following:

```
python manage.py showmigrations
```

At this point, the unchecked migrations are pending and have **not** (yet) been applied to the database. We, must use the `migrate` command to apply these pending migrations and update the database:

```
python manage.py migrate
```

`OK` messages are a good thing 😊 

A good way to remember (and to differentiate) what these two commands do, is by comparing them to these git commands: 

- ***makemigrations*** ==> add/commit 
- ***migrate*** ===> push

### ❓ Review Questions (1 min)

<details>
<summary>
What are used to update a database's schema over time as an application's functionality evolves?
</summary>
<hr>

**Migrations**

<hr>
</details>

<details>
<summary>
When is it necessary to make and run migrations?
</summary>
<hr>

**Whenever a Model is added or updated in a way that impacts the database's schema.**

<hr>
</details>

## 6. Performing CRUD Using Django's ORM

### What's an ORM?

ORM stands for Object-Relational-Mapper.

It's called an ORM because it turns rows in a relational database into Python objects and vice-versa. SQL to Python & Python to SQL

The ORM allows developers to write object-oriented code to "C.R.U.D" data instead of having to write SQL directly. ORMs save us time and make application developers more productive.

The fact is, Django's ORM can generate SQL that, *even the most **experienced** developer* would struggle to write.

Another benefit is that the ORM provides a level of abstraction that enables us to write the same Python code to manipulate our data, regardless of which database engine is being used! Yes, it's even possible to use MongoDB with Django!

### Django "Objects" (Terminology)

Django refers to **objects** throughout its documentation.

A Django Object is:

- An instance of a Django Model
- A row in the database

### Django's ORM

The Django ORM is automatically going to generate a *plethora* of methods for each Model.

Django's ORM includes methods for performing:

- Filtering (querying based on criteria)
- Ordering
- Even accessing the data from related Models!

Django refers to the ORM functions available as its: [**database API**](https://docs.djangoproject.com/en/4.1/topics/db/queries/). Additional documentation can be [found here](https://docs.djangoproject.com/en/4.1/ref/models/).

### Performing CRUD in a Python Interactive Shell

After creating a new Model, you can take it for a test drive by using the built-in Python shell that helps to load the Django environment:

```
python manage.py shell
```

Now, you should see a `>>>` prompt. Let's type out some commands. 

Any model you want to work with must be imported just like you will have to do in the application:

```python
>>> from main_app.models import Cat
```

> 💡 Key Point: The code we type in the shell to perform CRUD is going to be the same or extremely similar to the code we use in the application’s views, so even though we’re working in the shell start internalizing some of this so that you can apply it in your apps!

To retrieve all of the Cat objects, enter this command:

```python
>>> Cat.objects.all()
<QuerySet []>
```

### The Django Model Manager

Any time you want to perform query operations on a **Model** to retrieve *model objects* (rows) from a database table, it is done via a **Manager** object.

By default, Django adds a Manager to every Model class - this is the `objects` attribute attached to `Cat` above.

### **The `<QuerySet>`**

The `<QuerySet []>` returned represents a database query that can be refined by chaining additional methods to it.

Ultimately though, when the app needs the data, for example, to iterate over cats, the query will be sent to the database and the result is a list-like object that represents a collection of model instances (rows) from the database.

Besides `Cat.objects.all()`, let’s see some of the other common ORM operations…

### Give Me a "C"

Here's how we can **create** an in-memory object (an instance of a Model), and then save it to the database:
 
```python
>>> c = Cat(name="Biscuit", breed='Sphinx', description='Evil looking cuddle monster. Hairless', age=2)
>>> c.__dict__ 
```
Those are double-underscores on either side of dict.

EXPECTED OUTPUT:
```
{'state':...., 'id': None, 'name': 'Biscuit', 'breed': 'Sphinx',
 'description': 'Evil looking cuddle monster. Hairless', 'age': 2}
```

As you can see, we pass the data for the model's attributes as [kwargs](https://www.w3schools.com/python/gloss_python_function_arbitrary_keyword_arguments.asp).

> 👀 FYI: The model currently has `None` as its `id` because it is not yet saved to the database.

```python
>>> c.save()
>>> c.id
1
```

Calling the `save()` method on an object saves it to the database.

Run `Cat.objects.all()` again and you'll see a `Cat` object exists now:

```python
>>> Cat.objects.all()
<QuerySet [<Cat: Cat object (1)>]>
```

### 👉 You Do - Create Another Cat (2 mins)

- Create another `Cat` with attribute values of your choice.

- Since there's no reason we need to remember the current cat object held by the variable `c`, feel free to re-use that variable.

- Check that your cat was added by using `Cat.objects.all()`.

### Adding a `__str__` Method

It's a best practice to override the `__str__` method in Models so that they will print in a more helpful way.

For the `Cat` model, we'll code `__str__` to return the cat's `name` attribute:

```python
# main_app/models.py
...
  age = models.IntegerField()

  # new code below
  def __str__(self):
    return self.name
```

Changes made to a Model do not become active in the shell unless you `exit()`, re-launch, and re-import the Models...

### 👉 You Do - Reload the Shell (1 min)

- `exit()` or `ctrl + D` to exit the current shell.
- Relaunch the shell (see above)
- Import the `Cat` Model (see above)

## Give Me a “R”

If you call `Cat.objects.all()` again you’ll see a `Cat` object exists now:

```python
Cat.objects.all()
```

`<QuerySet [<Cat: Biscuit>]>` should be returned!

We’re reading cats!

### Give Me a "U"

The attributes can be updated by simply assigning the new values then calling the object's `save()` method:

```python
>>> from main_app.models import Cat
>>> c = Cat.objects.first()
>>> c
<Cat: Biscuit>
>>> c.name = 'Rubber Biscuit'
>>> c.save()
>>> c
<Cat: Rubber Biscuit>
```

We've updated a cat!

### Filtering (querying) for Records

We can use [objects.filter()](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#filter) to query a Model's table for data that matches certain criteria. This is very similar to how we used Mongoose's `find()` method.

For example, the query below would return **all** cats *with* the name "Rubber Biscuit":

```python
>>> Cat.objects.filter(name='Rubber Biscuit')
<QuerySet [<Cat: Rubber Biscuit>]>
```

<details>
<summary>
❓ The <code>name='Rubber Biscuit'</code> is not a Python comparison expression, it's a Python _____.
</summary>
<hr>

**kwarg**

<hr>
</details>

Using `objects.filter()` and `objects.exclude()` is similar to writing a `WHERE` clause in SQL.

The Django ORM creates several helpful [Field lookups](https://docs.djangoproject.com/en/4.1/topics/db/queries/#field-lookups).

For example, if we wanted to query for *all* cats *whose* names _contain_ a certain string:

```python
>>> Cat.objects.filter(name__contains='Bis')
<QuerySet [<Cat: Rubber Biscuit>]>
```
The above code will elicit the same result as an SQL query like this:

```sql
SELECT * FROM main_app_cat WHERE name LIKE '%Bis%';
```

As another example, here's how we can find: cats that have an age _equal to or less than_ 3:

```python
>>> Cat.objects.filter(age__lte=3)
<QuerySet [<Cat: Biscuit>]>
```

For basic lookups, the format is:  `field__lookuptype=value` (that's a double underscore).

Filters can even be chained!

Like most things in SEB, learning how to use `filter()` will take practice.

### Reading a Single Record

You've seen how `Cat.objects.all()` and `Cat.objects.filter()` returns a list of objects.

However, it's a very common data operation to read one specific model object from the table based on some provided value, usually its `id`. 

Instead of the `objects.all()` method, we can use the [objects.get()](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#get) method instead to read a single object:

```python
Cat.objects.get(id=1)
```

The `get()` method can also be called with multiple `field=value` arguments to query multiple columns.

Be sure to use error handling if there's a chance that `get()` won't find what you're looking for because if Django doesn't find it, an error is raised.

### What About Ordering (sorting)?

Similar to what you saw in SQL, there's an "[order_by](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#order-by)" method:

```python
>>> Cat.objects.order_by('age')
``` 

Or in descending order:

```python
>>> Cat.objects.order_by('-age')
```

The `<QuerySet>` object can be indexed and sliced (like other sequences) too.

Poor old cat:

```python
>>> Cat.objects.order_by('-age')[0]
```

## 7. I am the Admin!

But wait, there's another really REALLY neat thing about Django - it comes with a built-in Administration functionality! Remember that `django.contrib.admin` in the `INSTALLED_APPS`? Time to use that app!

First though, we need a **super user**.

A super user is an administrator for the site that can access the Admin app to view and manipulate the data in the database.

Run this command in the terminal to create the super user:

```
python manage.py createsuperuser
```

You will be prompted to enter a username, email address, and a password. Enter a simple username, SKIP the email address by hitting Enter, Django will want you to create a password that's complex, make a simple password like `1111` and then you can bypass the password warning by typing `y` at the warning prompt.

Now go to your browser and type `localhost:8000/admin` to access the administration portal (make sure your server is running)!  

Did you mess up your password? It's okay - no sweat...go back to your Terminal and use this handy command:

```
python3 manage.py changepassword <user_name>
```

We won't initially see Cats in the admin portal because the admin app doesn't know about Models in the project unless they are first "registered" with it.

We register our Models in the `main_app/admin.py` file:

```python
from django.contrib import admin
# import your models here
from .models import Cat

# Register your models here
admin.site.register(Cat)
```

No need to restart the server - just refresh that beautiful portal!

We can add, edit, and remove data objects anytime we need to by browsing to `/admin` - neat!


## 8. Serializers

Now it's time to set up our serializers! Here's a recap of what serializers are from the Django REST documentation:

> Serializers allow complex data such as querysets and model instances to be converted to native Python data types that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.

We have already installed Django REST Framework (check your pipfile) and included it in the list of `INSTALLED_APPS`.

Next, we'll set up our serializers by creating serializers.py in the main_app folder:

```py
from rest_framework import serializers
from .models import Cat

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'
```

## 9. Using the `Cat` Model in Cat Collector

Time to add some of this ORM magic to Cat Collector!

### Typical Process to Add Functionality to an App

Remember, nothing is going to happen unless an HTTP request leaves the browser informing the server what the app wants to do.

When adding additional functionality to a web app we need to do the following:

1. With Django, decide the appropriate URL for the route. Because Django does not follow the RESTful routing methodology, you are free to name the URLs as you see fit.
2. Code the route on the server. In the case of Django, this is done by adding an additional `path(...)` to the `urlpatterns` list within the app’s `**urls.py**` module. **Each entry in `urlpatterns` determines what code will run when the URL matches an HTTP request**.
3. Now you need to add the *view function* referenced by the `path(...)` inside of the `**views.py**` module. The *view function* contains the code to perform CRUD, etc. It ultimately is responsible for responding to the client’s request…

Make it a habit to follow the steps above anytime you need new functionality in your app. Let's recap:

- Step 1: Determine the proper route
- Step 2: Define the route
- Step 3: Code the view

> Note: The __view__ logic will use the `Cat` Model and appropriate serializer to perform CRUD operations and send JSON to the client, respectively

#### Step 1 - Determine the Proper Route

In Django, we don't worry about the HTTP method when determining the "proper" route for a feature.

So what should the path be for viewing all cats or a single cat?

Once again, we can use a RESTful path:

```
/cats/
/cats/:id/
```

We'll see how to define that route parameter Django style in Step 2.

#### Step 2 - Define the Route

Add route entries to the `urlpatterns` list in ***main_app/urls.py*** (we don't have views to point to, but you can name them now and create them after):

```python
from django.urls import path
from .views import Home, CatList, CatDetail # additional imports

urlpatterns = [
  path('', Home.as_view(), name='home'),
  # new routes below 
  path('cats/', CatList.as_view(), name='cat-list'),
  path('cats/<int:id>/', CatDetail.as_view(), name='cat-detail'),
]
```

In Django, we use angle brackets to declare a _URL parameter_ to capture values within the _segments_ of a URL as follows.

The `int:` part is called a "converter" and it's used to match and convert the captured value from a string into, in this case, an integer.

If the data in the segment does not look like an integer, then it will not be matched - this is different than what we saw in Express where URL parameters were always *string values*. 

#### Step 3 - Code the View

As you know, view functions are defined within **views.py**.

Please find the updated views.py file below:

```python
# additional imports below
from rest_framework import generics
from .models import Cat
from .serializers import CatSerializer

class CatList(generics.ListCreateAPIView):
  queryset = Cat.objects.all()
  serializer_class = CatSerializer

class CatDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Cat.objects.all()
  serializer_class = CatSerializer
  lookup_field = 'id'
```

> 👀 Django will pass any captured URL parameters as a named argument to the view function!

What are generics?
- [Django Documentation on Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/) suggest generic views were developed as a shortcut for common usage patterns. They take certain common idioms and patterns found in view development and abstract them so that you can quickly write common views of data without having to repeat yourself.

Let's break down the views above:
- CatList is a view that handles GET requests for a list of cats and POST requests to create a new cat.
- CatDetail is a view that handles GET, PUT, PATCH, and DELETE requests for a single cat, identified by its ID.

<details>
<summary>
❓ What determined the parameter name of <code>id</code> in the view function?
</summary>
<hr>

**The route parameter in urls.py:**
<br>
<code>cats/&lt;int:id&gt;/</code>
<br>

<hr>
</details>

👏 **Congrats on coding the Django `Cat` Model and Serializer; as well as the updated url patterns and view functionality for the Cat Collector. We now have full CRUD on the cat model!**

Feel free to test each route on Postman.

## 10. Lab

For practice, do everything we did in this lesson on your Finch Collector project!

Don't forget to make commits.

## 11. Further Reading
#### Customizing Class-based Views
Class-based Views are classes defined in the Django framework that we can extend and use instead of view functions.

So, we now know that Django provides us with a set of very useful classes that make development in Django easier and more productive.

You should consider class-based views as the go to vs. function-based views.

There might come a time though, when you might believe that class-based views can't be used in situations that require more flexibility. However, Django's class-based views are designed to be easily customizable by overriding their methods and assigning values to attributes.

Your app's requirements may, or may not, need to depend upon customization of the built-in CBVs, however, you should take time to investigate the variety of options.

### Resources

[Django Model API](https://docs.djangoproject.com/en/4.1/ref/models/)

<!-- {% endraw %} -->
