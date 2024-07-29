<img src="https://i.imgur.com/TGhY9yA.png">

# Django Authentication

## Road Map

1. Setup
2. Intro to Authentication in Django
3. Creating the `User ---< Cat` Relationship
4. Getting Ready for Auth
5. Update Serializers
6. Establishing Authentication-Related URLs
7. Constructing Authentication Views
8. Summary
9. Lab
10. Further Study - Customizing the `User` Model

## 1. Setup

This lesson continues to build-out Cat Collector right where the [_Django Many-to-Many-Models_](/catcollector/many-to-many-models/README.md) lesson left off.

Open the `~/lessons/django-catcollector` project in VS Code.

Enter your virtual environment:
```
pipenv shell
```

Start the server:
```
python manage.py runserver
```

Okay, let's begin.

## 2. Intro to Authentication in Django

By default, Django creates projects with authentication and authorization capabilities pre-installed!

Two review questions for you...

<details>
<summary>
❓ What is authentication?
</summary>
<hr>

Authentication has to do with the <strong>identity</strong> of the user using your app.

If the user is not logged in, we ofter refer to that user as an <strong>anonymous user</strong> or a <strong>visitor</strong>.

<hr>
</details>

<details>
<summary>
❓ What is authorization?
</summary>
<hr>

<strong>Authorization</strong> pertains to a user's <strong>permission</strong> to access an app's features.

<hr>
</details>

Django's built-in authentication functionality is provided by the `'django.contrib.auth'` app included within the `INSTALLED_APPS` list in `settings.py`:

```python
INSTALLED_APPS = [
    'main_app',
    'django.contrib.admin',
    'django.contrib.auth',    # Thank You Django!
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Django provides the common **username** and **password** type of authentication.

Django relies on server-side sessions, implemented by the `'django.contrib.sessions'` app, to track when a user is logged in or out.

### The `User` Model

At the core of Django's authentication, is the provided `User` Model which by default has the following attributes:

- `username`
- `password`
- `email`
- `first_name`
- `last_name`

Although these attributes are fine for the Cat Collector, some projects may need additional attributes such as `birthdate`, `favorite_color`, etc. The _Further Study_ section will point you in the right direction should you need this functionality, however, do know that changing the built-in Django functionality is not trivial.

## 3. Creating the `User ---< Cat` Relationship

### Cat Collector's Functionality is Changing

Currently, all furry critters in Cat Collector are wild - they don't belong to a _Cat Collector_ (the user).

The functionality of Cat Collector is about to change!

By the end of this lesson, with authentication implemented, all cats will belong to a user.

As a reminder, it's a best practice to implement an app's authentication up front to avoid having to make the changes to the code we're going to have to make in Cat Collector.

### Update the `Cat` Model

Implementing the relationship of<br>
`User --< Cat`<br>
**_A User has many Cats; and a Cat belongs to a User_**<br>will require a `ForeignKey` attribute like any other one-to-many relationship in Django.

The `User` Model lives in the `django.contrib.auth` app, so the first thing we need to do is import it into **models.py**:

```python
from django.db import models
from datetime import date
# Import the User
from django.contrib.auth.models import User
```

One of the Model's needs a `Foreign Key` attribute... - `User` or `Cat`...

<details>
<summary>
❓ The <code>User</code> or the <code>Cat</code> Model?
</summary>
<hr>

<code>Cat</code> because a Cat <strong>belongs to</strong> a User.

<hr>
</details>

Now let's add the field linking a `Cat` to a `User`:

```python
class Cat(models.Model):
  ...
  toys = models.ManyToManyField(Toy)
  # Add the foreign key linking to a user instance
  user = models.ForeignKey(User, on_delete=models.CASCADE)
```

### Migrate the Change

Now that we've made a change to a Model that impacts the database, we need to migrate that change to the database.

However, there's an issue because:

- The updated `Cat` model now has a FK constraint that requires that each cat row in the database must have a value for its `user_id` column, and
- There are existing cat rows in the database

To address this issue, Django is going to prompt us with two options...

Here we go:

```
python manage.py makemigrations
```

Which then presents us with this message:

```
You are trying to add a non-nullable field 'user' to cat without a default;
we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option:
```

Option `1)` is our best option because it will allow us to enter the `id` of a user, which we created earlier this week (the superuser).

Go ahead and press `1` and `[enter]`, which will then prompt us to enter the value:

```
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available,
so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> 
```

Our superuser's `id` should be `1`, so type `1` and press `[enter]`.

The migration file will then be created.  Let's migrate the changes:

```
python manage.py migrate
```

Congrats, the one-to-many relationship between User and Cat has been created and all existing cats have been collected by the superuser!

## 4. Getting Ready for Auth
To ensure a seamless integration of authentication, it's essential to configure our project to effectively manage auth before we proceed with creating and modifying the serializers, URLs, and views. This process involves installing additional packages and configuring the settings.py file of our project.

### Package Installation

For this project, which functions as a RESTful API and accepts requests from a separate origin, we need to install the following packages:

- **Django Rest Framework Simple JWT**: This package is a JSON Web Token authentication plugin, essential for managing user authentication securely.
- **Django Cors Headers**: This is a Django application that manages Cross-Origin Resource Sharing (CORS) by adding appropriate headers to the responses. This inclusion permits in-browser requests to our Django application from different origins.


Execute the following command in your terminal (ensure you're operating within your virtual environment):

```
pipenv install djangorestframework-simplejwt django-cors-headers
```

### Configuration in `settings.py`
Let's make the following adjustments in the settings.py file to set up the necessary configurations:

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # allows requests from localhost - will need to update again for deployment

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Adjust the port if your frontend runs on a different one
]

# Add 'corsheaders' to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

# Add 'corsheaders.middleware.CorsMiddleware' to MIDDLEWARE
MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# Configuration for django-rest-framework-simplejwt
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Configuration for simple JWT
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

```

**Key Points to Remember**:

- We have enabled access to our Django application from an external origin by specifying ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS.
- The addition of "rest_framework_simplejwt" to INSTALLED_APPS is not mandatory unless advanced token configurations, such as token blacklisting, are required.
- Despite "rest_framework_simplejwt" not being listed in INSTALLED_APPS, we have set up the authentication to utilize rest_framework_simplejwt.
- The JWT settings have been meticulously configured to ensure secure and efficient authentication, including token expiration, encryption algorithm, and more.

These steps lay a solid foundation for integrating a robust and secure authentication system into your Django project.

## 5. Update Serializers
For optimal management and clarity within our project, it's necessary to create a serializer for the User model and enhance the Cat serializer by incorporating the user field. Proceed by making the following modifications to the serializers.py file:

```python
from django.contrib.auth.models import User # add this line to list of imports

# include User serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class CatSerializer(serializers.ModelSerializer):
  fed_for_today = serializers.SerializerMethodField()
  toys = ToySerializer(many=True, read_only=True)
  # add user field to Cat serializer
  user = serializers.PrimaryKeyRelatedField(read_only=True)  # Make the user field read-only
  
  # rest of code
```

#### Key Observations on Serializers

1. **Enhancing User Serializer Security**: In the `UserSerializer`, we've included the `password` field but designated it as `write_only`. This measure is a deliberate strategy to minimize the exposure of sensitive user data and ensure that the password is not included in API responses.

2. **Cat Serializer and User Association**: In the `CatSerializer`, we introduce a `user` field, utilizing `serializers.PrimaryKeyRelatedField`. Importantly, we set this field to `read_only=True`. This setting ensures that while the `user` field is included in the serialized data (providing valuable context and information), it cannot be used to modify the underlying user-cat relationship or the user object itself. This decision effectively preserves data integrity and simplifies the API interaction, as changes to the user must be routed specifically through the User model. Furthermore, this configuration can lead to performance benefits by streamlining the serialization process and eliminating unnecessary write operations.

## 6. Establishing Authentication-Related URLs

Leveraging Django's inherent authentication capabilities and its default configurations is often the most efficient approach. In our scenario, we aim to harmonize these built-in features with custom class-based views. Specifically, we will utilize Django's native User Authentication Model in conjunction with the API views provided by the REST framework and Simple JWT for a robust and secure authentication system.

Before we can harness the power of these views, we need to establish URLs that will route to them.

Let's go ahead and integrate the following routes into our `urls.py` file:

```python
urlpatterns = [
  ...
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
  ...
]
```

These newly defined URL patterns are pivotal for:

1. **User Registration**: The 'register' URL facilitates the registration of new users, enabling them to create an account within the system.
2. **User Login**: The 'login' URL allows existing users to authenticate and gain access to their accounts.
3. **Token Refresh**: The 'token_refresh' URL is crucial for maintaining seamless user sessions. It enables the issuance of a new access JWT token when a user refreshes their page or when the current access token reaches expiration.

By setting up these routes, we pave the way for a fluid and secure user interaction with our application, ensuring that users can register, log in, and maintain their sessions with minimal friction.

Next up, the final piece of the puzzle - our views.

## 7. Constructing Authentication Views

The creation of dedicated User Authentication views is a crucial step in our project, as it lays the foundation for secure user interaction within the system. We will also be refining our Cat Views to ensure they align with our authentication framework.

### User Authentication Views
Integrate the code snippets below into your `views.py` file to establish the necessary authentication views:

```python
from rest_framework import generics, status, permissions # modify these imports to match
...
# include the following imports
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
...
from .serializers import UserSerializer, CatSerializer, ... # add the UserSerizlier to the list
...

# include the registration, login, and verification views below
# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })
```

Key Insights:

1. **CreateUserView**: This view manages user registration. It not only creates a new user but also generates a JWT token, pivotal for authorizing future requests. It's important to note that our server is configured to reject any requests that lack a validated token in the authentication headers.
2. **LoginView**: This view handles user authentication. Upon successful login (validated by username and password), it responds with the user's information alongside fresh access JWT tokens.
3. **VerifyUserView**: This view is responsible for token verification. It examines the token present in the header, and upon successful validation, it provides an updated token along with the user's information.

With these views in place, we've secured the user interaction flow. However, we still need to refine our Cat Views to ensure they're in sync with our authentication architecture.

### Refinement of `CatList` and `CatDetail` Views for Authentication Compliance

To ensure our Cat views align seamlessly with our comprehensive authentication framework, significant updates are required. These modifications are meticulously implemented to guarantee that user interactions with the Cat views are both secure and user-specific.

The updated code is structured as follows:

```python
...
from rest_framework.exceptions import PermissionDenied # include this additional import
...

# Updated CatList and CatDetail views below
class CatList(generics.ListCreateAPIView):
  serializer_class = CatSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      # This ensures we only return cats belonging to the logged-in user
      user = self.request.user
      return Cat.objects.filter(user=user)

  def perform_create(self, serializer):
      # This associates the newly created cat with the logged-in user
      serializer.save(user=self.request.user)

class CatDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = CatSerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Cat.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    toys_not_associated = Toy.objects.exclude(id__in=instance.toys.all())
    toys_serializer = ToySerializer(toys_not_associated, many=True)

    return Response({
        'cat': serializer.data,
        'toys_not_associated': toys_serializer.data
    })

  def perform_update(self, serializer):
    cat = self.get_object()
    if cat.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this cat."})
    serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this cat."})
    instance.delete()
```

Key modifications include:

- **CatList Adjustments**:
  - User-Specific Retrieval: The `get_queryset` method has been tailored to fetch only those cats that are associated with the currently logged-in user, enhancing both security and relevance of the data provided.
  - User Association on Creation: The `perform_create` method ensures that any cat created through this view is automatically associated with the logged-in user, preserving the integrity and privacy of user data.

- **CatDetail Adjustments**:
  - User-Specific Query Set: Similar to `CatList`, the `get_queryset` in `CatDetail` is fine-tuned to return cats that are linked to the logged-in user, ensuring data is personalized and secured.
  - Protected Update and Delete Operations: Both `perform_update` and `perform_destroy` methods are fortified with checks to ensure that the operation is being performed by the user who owns the cat. This is achieved by comparing the cat's user with the logged-in user, and raising a `PermissionDenied` exception if there's a mismatch, thereby safeguarding against unauthorized modifications or deletions.

Through these enhancements, our views are not only more secure but also user-centric, ensuring that each user interacts exclusively with their own cats, thereby upholding data integrity and user privacy within our application.

With that, our updated views are complete!

## 8. Summary

Authentication stands as a cornerstone in the vast majority of applications, underpinning the security and personalized experience that users expect.

The functionality and security of an application are intricately tied to its ability to accurately discern and validate the identity of each user. This critical layer ensures that each interaction with the application is as intended, safeguarded, and tailored to the individual user.

Given the pivotal role of authentication, it's paramount to integrate this feature into your projects from the outset. A robust authentication system not only fortifies the application against unauthorized access but also paves the way for a multitude of user-specific functionalities and services.

In the off chance you had a little trouble following every step, please feel free to view the [Final Code](https://git.generalassemb.ly/SEB-Base-Curriculum/django-catcollector-final) repository. It includes screenshots of how we can test each route on Postman!

On that note, extend yourself a well-deserved congratulations. You've successfully navigated through the complexities of constructing a RESTful API, integrating comprehensive authentication mechanisms, managing complex associations, and embedding custom functionalities. This achievement marks a significant milestone in your journey towards mastering application development and securing digital interactions.

## Suggested Challenge Exercise

Wouldn't it be nice to see the username of the logged in user displayed in the nav bar?

It sure would!

## 9. Lab

Implementing authentication in your Finch Collector project is OPTIONAL.  However, Django authentication is required in the group project.

## 10. Further Study - Customizing the `User` Model

There are a couple of options when it comes to adding additional attributes and/or behavior to the "user" in a Django app.

### APPROACH 1:  "Extending" the Existing `User` Model

This recommended approach would be to extend the current `User` model by creating a one-to-one relationship with another Model, usually named something like `Profile`:

```python
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_color = models.CharField(max_length=50)
```

Start [here](https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-the-existing-user-model) for more info about using this approach.

### APPROACH 2:  Custom `User` Model

> Note:  This approach is more complex and requires more effort to implement - it is recommended that the first approach be followed.

This approach creates a custom `User` Model by inheriting from an `AbstractUser` class provided by Django:

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add your additional features
```

Start [here](https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project) for more information about using this approach.

## References

- [Django Authentication System](https://docs.djangoproject.com/en/4.1/topics/auth/default/)
