# Query Parameters { #query-parameters }

When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.

The query is the set of key-value pairs that go after the `?` in a URL, separated by `&` characters. For example, in the URL `http://127.0.0.1:8000/items/?skip=0&limit=10`, the query parameters are `skip` with a value of `0` and `limit` with a value of `10`.

As they are part of the URL, they are "naturally" strings. But when you declare them with Python types (as `int`), they are converted to that type and validated against it. All the same processes that apply to path parameters also apply to query parameters: editor support, data parsing, data validation, and automatic documentation.

## Defaults { #defaults }

As query parameters are not a fixed part of a path, they can be optional and can have default values. Going to a URL without the query parameters would use the default values, e.g. `skip=0` and `limit=10`.

## Optional parameters { #optional-parameters }

You can declare optional query parameters, by setting their default to `None`.

/// tip

**FastAPI** is smart enough to notice that a path parameter like `item_id` is a path parameter and `q` is not, so it's a query parameter.

///

## Query parameter type conversion { #query-parameter-type-conversion }

You can also declare `bool` types, and they will be converted. Values like `1`, `True`, `true`, `on`, and `yes` (in any case variation) will all be converted to a `bool` value of `True`. Otherwise `False`.

## Multiple path and query parameters { #multiple-path-and-query-parameters }

You can declare multiple path parameters and query parameters at the same time, **FastAPI** knows which is which, and you don't have to declare them in any specific order. They will be detected by name.

## Required query parameters { #required-query-parameters }

When you declare a default value for non-path parameters, it is not required. If you don't want to add a specific value but just make it optional, set the default as `None`. But when you want to make a query parameter required, you can just not declare any default value.

If you don't add the required parameter, you will see an error like:

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "needy"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

You can also define some parameters as required, some as having a default value, and some entirely optional, for example `needy` (a required `str`), `skip` (an `int` with a default value of `0`), and `limit` (an optional `int`).

/// tip

You could also use `Enum`s the same way as with Path Parameters.

///
