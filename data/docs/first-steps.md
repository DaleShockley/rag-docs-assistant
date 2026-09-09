# First Steps { #first-steps }

The simplest FastAPI file could look like this:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

Copy that to a file `main.py`.

Run the live server:

```console
$ fastapi dev

  FastAPI  Starting development server

   server  Server started at http://127.0.0.1:8000
   server  Documentation at http://127.0.0.1:8000/docs
```

### Check it { #check-it }

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

You will see the JSON response as:

```JSON
{"message": "Hello World"}
```

### Interactive API docs { #interactive-api-docs }

Now go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic interactive API documentation (provided by Swagger UI).

### Alternative API docs { #alternative-api-docs }

And now, go to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

You will see the alternative automatic documentation (provided by ReDoc).

### OpenAPI { #openapi }

**FastAPI** generates a "schema" with all your API using the **OpenAPI** standard for defining APIs.

#### "Schema" { #schema }

A "schema" is a definition or description of something. Not the code that implements it, but just an abstract description.

#### API "schema" { #api-schema }

OpenAPI is a specification that dictates how to define a schema of your API. This schema definition includes your API paths, the possible parameters they take, etc.

#### Data "schema" { #data-schema }

The term "schema" might also refer to the shape of some data, like a JSON content. In that case, it would mean the JSON attributes, and data types they have, etc.

#### Check the `openapi.json` { #check-the-openapi-json }

If you are curious about what the raw OpenAPI schema looks like, FastAPI automatically generates a JSON (schema) with the descriptions of all your API. You can see it directly at: http://127.0.0.1:8000/openapi.json.

## Recap, step by step { #recap-step-by-step }

### Step 1: import `FastAPI` { #step-1-import-fastapi }

`FastAPI` is a Python class that provides all the functionality for your API. `FastAPI` is a class that inherits directly from `Starlette`. You can use all the Starlette functionality with `FastAPI` too.

### Step 2: create a `FastAPI` "instance" { #step-2-create-a-fastapi-instance }

Here the `app` variable will be an "instance" of the class `FastAPI`. This will be the main point of interaction to create all your API.

### Step 3: create a *path operation* { #step-3-create-a-path-operation }

#### Path { #path }

"Path" here refers to the last part of the URL starting from the first `/`. A "path" is also commonly called an "endpoint" or a "route".

#### Operation { #operation }

"Operation" here refers to one of the HTTP "methods": `POST`, `GET`, `PUT`, `DELETE`, and the more exotic ones: `OPTIONS`, `HEAD`, `PATCH`, `TRACE`. Normally you use `POST` to create data, `GET` to read data, `PUT` to update data, and `DELETE` to delete data. In OpenAPI, each of the HTTP methods is called an "operation".

#### Define a *path operation decorator* { #define-a-path-operation-decorator }

The `@app.get("/")` tells **FastAPI** that the function right below is in charge of handling requests that go to the path `/` using a `get` operation. It is the "**path operation decorator**".

### Step 4: define the **path operation function** { #step-4-define-the-path-operation-function }

This is our "path operation function": path is `/`, operation is `get`, function is the function below the decorator. It will be called by **FastAPI** whenever it receives a request to the URL "`/`" using a `GET` operation.

### Step 5: return the content { #step-5-return-the-content }

You can return a `dict`, `list`, singular values as `str`, `int`, etc. You can also return Pydantic models. There are many other objects and models that will be automatically converted to JSON (including ORMs, etc).

## Recap { #recap }

* Import `FastAPI`.
* Create an `app` instance.
* Write a **path operation decorator** using decorators like `@app.get("/")`.
* Define a **path operation function**; for example, `def root(): ...`.
* Run the development server using the command `fastapi dev`.
