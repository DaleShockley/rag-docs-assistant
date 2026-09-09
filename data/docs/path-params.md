# Path Parameters { #path-parameters }

You can declare path "parameters" or "variables" with the same syntax used by Python format strings:

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

The value of the path parameter `item_id` will be passed to your function as the argument `item_id`.

## Path parameters with types { #path-parameters-with-types }

You can declare the type of a path parameter in the function, using standard Python type annotations. In this case, `item_id` is declared to be an `int`.

/// tip

This will give you editor support inside of your function, with error checks, completion, etc.

///

## Data conversion { #data-conversion }

If you run this example and open your browser at http://127.0.0.1:8000/items/3, you will see a response of `{"item_id":3}`. Notice that the value your function received (and returned) is `3`, as a Python `int`, not a string `"3"`. So, with that type declaration, **FastAPI** gives you automatic request "parsing".

## Data validation { #data-validation }

But if you go to the browser at http://127.0.0.1:8000/items/foo, you will see a nice HTTP error, because the path parameter `item_id` had a value of `"foo"`, which is not an `int`. The same error would appear if you provided a `float` instead of an `int`.

/// tip

So, with the same Python type declaration, **FastAPI** gives you data validation. Notice that the error also clearly states exactly the point where the validation didn't pass.

///

## Documentation { #documentation }

And when you open your browser at http://127.0.0.1:8000/docs, you will see an automatic, interactive, API documentation.

## Standards-based benefits, alternative documentation { #standards-based-benefits-alternative-documentation }

And because the generated schema is from the OpenAPI standard, there are many compatible tools. Because of this, **FastAPI** itself provides an alternative API documentation (using ReDoc).

## Pydantic { #pydantic }

All the data validation is performed under the hood by Pydantic, so you get all the benefits from it. You can use the same type declarations with `str`, `float`, `bool` and many other complex data types.

## Order matters { #order-matters }

When creating *path operations*, you can find situations where you have a fixed path. Like `/users/me`, let's say that it's to get data about the current user. And then you can also have a path `/users/{user_id}` to get data about a specific user by some user ID. Because *path operations* are evaluated in order, you need to make sure that the path for `/users/me` is declared before the one for `/users/{user_id}`. Otherwise, the path for `/users/{user_id}` would match also for `/users/me`, thinking that it's receiving a parameter `user_id` with a value of `"me"`. Similarly, you cannot redefine a path operation: the first one will always be used since the path matches first.

## Predefined values { #predefined-values }

If you have a *path operation* that receives a *path parameter*, but you want the possible valid *path parameter* values to be predefined, you can use a standard Python `Enum`.

### Create an `Enum` class { #create-an-enum-class }

Import `Enum` and create a sub-class that inherits from `str` and from `Enum`. By inheriting from `str` the API docs will be able to know that the values must be of type `string` and will be able to render correctly. Then create class attributes with fixed values, which will be the available valid values.

### Declare a *path parameter* { #declare-a-path-parameter }

Then create a *path parameter* with a type annotation using the enum class you created (`ModelName`).

### Working with Python *enumerations* { #working-with-python-enumerations }

The value of the *path parameter* will be an *enumeration member*. You can compare it with the *enumeration member* in your created enum `ModelName`, and get the actual value using `model_name.value`.

## Path parameters containing paths { #path-parameters-containing-paths }

Let's say you have a *path operation* with a path `/files/{file_path}`. But you need `file_path` itself to contain a *path*, like `home/johndoe/myfile.txt`.

### OpenAPI support { #openapi-support }

OpenAPI doesn't support a way to declare a *path parameter* to contain a *path* inside, as that could lead to scenarios that are difficult to test and define. Nevertheless, you can still do it in **FastAPI**, using one of the internal tools from Starlette.

### Path convertor { #path-convertor }

Using an option directly from Starlette you can declare a *path parameter* containing a *path* using a URL like `/files/{file_path:path}`. In this case, the name of the parameter is `file_path`, and the last part, `:path`, tells it that the parameter should match any *path*.

## Recap { #recap }

With **FastAPI**, by using short, intuitive and standard Python type declarations, you get editor support, data parsing, data validation, and API annotation and automatic documentation. And you only have to declare them once.
