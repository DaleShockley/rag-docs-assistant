# Handling Errors { #handling-errors }

There are many situations in which you need to report an error to a client that is using your API. In these cases, you would normally return an **HTTP status code** in the range of **400** (from 400 to 499), meaning there was an error from the client. Remember all those "404 Not Found" errors?

## Use `HTTPException` { #use-httpexception }

To return HTTP responses with errors to the client you use `HTTPException`.

### Import `HTTPException` { #import-httpexception }

Import `HTTPException` from `fastapi`.

### Raise an `HTTPException` in your code { #raise-an-httpexception-in-your-code }

`HTTPException` is a normal Python exception with additional data relevant for APIs. Because it's a Python exception, you don't `return` it, you `raise` it. If you raise the `HTTPException` from inside a utility function, it won't run the rest of the code in the path operation function; it will terminate that request right away and send the HTTP error to the client.

### The resulting response { #the-resulting-response }

If the client requests a non-existent item, that client will receive an HTTP status code of 404, and a JSON response like `{"detail": "Item not found"}`.

/// tip

When raising an `HTTPException`, you can pass any value that can be converted to JSON as the `detail` parameter, not only `str`. You could pass a `dict`, a `list`, etc.

///

## Add custom headers { #add-custom-headers }

There are some situations where it's useful to be able to add custom headers to the HTTP error, for example for some types of security.

## Install custom exception handlers { #install-custom-exception-handlers }

You can add custom exception handlers with the same exception utilities from Starlette. If you have a custom exception that you or a library you use might raise, you can handle it globally with FastAPI using `@app.exception_handler()`.

## Override the default exception handlers { #override-the-default-exception-handlers }

**FastAPI** has some default exception handlers in charge of returning the default JSON responses when you raise an `HTTPException` and when the request has invalid data. You can override these with your own.

### Override request validation exceptions { #override-request-validation-exceptions }

When a request contains invalid data, **FastAPI** internally raises a `RequestValidationError`, and includes a default exception handler for it. To override it, import `RequestValidationError` and use it with `@app.exception_handler(RequestValidationError)`.

### Override the `HTTPException` error handler { #override-the-httpexception-error-handler }

The same way, you can override the `HTTPException` handler, for example to return a plain text response instead of JSON.

/// warning

The `RequestValidationError` contains the file name and line where the validation error happened, so converting it directly to a string and returning it could leak information about your system.

///

### Use the `RequestValidationError` body { #use-the-requestvalidationerror-body }

The `RequestValidationError` contains the `body` it received with invalid data. You could use it while developing your app to log the body and debug it, or return it to the user.

#### FastAPI's `HTTPException` vs Starlette's `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** has its own `HTTPException`, which inherits from Starlette's `HTTPException`. The only difference is that FastAPI's `HTTPException` accepts any JSON-able data for the `detail` field, while Starlette's only accepts strings. When you register an exception handler, you should register it for Starlette's `HTTPException`, so that internal Starlette code or plug-ins that raise it will also be caught.

### Reuse **FastAPI**'s exception handlers { #reuse-fastapis-exception-handlers }

If you want to use your exception along with the same default exception handlers from **FastAPI**, you can import and reuse the default exception handlers from `fastapi.exception_handlers`.
