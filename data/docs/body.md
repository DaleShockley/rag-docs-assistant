# Request Body { #request-body }

When you need to send data from a client (let's say, a browser) to your API, you send it as a **request body**. A **request** body is data sent by the client to your API. A **response** body is the data your API sends to the client. Your API almost always has to send a **response** body, but clients don't necessarily need to send **request bodies** all the time.

To declare a **request** body, you use Pydantic models with all their power and benefits.

/// note

To send data, you should use one of: `POST` (the most common), `PUT`, `DELETE` or `PATCH`. Sending a body with a `GET` request has an undefined behavior in the specifications.

///

## Import Pydantic's `BaseModel` { #import-pydantics-basemodel }

First, you need to import `BaseModel` from `pydantic`.

## Create your data model { #create-your-data-model }

Then you declare your data model as a class that inherits from `BaseModel`. Use standard Python types for all the attributes. When a model attribute has a default value, it is not required; otherwise, it is required. Use `None` to make it just optional.

## Declare it as a parameter { #declare-it-as-a-parameter }

To add it to your *path operation*, declare it the same way you declared path and query parameters, using the model you created as the type.

## Results { #results }

With just that Python type declaration, **FastAPI** will read the body of the request as JSON, convert the corresponding types, validate the data (returning a clear error if invalid), give you the received data in the parameter, and generate JSON Schema definitions for your model as part of the OpenAPI schema.

## Automatic docs { #automatic-docs }

The JSON Schemas of your models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs.

## Editor support { #editor-support }

In your editor, inside your function you will get type hints and completion everywhere. This wouldn't happen if you received a `dict` instead of a Pydantic model. You also get error checks for incorrect type operations.

## Use the model { #use-the-model }

Inside of the function, you can access all the attributes of the model object directly.

## Request body + path parameters { #request-body-path-parameters }

You can declare path parameters and request body at the same time. **FastAPI** will recognize that the function parameters that match path parameters should be taken from the path, and that function parameters declared as Pydantic models should be taken from the request body.

## Request body + path + query parameters { #request-body-path-query-parameters }

You can also declare body, path and query parameters, all at the same time. **FastAPI** will recognize each of them and take the data from the correct place: if the parameter is also declared in the path, it will be used as a path parameter; if it's a singular type (`int`, `float`, `str`, `bool`), it's a query parameter; if it's a Pydantic model, it's a request body.

## Without Pydantic { #without-pydantic }

If you don't want to use Pydantic models, you can also use `Body` parameters directly for singular values in the body.
