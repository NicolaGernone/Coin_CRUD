## Start

To create a Complete CRUDE arquitecture i want base the view on ModelViewSet of Django Rest Framework.
This allow me to inherit all the CRUD method with the use of this class and rooting them in the url.py authomatically with carts as base root.

I've included the listing of carts too, eaven though is not requested in the api. I could exclude it using a GenericViewSet and only include the methods i want.

I've also included the pagination of the list of carts, using the default pagination of Django Rest Framework.

I'll use a Hexagonal Aqruitecture for build the app, so i'll create a folder for each layer of the architecture.

# STEP 1: Create the Models and Serializers

I'll create the models in the domain layer, in the file domain/models.py
I'll create the models with the fields requested in the api, and i'll add a field for the total price of the cart, that will be calculated with the price of the products and the quantity of each product.
The relationtion between the models will be a OneToMany relation, so i'll add a ForeignKey field in the CartItem model. One Cart can have many CartItems, but one CartItem can only have one Cart.

I'll create the serializers in the application layer, in the file application/serializers.py
I'll create the serializers with the fields requested in the api, and i'll add a field for the total price of the cart, that will be calculated with the price of the products and the quantity of each product.
The relationtion between the serializers will be a OneToMany relation, so i'll add a CartItemSerializer field in the CartSerializer. One Cart can have many CartItems, but one CartItem can only have one Cart.

# STEP 2: Create Admin

I'll create the admin in the infrastructure layer, in the file infrastructure/admin.py
I'll register the models in the admin, so i can create, edit and delete the models in the admin page.

# STEP 3: Create the Views

I'll create the admin in the infrastructure layer, in the file infrastructure/views.py
I'll create the views with the ModelViewSet of Django Rest Framework, so i can inherit all the CRUD methods and use them in the api.

# STEP 4: Create the Urls

I'll create the urls in the api layer, in the file api/urls.py
I'll create the urls with the routers of Django Rest Framework.
The base url will be api/carts. The create, update and delete urls will be api/carts/{id}. The list url will be api/carts/list. The retrieve url will be api/carts/{id}/detail.

# STEP 5: Create the Services

I'll create the services in the application layer, in the file application/services.py.
Here i'll implement create, update and delete methods for the carts and cart items.

# STEP 6: Implement update and create methods for CartSerializer

I'll use services in the update and create methods of the CartSerializer, so i can use the services in the api.

# STEP 7: Implement the blockchain in the models and serializers

Added the hash property to the models and serializers, and the calculate_hash method to the models, to simulate a blockchain.

# STEP 8: Implement the tests

Implementation of the tests for the models, views and services.

# STEP 9: Check functionality of services and models.

I'll check the functionality of the services and models in the shell, creating a cart and a cart item, and checking the hash of the cart.

# STEP 10: Check functionality of the api.

I'll check the functionality of the api in the browser, creating a cart and a cart item, and checking the hash of the cart.

# STEP 11: Check functionality of the tests.

I'll check the functionality of the tests in the terminal, running the tests with the command `python manage.py test`.

This is the last part  with adding some pydoc to the code, and adding some comments to the code.