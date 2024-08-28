# Coin_CRUD

## Description

This API is a CRUD for the management of virtual coins. It allows the creation, update and deletion of coins, and also the listing of all coins.

## How it works?

The aim of this API is to manage a shopping cart of our ecommerce website. So, through it, the Fronten Team will be
able to request and create, update or delete any item in the current cart.

Every action of the API will generate a new _Block_ on the _Blockchain_ in order to create a history and persist the
information, so we can retrieve it later, but also keeps a history of which items have the user added to the cart.

### Workflow

The workflow of this API is as follows:

* Create

1. Create request is received
2. Check if the `id` for a Cart is not already used
    1. If it has been used we return error
    2. If it has not been used, we create the cart with the given item and generates a new Block to add to the
       Blockchain
3. Add the new _Block_ to the _Blockchain_ with the current information of this Cart

* Update

1. Update request is received
2. Check if the `id` for a Cart exists
    1. If not exists return error
    2. If exist retrieve it
3. Update the items in the cart and generate a new Block with the information
4. Add the new _Block_ to the _Blockchain_

* Delete

1. Delete request is received
2. Check if the `id` for a Cart exists
    1. If not exists return error
    2. If exist retrieve it
3. Remove cart information and create a new _Block_
4. Add the new _Block_ to the _Blockchain_
